from dotenv import load_dotenv
from pathlib import Path
import os

load_dotenv()

api_key = os.getenv("OPENAI_API_KEY")

if api_key:
    print("API key loaded successfully")
else:
    print("OPENAI_API_KEY not found")

# Buscar archivos MP3 en la carpeta input/
input_dir = Path("input")
mp3_files = list(input_dir.glob("*.mp3"))

if not mp3_files:
    print("No MP3 files found in input/")
else:
    # Por ahora usamos solo el primero encontrado
    print(f"MP3 file found: {mp3_files[0].name}")
