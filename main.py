from dotenv import load_dotenv
from pathlib import Path
import os

from services.file_service import find_mp3, save_text
from services.markdown_service import ensure_transcript, save_markdown
from services.transcription.openai_transcription import OpenAITranscriptionService
from services.analysis.openai_analysis import OpenAIAnalysisService

load_dotenv()

api_key = os.getenv("OPENAI_API_KEY")

if not api_key:
    print("OPENAI_API_KEY not found")
    exit(1)

print("API key loaded successfully")

input_dir = Path("input")
output_dir = Path("output")

transcription_svc = OpenAITranscriptionService(api_key)
analysis_svc = OpenAIAnalysisService(api_key)

# Buscar MP3
mp3_path = find_mp3(input_dir)

# Transcribir y guardar transcript
transcript = transcription_svc.transcribe(mp3_path)
save_text(output_dir / f"{mp3_path.stem}_transcript.txt", transcript)

# Analizar y guardar Markdown
markdown = analysis_svc.analyze(transcript)
markdown = ensure_transcript(markdown, transcript)
save_markdown(output_dir / f"{mp3_path.stem}_analysis.md", markdown)
