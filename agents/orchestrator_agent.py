from pathlib import Path

from services.transcription.base import TranscriptionService
from services.analysis.base import AnalysisService
from services.file_service import find_all_mp3, save_text

from agents.transcription_agent import TranscriptionAgent
from agents.analysis_agent import AnalysisAgent
from agents.markdown_agent import MarkdownAgent
from agents.knowledge_base_agent import KnowledgeBaseAgent
from agents.archive_agent import ArchiveAgent


class OrchestratorAgent:
    """Coordinates the full pipeline for all MP3s in input/."""

    def __init__(
        self,
        transcription_svc: TranscriptionService,
        analysis_svc: AnalysisService,
        input_dir: Path,
        output_dir: Path,
        processed_dir: Path,
        prompts_dir: Path,
        kb_dir: Path,
    ):
        self.input_dir = input_dir
        self.output_dir = output_dir

        self.transcription_agent = TranscriptionAgent(transcription_svc)
        self.analysis_agent = AnalysisAgent(analysis_svc, prompts_dir)
        self.markdown_agent = MarkdownAgent()
        self.kb_agent = KnowledgeBaseAgent(kb_dir)
        self.archive_agent = ArchiveAgent(processed_dir)

    def run(self) -> None:
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

        except Exception as e:
            print(f"[OrchestratorAgent] ERROR on {mp3_path.name}: {e}")
            print(f"[OrchestratorAgent] File was NOT moved. Check input/ for the original.")
            return False

        self.archive_agent.run(mp3_path)
        return True
