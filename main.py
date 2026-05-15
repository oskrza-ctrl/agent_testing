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

client = OpenAI(api_key=api_key)

# --- PASO 1: Transcripción con Whisper ---
print("Transcribing...")

with open(mp3_path, "rb") as audio_file:
    response = client.audio.transcriptions.create(
        model="whisper-1",
        file=audio_file
    )

transcript = response.text

print("\n--- Transcript ---")
print(transcript)

# Guardar transcript como .txt
output_dir = Path("output")
transcript_file = output_dir / f"{mp3_path.stem}_transcript.txt"
transcript_file.write_text(transcript, encoding="utf-8")
print(f"\nTranscript saved to: {transcript_file}")

# --- PASO 2: Análisis con GPT-4o mini (modelo económico para texto) ---
print("\nAnalyzing transcript...")

prompt = f"""Analiza el siguiente transcript de audio y genera un documento Markdown con estas secciones exactas.
Si no detectas información para una sección, escribe "No detectado". No inventes información.

Transcript:
{transcript}

Responde SOLO con el contenido Markdown, sin explicaciones adicionales.

# Título sugerido

## Resumen

## Ideas detectadas

## Tareas accionables

## Proyectos relacionados

## Recordatorios

## Tags

## Transcript completo
"""

analysis_response = client.chat.completions.create(
    model="gpt-4o-mini",
    messages=[{"role": "user", "content": prompt}]
)

markdown_content = analysis_response.choices[0].message.content

# Agregar el transcript completo al final si el modelo no lo incluyó
if transcript not in markdown_content:
    markdown_content += f"\n\n{transcript}"

# Guardar el análisis como .md
analysis_file = output_dir / f"{mp3_path.stem}_analysis.md"
analysis_file.write_text(markdown_content, encoding="utf-8")
print(f"Analysis saved to: {analysis_file}")
