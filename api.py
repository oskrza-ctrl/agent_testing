"""
api.py — Entrypoint HTTP del Second Brain Agent (FastAPI).

Uso:
    python api.py

Endpoints:
    GET  /health        — estado del servicio
    POST /chat          — mensaje de texto → respuesta del agente
    GET  /kb/{category} — contenido de una categoría de la Knowledge Base
"""
import os
from pathlib import Path

import uvicorn
from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from core.agent_factory import build_message_handler

load_dotenv()

app = FastAPI(title="Second Brain Agent API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

KB_CATEGORIES = {"ideas", "tasks", "meetings", "reminders", "projects", "notes"}
KB_FOLDER_MAP = {
    "ideas":     "Ideas/ideas.md",
    "tasks":     "Tasks/tasks.md",
    "reminders": "Reminders/reminders.md",
    "projects":  "Projects/projects.md",
    "meetings":  "Meetings",
    "notes":     "General_Notes",
}

_handler = None


def get_handler():
    global _handler
    if _handler is None:
        api_key = os.getenv("OPENAI_API_KEY")
        if not api_key:
            raise ValueError("OPENAI_API_KEY no configurada.")
        _handler = build_message_handler(api_key=api_key)
    return _handler


# ── Schemas ───────────────────────────────────────────────────────

class ChatRequest(BaseModel):
    message: str

class ChatResponse(BaseModel):
    response: str


# ── Endpoints ─────────────────────────────────────────────────────

@app.get("/health")
def health():
    return {"status": "ok"}


@app.post("/chat", response_model=ChatResponse)
def chat(req: ChatRequest):
    if not req.message.strip():
        raise HTTPException(status_code=400, detail="El mensaje no puede estar vacío.")
    response = get_handler().process_message(req.message)
    return ChatResponse(response=response)


@app.get("/kb/{category}")
def kb(category: str):
    """Return the content of a KB category as plain text."""
    if category not in KB_CATEGORIES:
        raise HTTPException(
            status_code=404,
            detail=f"Categoría no válida. Opciones: {sorted(KB_CATEGORIES)}",
        )
    kb_dir  = Path("Knowledge_Base")
    target  = kb_dir / KB_FOLDER_MAP[category]

    # Accumulative files (single .md)
    if target.suffix == ".md":
        if not target.exists():
            return {"category": category, "content": ""}
        return {"category": category, "content": target.read_text(encoding="utf-8")}

    # Individual files (folder with multiple .md)
    if not target.exists():
        return {"category": category, "files": []}
    files = sorted(target.glob("*.md"), reverse=True)
    return {
        "category": category,
        "files": [
            {"name": f.name, "content": f.read_text(encoding="utf-8")}
            for f in files
        ],
    }


# ── Main ──────────────────────────────────────────────────────────

if __name__ == "__main__":
    port = int(os.getenv("PORT", 8000))
    uvicorn.run("api:app", host="0.0.0.0", port=port, reload=False)
