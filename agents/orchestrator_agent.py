from pathlib import Path
from typing import Optional

from services.transcription.base import TranscriptionService
from services.analysis.base import AnalysisService
from services.tasks.base import TasksService
from services.calendar.base import CalendarService
from services.file_service import find_all_mp3

from agents.transcription_agent import TranscriptionAgent
from agents.analysis_agent import AnalysisAgent
from agents.markdown_agent import MarkdownAgent
from agents.knowledge_base_agent import KnowledgeBaseAgent
from agents.tasks_agent import TasksAgent
from agents.calendar_agent import CalendarAgent
from agents.archive_agent import ArchiveAgent
from agents.drive_agent import DriveAgent
from pipeline.graph import build_graph


class OrchestratorAgent:
    """Coordinates the full pipeline via a LangGraph StateGraph."""

    def __init__(
        self,
        transcription_svc: TranscriptionService,
        analysis_svc: AnalysisService,
        input_dir: Path,
        output_dir: Path,
        processed_dir: Path,
        prompts_dir: Path,
        kb_dir: Path,
        tasks_svc: Optional[TasksService] = None,
        calendar_svc: Optional[CalendarService] = None,
        drive_agent: Optional[DriveAgent] = None,
    ):
        self.input_dir   = input_dir
        self.output_dir  = output_dir
        self.kb_dir      = kb_dir
        self.drive_agent = drive_agent

        # Build individual agents
        transcription_agent = TranscriptionAgent(transcription_svc)
        analysis_agent      = AnalysisAgent(analysis_svc, prompts_dir)
        markdown_agent      = MarkdownAgent()
        kb_agent            = KnowledgeBaseAgent(kb_dir)
        archive_agent       = ArchiveAgent(processed_dir)

        tasks_agent = (
            TasksAgent(tasks_svc, kb_dir / "Tasks" / "created_tasks.json")
            if tasks_svc else None
        )
        calendar_agent = (
            CalendarAgent(calendar_svc, kb_dir / "Reminders" / "created_events.json")
            if calendar_svc else None
        )

        # Build LangGraph pipeline
        self.pipeline = build_graph(
            agents={
                "transcription":  transcription_agent,
                "analysis":       analysis_agent,
                "markdown":       markdown_agent,
                "kb":             kb_agent,
                "tasks":          tasks_agent,
                "calendar":       calendar_agent,
                "archive":        archive_agent,
                "drive":          drive_agent,
                "drive_sync_fn":  self._sync_kb_to_drive if drive_agent else None,
            },
            dirs={"output": output_dir, "kb": kb_dir},
        )

    def run(self) -> None:
        if self.drive_agent:
            self.drive_agent.download_kb()
            print("\n[DriveAgent] Syncing inbox from Google Drive...")
            self.drive_agent.download_inbox()

        mp3_files = find_all_mp3(self.input_dir)

        if not mp3_files:
            return

        ok, failed = 0, 0

        for mp3_path in mp3_files:
            print(f"\n{'-' * 50}")
            print(f"Processing: {mp3_path.name}")
            if self._process_one(mp3_path):
                ok += 1
            else:
                failed += 1

        print(f"\n{'=' * 50}")
        print(f"Done. Total: {len(mp3_files)} | OK: {ok} | Failed: {failed}")
        print(f"{'=' * 50}")

    def _process_one(self, mp3_path: Path) -> bool:
        initial_state = {
            "mp3_path":   mp3_path,
            "mp3_name":   mp3_path.name,
            "mp3_stem":   mp3_path.stem,
            "transcript": "",
            "result":     None,
            "error":      None,
        }

        final_state = self.pipeline.invoke(initial_state)

        if final_state.get("error"):
            print(f"[OrchestratorAgent] ERROR on {mp3_path.name}: {final_state['error']}")
            print("[OrchestratorAgent] File was NOT moved. Check input/ for the original.")
            return False

        return True

    def _sync_kb_to_drive(self, result) -> None:
        """Upload KB files that were written for this result to Drive."""
        from agents.knowledge_base_agent import ACCUMULATIVE, INDIVIDUAL
        import re
        from datetime import date

        files_to_sync = []

        if result.category in ACCUMULATIVE:
            folder, filename, _ = ACCUMULATIVE[result.category]
            files_to_sync.append(self.kb_dir / folder / filename)
        else:
            folder_key = "Reunion" if result.category == "Reunión" else result.category
            folder = INDIVIDUAL.get(folder_key, "General_Notes")
            today  = date.today().isoformat()
            safe   = re.sub(r"[^\w\s-]", "", result.title.lower())
            safe   = re.sub(r"\s+", "_", safe.strip())[:50].rstrip("_") or "sin_titulo"
            files_to_sync.append(self.kb_dir / folder / f"{today}_{safe}.md")

            if result.tasks:
                files_to_sync.append(self.kb_dir / "Tasks" / "tasks.md")
            if result.reminders:
                files_to_sync.append(self.kb_dir / "Reminders" / "reminders.md")
            if result.ideas:
                files_to_sync.append(self.kb_dir / "Ideas" / "ideas.md")

        for f in files_to_sync:
            if f.exists():
                self.drive_agent.upload_kb_file(f)
