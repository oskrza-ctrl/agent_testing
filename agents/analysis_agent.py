from pathlib import Path

from services.analysis.base import AnalysisService
from services.analysis.analysis_result import AnalysisResult
from services.prompt_loader import load_prompt


class AnalysisAgent:
    """Runs the analysis step using instructions from prompts/analysis_agent.md."""

    def __init__(self, service: AnalysisService, prompts_dir: Path):
        self.service = service
        self.instructions = load_prompt(prompts_dir, "analysis_agent.md")

    def run(self, transcript: str) -> AnalysisResult:
        prompt = (
            self.instructions
            + "\n\n---\n\n"
            + f"Transcript:\n{transcript}"
        )
        return self.service.analyze(prompt)
