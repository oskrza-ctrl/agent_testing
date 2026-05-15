from pathlib import Path

from services.transcription.base import TranscriptionService


class TranscriptionAgent:
    """Runs the transcription step for a given MP3 file."""

    def __init__(self, service: TranscriptionService):
        self.service = service

    def run(self, mp3_path: Path) -> str:
        return self.service.transcribe(mp3_path)
