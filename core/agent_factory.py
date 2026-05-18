"""
agent_factory.py — construye un MessageHandler listo para usar.

Cualquier entrypoint (chat.py, telegram_bot.py, api.py) llama a
build_message_handler() y obtiene todo configurado sin repetir código.
"""
import os
from pathlib import Path

from openai import OpenAI

from services.analysis.openai_analysis import OpenAIAnalysisService
from services.transcription.openai_transcription import OpenAITranscriptionService
from services.rag.chromadb_rag_service import ChromaDBRAGService
from agents.analysis_agent import AnalysisAgent
from agents.markdown_agent import MarkdownAgent
from agents.knowledge_base_agent import KnowledgeBaseAgent
from agents.query_agent import QueryAgent
from agents.transcription_agent import TranscriptionAgent
from core.message_handler import MessageHandler


def build_message_handler(
    api_key: str,
    kb_dir: Path      = Path("Knowledge_Base"),
    output_dir: Path  = Path("output"),
    persist_dir: Path = Path("chroma_db"),
    prompts_dir: Path = Path("prompts"),
) -> MessageHandler:
    """
    Initialize all agents and return a ready-to-use MessageHandler.

    Optional Google integrations (Tasks, Calendar) are enabled automatically
    if credentials/credentials.json exists.
    """
    output_dir.mkdir(exist_ok=True)

    # ── OpenAI client ─────────────────────────────────────────────
    client = OpenAI(api_key=api_key)

    # ── RAG ───────────────────────────────────────────────────────
    rag_service = ChromaDBRAGService(api_key=api_key, persist_dir=persist_dir)
    if kb_dir.exists() and any(kb_dir.rglob("*.md")):
        print("[factory] Indexando Knowledge Base...")
        total = rag_service.index_kb(kb_dir)
        print(f"[factory] {total} fragmentos indexados.")
    else:
        print("[factory] Knowledge Base vacia — solo modo captura disponible.")

    query_agent = QueryAgent(rag_service, prompts_dir=prompts_dir)

    # ── Capture pipeline ──────────────────────────────────────────
    transcription_agent = TranscriptionAgent(OpenAITranscriptionService(api_key))
    analysis_agent      = AnalysisAgent(OpenAIAnalysisService(api_key), prompts_dir)
    markdown_agent      = MarkdownAgent()
    kb_agent            = KnowledgeBaseAgent(kb_dir)

    # ── Google integrations (opcionales) ─────────────────────────
    credentials_file = Path(
        os.getenv("GOOGLE_CREDENTIALS_FILE", "credentials/credentials.json")
    )
    tasks_agent    = _build_tasks_agent(credentials_file, kb_dir)
    calendar_agent = _build_calendar_agent(credentials_file, kb_dir)

    return MessageHandler(
        openai_client        = client,
        rag_service          = rag_service,
        query_agent          = query_agent,
        transcription_agent  = transcription_agent,
        analysis_agent       = analysis_agent,
        markdown_agent       = markdown_agent,
        kb_agent             = kb_agent,
        kb_dir               = kb_dir,
        output_dir           = output_dir,
        tasks_agent          = tasks_agent,
        calendar_agent       = calendar_agent,
    )


# ── Optional Google helpers ───────────────────────────────────────

def _build_tasks_agent(credentials_file: Path, kb_dir: Path):
    token_file = Path(os.getenv("GOOGLE_TOKEN_FILE", "credentials/token.json"))
    if not credentials_file.exists():
        return None
    try:
        from services.tasks.google_tasks_service import GoogleTasksService
        from agents.tasks_agent import TasksAgent
        svc = GoogleTasksService(credentials_file, token_file)
        return TasksAgent(svc, kb_dir / "Tasks" / "created_tasks.json")
    except Exception as e:
        print(f"[factory] Google Tasks no disponible: {e}")
        return None


def _build_calendar_agent(credentials_file: Path, kb_dir: Path):
    cal_token = Path(os.getenv("GOOGLE_CALENDAR_TOKEN_FILE", "credentials/token_calendar.json"))
    timezone  = os.getenv("GOOGLE_CALENDAR_TIMEZONE", "America/Mexico_City")
    if not credentials_file.exists():
        return None
    try:
        from services.calendar.google_calendar_service import GoogleCalendarService
        from agents.calendar_agent import CalendarAgent
        svc = GoogleCalendarService(credentials_file, cal_token, timezone)
        return CalendarAgent(svc, kb_dir / "Reminders" / "created_events.json")
    except Exception as e:
        print(f"[factory] Google Calendar no disponible: {e}")
        return None
