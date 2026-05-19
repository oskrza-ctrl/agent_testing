"""
MessageHandler — núcleo de la lógica conversacional.

Cualquier canal (CLI, Telegram, API web, app) llama a process_message()
y recibe una respuesta en texto. El canal no sabe nada del pipeline interno.
"""
import re
from datetime import datetime
from pathlib import Path
from typing import Optional

from openai import OpenAI

from services.rag.chromadb_rag_service import ChromaDBRAGService
from services.rag.intent_classifier import classify_intent
from services.rag.action_classifier import classify_action
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
        drive_agent=None,
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
        self.drive_agent          = drive_agent

    # ── Public interface ──────────────────────────────────────────

    def process_message(self, text: str) -> str:
        """Route message: pipeline and actions are explicit; everything else is conversational."""
        intent = classify_intent(self.client, text)
        if intent == "PIPELINE":
            return self.run_pipeline()
        if intent == "ACTION":
            return self._handle_action(text)

        # Conversational flow — GPT responds naturally and decides when to capture
        response = self.query_agent.chat(text)
        return self._process_capture_marker(response)

    def _process_capture_marker(self, response: str) -> str:
        """Detect [CAPTURE: ...] marker in GPT response, execute capture silently, return clean message."""
        match = re.search(r'\[CAPTURE:(.*?)\]', response, re.DOTALL)
        if not match:
            return response

        capture_text = match.group(1).strip()
        clean_response = re.sub(r'\[CAPTURE:.*?\]', '', response, flags=re.DOTALL).strip()

        # Execute capture silently
        capture_result = self._handle_capture(capture_text)

        # Append a brief save confirmation
        folder = capture_result.split("\n")[0] if capture_result else ""
        return f"{clean_response}\n\n_{folder}_"

    def run_pipeline(self) -> str:
        """Run the full MP3 processing pipeline and return a conversational summary."""
        import subprocess, sys
        from datetime import datetime

        print("[MessageHandler] Iniciando pipeline de procesamiento...")
        start_time = datetime.now()

        try:
            result = subprocess.run(
                [sys.executable, "main.py"],
                capture_output=True, text=True, timeout=600
            )
        except subprocess.TimeoutExpired:
            return "El pipeline tardó demasiado (más de 10 min). Revisa input/ manualmente."
        except Exception as e:
            return f"Error al correr el pipeline: {e}"

        if result.returncode != 0:
            return f"El pipeline terminó con errores:\n{(result.stdout or '')[-500:]}"

        # Re-index para que los nuevos contenidos sean consultables
        self.rag_service.index_kb(self.kb_dir)

        # Leer las nuevas entradas de la KB creadas durante este run
        new_entries = self._get_new_kb_entries(start_time)

        if not new_entries:
            return "Revisé el inbox pero no había archivos nuevos para procesar."

        # GPT genera una respuesta conversacional sobre lo que se procesó
        return self._summarize_pipeline_results(new_entries)

    def _get_new_kb_entries(self, since: "datetime") -> list[dict]:
        """Collect KB entries written after 'since' timestamp."""
        import re
        from datetime import datetime

        entries = []
        if not self.kb_dir.exists():
            return entries

        for md_file in self.kb_dir.rglob("*.md"):
            # Skip dedup JSONs
            if md_file.suffix != ".md":
                continue
            mtime = datetime.fromtimestamp(md_file.stat().st_mtime)
            if mtime < since:
                continue

            content = md_file.read_text(encoding="utf-8")
            # Get the last entry (after the last separator)
            parts = re.split(r"\n---\n\n", content)
            last = parts[-1].strip()
            if len(last) > 50:
                entries.append({
                    "file": md_file.name,
                    "folder": md_file.parent.name,
                    "content": last[:600],
                })

        return entries

    def _summarize_pipeline_results(self, entries: list[dict]) -> str:
        """Ask GPT to generate a conversational summary of what was just processed."""
        context = "\n\n---\n\n".join(
            f"[{e['folder']}] {e['file']}:\n{e['content']}"
            for e in entries
        )
        prompt = (
            "El usuario acaba de pedirte que proceses sus audios. "
            "Aquí están las nuevas entradas que se guardaron en su base de conocimiento:\n\n"
            f"{context}\n\n"
            "Responde de forma conversacional y natural, como si fueras su asistente personal. "
            "Cuéntale qué se procesó, qué tipo de contenido era (idea, tarea, reunión, etc.), "
            "los puntos más importantes y si se crearon tareas o eventos. "
            "Sé conciso pero informativo. No uses listas con bullets si puedes evitarlo."
        )
        response = self.client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": "Eres el asistente personal del usuario, conoces su base de conocimiento."},
                {"role": "user",   "content": prompt},
            ],
            temperature=0.5,
        )
        return response.choices[0].message.content.strip()

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

        # Sync the modified KB file(s) to Google Drive
        self._sync_kb_to_drive(result)

        folder = _FOLDER_LABEL.get(result.category, result.category)
        tags   = " ".join(result.tags) if result.tags else "sin tags"

        return (
            f"[Guardado] {result.category} — \"{result.title}\"\n"
            f"  Carpeta : Knowledge_Base/{folder}/\n"
            f"  Tags    : {tags}"
            f"{tasks_msg}"
            f"{cal_msg}"
        )

    # ── Action ────────────────────────────────────────────

    def _handle_action(self, text: str) -> str:
        """Level-2 routing: determine the specific action and execute it."""
        action = classify_action(self.client, text)

        if action == "COMPLETE_TASK":
            if not self.tasks_agent:
                return "Google Tasks no está configurado."
            return self.tasks_agent.find_and_complete(text, self.client)

        if action == "ARCHIVE_EVENTS":
            if not self.calendar_agent:
                return "Google Calendar no está configurado."
            return self.calendar_agent.archive_past_events()

        return "No entendí qué acción querías ejecutar."

    def _sync_kb_to_drive(self, result) -> None:
        """Upload the KB file(s) modified by this capture to Google Drive."""
        if not self.drive_agent:
            return

        # Accumulative categories → single known file
        accumulative = {
            "Idea":         self.kb_dir / "Ideas"         / "ideas.md",
            "Tarea":        self.kb_dir / "Tasks"         / "tasks.md",
            "Recordatorio": self.kb_dir / "Reminders"     / "reminders.md",
            "Proyecto":     self.kb_dir / "Projects"      / "projects.md",
        }
        # Individual categories → most recently modified file in folder
        individual = {
            "Reunión":      self.kb_dir / "Meetings",
            "Nota general": self.kb_dir / "General_Notes",
        }

        if result.category in accumulative:
            f = accumulative[result.category]
            if f.exists():
                self.drive_agent.upload_kb_file(f)
        elif result.category in individual:
            folder = individual[result.category]
            if folder.exists():
                files = sorted(folder.glob("*.md"), key=lambda x: x.stat().st_mtime, reverse=True)
                if files:
                    self.drive_agent.upload_kb_file(files[0])

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
