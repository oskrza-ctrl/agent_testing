from abc import ABC, abstractmethod
from pathlib import Path


class TranscriptionService(ABC):
    """Base interface for transcription providers.

    Implement this to add a new provider (e.g. LocalWhisperTranscriptionService).
    """

    @abstractmethod
    def transcribe(self, mp3_path: Path) -> str:
        """Transcribe an MP3 file and return the text."""
        ...
