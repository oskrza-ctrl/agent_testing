"""
chat.py — Agente consultable + captura por texto (Paso 18)

Uso:
    python chat.py

Comandos dentro del chat:
    salir   — termina la sesión
    reset   — reinicia el historial de conversación
"""
import os
from datetime import datetime
from pathlib import Path

from dotenv import load_dotenv
from openai import OpenAI

from services.rag.chromadb_rag_service import ChromaDBRAGService
from services.rag.intent_classifier import classify_intent
from services.analysis.openai_analysis import OpenAIAnalysisService
from agents.query_agent import QueryAgent
from agents.analysis_agent import AnalysisAgent
from agents.markdown_agent import MarkdownAgent
from agents.knowledge_base_agent import KnowledgeBaseAgent, ACCUMULATIVE, INDIVIDUAL


# ── Carpeta KB → nombre legible para feedback ───────────────────
_FOLDER_LABEL = {
    **{cat: info[0] for cat, info in ACCUMULATIVE.items()},
    "Reunión":      "Meetings",
    "Nota general": "General_Notes",
}


def _build_tasks_agent(credentials_file, kb_dir):
    token_file = Path(os.getenv("GOOGLE_TOKEN_FILE", "credentials/token.json"))
    if not credentials_file.exists():
        return None
    try:
        from services.tasks.google_tasks_service import GoogleTasksService
        from agents.tasks_agent import TasksAgent
        svc = GoogleTasksService(credentials_file, token_file)
        return TasksAgent(svc, kb_dir / "Tasks" / "created_tasks.json")
    except Exception as e:
        print(f"[chat] Google Tasks no disponible: {e}")
        return None


def _build_calendar_agent(credentials_file, kb_dir):
    cal_token   = Path(os.getenv("GOOGLE_CALENDAR_TOKEN_FILE", "credentials/token_calendar.json"))
    timezone    = os.getenv("GOOGLE_CALENDAR_TIMEZONE", "America/Mexico_City")
    if not credentials_file.exists():
        return None
    try:
        from services.calendar.google_calendar_service import GoogleCalendarService
        from agents.calendar_agent import CalendarAgent
        svc = GoogleCalendarService(credentials_file, cal_token, timezone)
        return CalendarAgent(svc, kb_dir / "Reminders" / "created_events.json")
    except Exception as e:
        print(f"[chat] Google Calendar no disponible: {e}")
        return None


def _handle_capture(
    text: str,
    analysis_agent: AnalysisAgent,
    markdown_agent: MarkdownAgent,
    kb_agent: KnowledgeBaseAgent,
    tasks_agent,
    calendar_agent,
    rag_service: ChromaDBRAGService,
    output_dir: Path,
    kb_dir: Path,
) -> str:
    stem   = f"chat_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
    source = f"chat:{stem}"

    # 1. Clasificar y extraer datos del texto
    result = analysis_agent.run(text)

    # 2. Respaldo .md en output/
    markdown_agent.run(output_dir, stem, text, result)

    # 3. Knowledge Base (crea el .md en la carpeta correcta)
    kb_agent.run(result, source)

    # 4. Google Tasks (opcional)
    tasks_msg = ""
    if tasks_agent:
        try:
            tasks_agent.run(result, source)
            if result.tasks:
                tasks_msg = f"\n  Google Tasks: procesadas ({len(result.tasks)} tarea(s))"
        except Exception as e:
            tasks_msg = f"\n  Google Tasks: error — {e}"

    # 5. Google Calendar (opcional)
    cal_msg = ""
    if calendar_agent:
        try:
            calendar_agent.run(result, source)
            reminders_with_cal = [
                r for r in result.reminders
                if "[candidato: google calendar]" in r.lower()
            ]
            if reminders_with_cal:
                cal_msg = f"\n  Google Calendar: procesado ({len(reminders_with_cal)} evento(s))"
        except Exception as e:
            cal_msg = f"\n  Google Calendar: error — {e}"

    # 6. Re-indexar para que el nuevo contenido sea consultable de inmediato
    rag_service.index_kb(kb_dir)

    # 7. Feedback al usuario
    folder = _FOLDER_LABEL.get(result.category, result.category)
    tags   = " ".join(result.tags) if result.tags else "sin tags"

    return (
        f"[Guardado] {result.category} — \"{result.title}\"\n"
        f"  Carpeta: Knowledge_Base/{folder}/\n"
        f"  Tags: {tags}"
        f"{tasks_msg}"
        f"{cal_msg}"
    )


def main() -> None:
    load_dotenv()

    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        raise ValueError("OPENAI_API_KEY no configurada en .env")

    kb_dir      = Path("Knowledge_Base")
    output_dir  = Path("output")
    persist_dir = Path("chroma_db")
    prompts_dir = Path("prompts")
    output_dir.mkdir(exist_ok=True)

    # ── RAG (consulta) ───────────────────────────────────────────
    rag_service = ChromaDBRAGService(api_key=api_key, persist_dir=persist_dir)

    if kb_dir.exists() and any(kb_dir.rglob("*.md")):
        print("\n[RAG] Indexando Knowledge Base...")
        total = rag_service.index_kb(kb_dir)
        print(f"[RAG] {total} fragmentos indexados.")
    else:
        print("[RAG] Knowledge Base vacia — solo modo captura disponible.")

    query_agent = QueryAgent(rag_service, prompts_dir=prompts_dir)

    # ── Pipeline de captura ──────────────────────────────────────
    openai_client    = OpenAI(api_key=api_key)
    analysis_svc     = OpenAIAnalysisService(api_key)
    analysis_agent   = AnalysisAgent(analysis_svc, prompts_dir)
    markdown_agent   = MarkdownAgent()
    kb_agent         = KnowledgeBaseAgent(kb_dir)

    credentials_file = Path(os.getenv("GOOGLE_CREDENTIALS_FILE", "credentials/credentials.json"))
    tasks_agent      = _build_tasks_agent(credentials_file, kb_dir)
    calendar_agent   = _build_calendar_agent(credentials_file, kb_dir)

    # ── Chat loop ────────────────────────────────────────────────
    print("\nListo. Escribe tu pregunta o comparte algo nuevo.")
    print("Comandos: 'reset' = nueva conversacion | 'salir' = terminar\n")
    print("-" * 60)

    while True:
        try:
            user_input = input("Tu: ").strip()
        except (EOFError, KeyboardInterrupt):
            print("\n[chat] Sesion terminada.")
            break

        if not user_input:
            continue

        if user_input.lower() == "salir":
            print("[chat] Hasta luego.")
            break

        if user_input.lower() == "reset":
            query_agent.reset()
            print("[chat] Conversacion reiniciada.\n")
            print("-" * 60)
            continue

        # Clasificar intención
        intent = classify_intent(openai_client, user_input)

        if intent == "CAPTURE":
            response = _handle_capture(
                text=user_input,
                analysis_agent=analysis_agent,
                markdown_agent=markdown_agent,
                kb_agent=kb_agent,
                tasks_agent=tasks_agent,
                calendar_agent=calendar_agent,
                rag_service=rag_service,
                output_dir=output_dir,
                kb_dir=kb_dir,
            )
        else:
            response = query_agent.chat(user_input)

        print(f"\nAgente: {response}\n")
        print("-" * 60)


if __name__ == "__main__":
    main()
