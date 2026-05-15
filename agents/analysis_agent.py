from pathlib import Path

from services.analysis.base import AnalysisService
from services.prompt_loader import load_prompt


class AnalysisAgent:
    """Runs the analysis step using instructions from prompts/analysis_agent.md."""

    def __init__(self, service: AnalysisService, prompts_dir: Path):
        self.service = service
        self.instructions = load_prompt(prompts_dir, "analysis_agent.md")

    def run(self, transcript: str) -> str:
        prompt = (
            self.instructions
            + "\n\n---\n\n"
            + f"Transcript:\n{transcript}\n\n"
            + "Responde SOLO con el contenido Markdown, sin explicaciones adicionales."
        )
        return self.service.analyze(prompt)
