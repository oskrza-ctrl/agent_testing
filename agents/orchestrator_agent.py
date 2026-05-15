from pathlib import Path

from services.transcription.base import TranscriptionService
from services.analysis.base import AnalysisService
from services.file_service import find_mp3, save_text

from agents.transcription_agent import TranscriptionAgent
from agents.analysis_agent import AnalysisAgent
from agents.markdown_agent import MarkdownAgent
from agents.archive_agent import ArchiveAgent


class OrchestratorAgent:
    """Coordinates the full pipeline: find → transcribe → analyze → save → archive."""

    def __init__(
        self,
        transcription_svc: TranscriptionService,
        analysis_svc: AnalysisService,
        input_dir: Path,
        output_dir: Path,
        processed_dir: Path,
    ):
        self.input_dir = input_dir
        self.output_dir = output_dir

        self.transcription_agent = TranscriptionAgent(transcription_svc)
        self.analysis_agent = AnalysisAgent(analysis_svc)
        self.markdown_agent = MarkdownAgent()
        self.archive_agent = ArchiveAgent(processed_dir)

    def run(self) -> None:
        mp3_path = find_mp3(self.input_dir)

        # If any step fails, the MP3 stays in input/ for manual review
        try:
            transcript = self.transcription_agent.run(mp3_path)
            save_text(self.output_dir / f"{mp3_path.stem}_transcript.txt", transcript)

            markdown = self.analysis_agent.run(transcript)
            self.markdown_agent.run(self.output_dir, mp3_path.stem, transcript, markdown)

        except Exception as e:
            print(f"\n[OrchestratorAgent] Error during processing: {e}")
            print("[OrchestratorAgent] File was NOT moved. Check input/ for the original.")
            return

        # Only archive after a successful run
        self.archive_agent.run(mp3_path)
