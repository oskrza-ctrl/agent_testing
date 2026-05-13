from dotenv import load_dotenv
from pathlib import Path
from openai import OpenAI
import os

load_dotenv()

api_key = os.getenv("OPENAI_API_KEY")

if not api_key:
    print("OPENAI_API_KEY not found")
    exit(1)

print("API key loaded successfully")

# Buscar el primer MP3 en input/
input_dir = Path("input")
mp3_files = list(input_dir.glob("*.mp3"))

if not mp3_files:
    print("No MP3 files found in input/")
    exit(1)

mp3_path = mp3_files[0]
print(f"MP3 file found: {mp3_path.name}")

# Transcribir con OpenAI Whisper (whisper-1 es el modelo más económico disponible)
client = OpenAI(api_key=api_key)

print("Transcribing...")

with open(mp3_path, "rb") as audio_file:
    response = client.audio.transcriptions.create(
        model="whisper-1",
        file=audio_file
    )

print("\n--- Transcript ---")
print(response.text)
