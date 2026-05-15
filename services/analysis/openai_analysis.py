import json

from openai import OpenAI

from services.analysis.base import AnalysisService
from services.analysis.analysis_result import AnalysisResult


class OpenAIAnalysisService(AnalysisService):
    """Text analysis using OpenAI GPT-4o-mini. Returns a structured AnalysisResult."""

    def __init__(self, api_key: str):
        self.client = OpenAI(api_key=api_key)

    def analyze(self, prompt: str) -> AnalysisResult:
        print("\nAnalyzing transcript...")

        response = self.client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[{"role": "user", "content": prompt}],
            response_format={"type": "json_object"},
        )

        data = json.loads(response.choices[0].message.content)

        return AnalysisResult(
            category=data.get("category", "Nota general"),
            title=data.get("title", "Sin título"),
            summary=data.get("summary", ""),
            ideas=data.get("ideas", []),
            tasks=data.get("tasks", []),
            reminders=data.get("reminders", []),
            related_project=data.get("related_project", "No asignado"),
            ambiguity_notes=data.get("ambiguity_notes", ""),
            tags=data.get("tags", []),
            participants=data.get("participants", []),
            decisions=data.get("decisions", []),
            actions_for_me=data.get("actions_for_me", []),
            actions_for_others=data.get("actions_for_others", []),
            risks_blockers=data.get("risks_blockers", []),
            next_steps=data.get("next_steps", []),
        )
