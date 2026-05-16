import uuid
from pathlib import Path
from typing import List, Dict

import chromadb
from openai import OpenAI

from services.rag.base import RAGService
from services.rag.indexer import load_chunks


class ChromaDBRAGService(RAGService):

    COLLECTION      = "second_brain_kb"
    EMBED_MODEL     = "text-embedding-3-small"
    CHAT_MODEL      = "gpt-4o-mini"
    TOP_K           = 5
    # ChromaDB returns distances (lower = more similar). Threshold below which
    # we consider a result "not relevant enough".
    DISTANCE_THRESHOLD = 1.0   # cosine distance: 0 = identical, 2 = opposite

    def __init__(self, api_key: str, persist_dir: Path):
        self.client    = OpenAI(api_key=api_key)
        self.chroma    = chromadb.PersistentClient(path=str(persist_dir))
        self._col      = None   # initialized on first use

    # ── Public interface ──────────────────────────────────────────

    def index_kb(self, kb_dir: Path) -> int:
        # Always recreate the collection for a fresh index
        try:
            self.chroma.delete_collection(self.COLLECTION)
        except Exception:
            pass
        self._col = self.chroma.create_collection(
            name=self.COLLECTION,
            metadata={"hnsw:space": "cosine"},
        )

        chunks = load_chunks(kb_dir)
        if not chunks:
            return 0

        texts     = [c["text"]     for c in chunks]
        metadatas = [{"source": c["source"], "category": c["category"], "date": c["date"]}
                     for c in chunks]
        ids       = [str(uuid.uuid4()) for _ in chunks]

        embeddings = self._embed(texts)
        self._col.add(embeddings=embeddings, documents=texts, metadatas=metadatas, ids=ids)
        return len(chunks)

    def query(self, message: str, history: List[Dict]) -> str:
        col = self._get_collection()

        # Retrieve most similar chunks
        query_embedding = self._embed([message])[0]
        results = col.query(
            query_embeddings=[query_embedding],
            n_results=min(self.TOP_K, col.count()),
            include=["documents", "metadatas", "distances"],
        )

        docs      = results["documents"][0]
        distances = results["distances"][0]

        # Filter by relevance threshold
        relevant = [
            (doc, meta, dist)
            for doc, meta, dist in zip(docs, results["metadatas"][0], distances)
            if dist < self.DISTANCE_THRESHOLD
        ]

        if not relevant:
            return (
                "No encontré información relevante sobre eso en tu base de conocimiento. "
                "Intenta reformular la pregunta o procesa más audios primero."
            )

        context = self._build_context(relevant)
        return self._generate(message, context, history)

    # ── Internal helpers ──────────────────────────────────────────

    def _get_collection(self):
        if self._col is None:
            self._col = self.chroma.get_collection(self.COLLECTION)
        return self._col

    def _embed(self, texts: List[str]) -> List[List[float]]:
        response = self.client.embeddings.create(model=self.EMBED_MODEL, input=texts)
        return [item.embedding for item in response.data]

    def _build_context(self, relevant: list) -> str:
        parts = []
        for doc, meta, dist in relevant:
            header = f"[{meta['category']} | {meta['source']} | {meta.get('date', '')}]"
            parts.append(f"{header}\n{doc}")
        return "\n\n---\n\n".join(parts)

    def _generate(self, message: str, context: str, history: List[Dict]) -> str:
        from services.prompt_loader import load_prompt
        # system prompt is injected by QueryAgent — here we just call the API
        messages = history + [
            {
                "role": "user",
                "content": (
                    f"Contexto de tu base de conocimiento:\n\n{context}"
                    f"\n\n---\n\nPregunta: {message}"
                ),
            }
        ]
        response = self.client.chat.completions.create(
            model=self.CHAT_MODEL,
            messages=messages,
            temperature=0.3,
        )
        return response.choices[0].message.content.strip()
