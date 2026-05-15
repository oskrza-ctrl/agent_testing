from pathlib import Path
from openai import OpenAI


def transcribe(client: OpenAI, mp3_path: Path) -> str:
    """Transcribes an MP3 file using OpenAI Whisper and returns the transcript text."""
    print("Transcribing...")

    with open(mp3_path, "rb") as audio_file:
        response = client.audio.transcriptions.create(
            model="whisper-1",
            file=audio_file
        )

    transcript = response.text
    print("\n--- Transcript ---")
    print(transcript)
    return transcript
