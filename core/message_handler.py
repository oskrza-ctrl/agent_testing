"""
MessageHandler — núcleo de la lógica conversacional.

Cualquier canal (CLI, Telegram, API web, app) llama a process_message()
y recibe una respuesta en texto. El canal no sabe nada del pipeline interno.
"""
from datetime import datetime
from pathlib import Path
from typing import Optional

from openai import OpenAI

from services.rag.chromadb_rag_service import ChromaDBRAGService
from services.rag.intent_classifier import classify_intent
from agents.query_agent import QueryAgent
from agents.analysis_agent import AnalysisAgent
from agents.markdown_agent import MarkdownAgent
from agents.knowledge_base_agent import KnowledgeBaseAgent, ACCUMULATIVE
from agents.transcription_agent import TranscriptionAgent


_FOLDER_LABEL = {
    **{cat: info[0] for cat, info in ACCUMULATIVE.items()},
    "Reunión":      "Meetings",
    "Nota general": "General_Notes",
}


class MessageHandler:
    """
    Canal-agnostic message processor.

    Usage:
        handler = MessageHandler(...)
        response = handler.process_message("¿qué ideas tengo?")
        response = handler.process_message("idea: usar RAG en el proyecto SAT")
    """

    def __init__(
        self,
        openai_client: OpenAI,
        rag_service: ChromaDBRAGService,
        query_agent: QueryAgent,
        analysis_agent: AnalysisAgent,
        markdown_agent: MarkdownAgent,
        kb_agent: KnowledgeBaseAgent,
        kb_dir: Path,
        output_dir: Path,
        transcription_agent: Optional[TranscriptionAgent] = None,
        tasks_agent=None,
        calendar_agent=None,
    ):
        self.client               = openai_client
        self.rag_service          = rag_service
        self.query_agent          = query_agent
        self.analysis_agent       = analysis_agent
        self.markdown_agent       = markdown_agent
        self.kb_agent             = kb_agent
        self.kb_dir               = kb_dir
        self.output_dir           = output_dir
        self.transcription_agent  = transcription_agent
        self.tasks_agent          = tasks_agent
        self.calendar_agent       = calendar_agent

    # ── Public interface ──────────────────────────────────────────

    def process_message(self, text: str) -> str:
        """Classify intent and route to the right handler. Returns a response string."""
        intent = classify_intent(self.client, text)
        if intent == "CAPTURE":
            return self._handle_capture(text)
        return self.query_agent.chat(text)

    def process_voice(self, file_path: Path) -> str:
        """Transcribe an audio file and process it as CAPTURE. Always saves to KB."""
        if not self.transcription_agent:
            return "Error: TranscriptionAgent no configurado."
        stem   = f"voice_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        source = f"telegram:{stem}"
        transcript = self.transcription_agent.run(file_path)
        return self._handle_capture_from_transcript(transcript, stem, source)

    def reset_conversation(self) -> None:
        """Clear in-session conversation history."""
        self.query_agent.reset()

    # ── Capture ───────────────────────────────────────────────────

    def _handle_capture(self, text: str) -> str:
        stem   = f"chat_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        source = f"chat:{stem}"
        return self._handle_capture_from_transcript(text, stem, source)

    def _handle_capture_from_transcript(self, transcript: str, stem: str, source: str) -> str:
        result = self.analysis_agent.run(transcript)
        self.markdown_agent.run(self.output_dir, stem, transcript, result)
        self.kb_agent.run(result, source)

        tasks_msg = self._run_tasks(result, source)
        cal_msg   = self._run_calendar(result, source)

        # Re-index so the new content is queryable immediately
        self.rag_service.index_kb(self.kb_dir)

        folder = _FOLDER_LABEL.get(result.category, result.category)
        tags   = " ".join(result.tags) if result.tags else "sin tags"

        return (
            f"[Guardado] {result.category} — \"{result.title}\"\n"
            f"  Carpeta : Knowledge_Base/{folder}/\n"
            f"  Tags    : {tags}"
            f"{tasks_msg}"
            f"{cal_msg}"
        )

    def _run_tasks(self, result, source: str) -> str:
        if not self.tasks_agent or not result.tasks:
            return ""
        try:
            self.tasks_agent.run(result, source)
            return f"\n  Tasks   : {len(result.tasks)} tarea(s) enviadas a Google Tasks"
        except Exception as e:
            return f"\n  Tasks   : error — {e}"

    def _run_calendar(self, result, source: str) -> str:
        if not self.calendar_agent:
            return ""
        cal_candidates = [
            r for r in result.reminders
            if "[candidato: google calendar]" in r.lower()
        ]
        if not cal_candidates:
            return ""
        try:
            self.calendar_agent.run(result, source)
            return f"\n  Calendar: {len(cal_candidates)} evento(s) enviados a Google Calendar"
        except Exception as e:
            return f"\n  Calendar: error — {e}"
