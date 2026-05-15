from pathlib import Path
from typing import Optional

from services.transcription.base import TranscriptionService
from services.analysis.base import AnalysisService
from services.tasks.base import TasksService
from services.calendar.base import CalendarService
from services.file_service import find_all_mp3, save_text

from agents.transcription_agent import TranscriptionAgent
from agents.analysis_agent import AnalysisAgent
from agents.markdown_agent import MarkdownAgent
from agents.knowledge_base_agent import KnowledgeBaseAgent
from agents.tasks_agent import TasksAgent
from agents.calendar_agent import CalendarAgent
from agents.archive_agent import ArchiveAgent
from agents.drive_agent import DriveAgent


class OrchestratorAgent:
    """Coordinates the full pipeline for all MP3s in input/ (or Drive Inbox)."""

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
        self.input_dir  = input_dir
        self.output_dir = output_dir
        self.kb_dir     = kb_dir
        self.drive_agent = drive_agent

        self.transcription_agent = TranscriptionAgent(transcription_svc)
        self.analysis_agent      = AnalysisAgent(analysis_svc, prompts_dir)
        self.markdown_agent      = MarkdownAgent()
        self.kb_agent            = KnowledgeBaseAgent(kb_dir)
        self.archive_agent       = ArchiveAgent(processed_dir)

        self.tasks_agent = (
            TasksAgent(tasks_svc, kb_dir / "Tasks" / "created_tasks.json")
            if tasks_svc else None
        )
        self.calendar_agent = (
            CalendarAgent(calendar_svc, kb_dir / "Reminders" / "created_events.json")
            if calendar_svc else None
        )

    def run(self) -> None:
        # If Drive is enabled, download MP3s from Inbox first
        if self.drive_agent:
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
        """Process a single MP3. Returns True on success, False on failure."""
        try:
            transcript = self.transcription_agent.run(mp3_path)
            save_text(self.output_dir / f"{mp3_path.stem}_transcript.txt", transcript)

            result = self.analysis_agent.run(transcript)
            print(f"[OrchestratorAgent] Category: {result.category} | Title: {result.title}")

            self.markdown_agent.run(self.output_dir, mp3_path.stem, transcript, result)
            self.kb_agent.run(result, mp3_path.name)

            # Sync updated KB files to Drive
            if self.drive_agent:
                self._sync_kb_to_drive(result)

            if self.tasks_agent:
                self.tasks_agent.run(result, mp3_path.name)

            if self.calendar_agent:
                self.calendar_agent.run(result, mp3_path.name)

        except Exception as e:
            print(f"[OrchestratorAgent] ERROR on {mp3_path.name}: {e}")
            print(f"[OrchestratorAgent] File was NOT moved. Check input/ for the original.")
            return False

        self.archive_agent.run(mp3_path)

        # Move the original file in Drive after successful archive
        if self.drive_agent:
            self.drive_agent.move_to_processed(mp3_path.name)

        return True

    def _sync_kb_to_drive(self, result) -> None:
        """Upload the KB files that were just written for this result."""
        from agents.knowledge_base_agent import ACCUMULATIVE, INDIVIDUAL
        import re
        from datetime import date

        # Determine which files were touched based on category
        files_to_sync = []

        if result.category in ACCUMULATIVE:
            folder, filename, _ = ACCUMULATIVE[result.category]
            files_to_sync.append(self.kb_dir / folder / filename)

        elif result.category not in ACCUMULATIVE:
            # Individual file — reconstruct filename same way KnowledgeBaseAgent does
            folder_key = "Reunion" if result.category == "Reunión" else result.category
            folder = INDIVIDUAL.get(folder_key, "General_Notes")
            today  = date.today().isoformat()
            safe   = re.sub(r"[^\w\s-]", "", result.title.lower())
            safe   = re.sub(r"\s+", "_", safe.strip())[:50].rstrip("_") or "sin_titulo"
            files_to_sync.append(self.kb_dir / folder / f"{today}_{safe}.md")

            # Also sync secondary files if any were written
            if result.tasks:
                files_to_sync.append(self.kb_dir / "Tasks" / "tasks.md")
            if result.reminders:
                files_to_sync.append(self.kb_dir / "Reminders" / "reminders.md")
            if result.ideas:
                files_to_sync.append(self.kb_dir / "Ideas" / "ideas.md")

        for f in files_to_sync:
            if f.exists():
                self.drive_agent.upload_kb_file(f)
