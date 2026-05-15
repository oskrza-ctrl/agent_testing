from pathlib import Path
from openai import OpenAI

from services.transcription.base import TranscriptionService


class OpenAITranscriptionService(TranscriptionService):
    """Transcription using OpenAI Whisper API (whisper-1)."""

    def __init__(self, api_key: str):
        self.client = OpenAI(api_key=api_key)

    def transcribe(self, mp3_path: Path) -> str:
        print("Transcribing...")

        with open(mp3_path, "rb") as audio_file:
            response = self.client.audio.transcriptions.create(
                model="whisper-1",
                file=audio_file
            )

        transcript = response.text
        print("\n--- Transcript ---")
        print(transcript)
        return transcript
