from datetime import date
from pathlib import Path

from services.analysis.base import AnalysisService
from services.analysis.analysis_result import AnalysisResult
from services.prompt_loader import load_prompt

_DAYS_ES = ["lunes", "martes", "miércoles", "jueves", "viernes", "sábado", "domingo"]


class AnalysisAgent:
    """Runs the analysis step using instructions from prompts/analysis_agent.md."""

    def __init__(self, service: AnalysisService, prompts_dir: Path):
        self.service = service
        self.instructions = load_prompt(prompts_dir, "analysis_agent.md")

    def run(self, transcript: str) -> AnalysisResult:
        today = date.today()
        day_name = _DAYS_ES[today.weekday()]
        date_context = (
            f"Fecha de hoy: {today.isoformat()} ({day_name}). "
            f"Usa esta fecha para resolver referencias temporales relativas "
            f"como 'hoy', 'mañana', 'el viernes', 'la próxima semana'."
        )
        prompt = (
            self.instructions
            + "\n\n---\n\n"
            + f"{date_context}\n\n"
            + f"Transcript:\n{transcript}"
        )
        return self.service.analyze(prompt)
