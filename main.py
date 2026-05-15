from dotenv import load_dotenv
from pathlib import Path
import os

from services.transcription.openai_transcription import OpenAITranscriptionService
from services.analysis.openai_analysis import OpenAIAnalysisService
from agents.orchestrator_agent import OrchestratorAgent

load_dotenv()

api_key = os.getenv("OPENAI_API_KEY")

if not api_key:
    print("OPENAI_API_KEY not found")
    exit(1)

print("API key loaded successfully")

transcription_svc = OpenAITranscriptionService(api_key)
analysis_svc = OpenAIAnalysisService(api_key)

orchestrator = OrchestratorAgent(
    transcription_svc=transcription_svc,
    analysis_svc=analysis_svc,
    input_dir=Path("input"),
    output_dir=Path("output"),
    processed_dir=Path("processed"),
    prompts_dir=Path("prompts"),
    kb_dir=Path("Knowledge_Base"),
)

orchestrator.run()
