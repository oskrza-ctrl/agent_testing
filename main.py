from dotenv import load_dotenv
from pathlib import Path
from openai import OpenAI
import os

from services.file_service import find_mp3, save_text
from services.transcription_service import transcribe
from services.analysis_service import analyze
from services.markdown_service import ensure_transcript, save_markdown

load_dotenv()

api_key = os.getenv("OPENAI_API_KEY")

if not api_key:
    print("OPENAI_API_KEY not found")
    exit(1)

print("API key loaded successfully")

client = OpenAI(api_key=api_key)
input_dir = Path("input")
output_dir = Path("output")

# Buscar MP3
mp3_path = find_mp3(input_dir)

# Transcribir
transcript = transcribe(client, mp3_path)
save_text(output_dir / f"{mp3_path.stem}_transcript.txt", transcript)

# Analizar y guardar Markdown
markdown = analyze(client, transcript)
markdown = ensure_transcript(markdown, transcript)
save_markdown(output_dir / f"{mp3_path.stem}_analysis.md", markdown)
