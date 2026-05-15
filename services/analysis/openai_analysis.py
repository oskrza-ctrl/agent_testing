from openai import OpenAI

from services.analysis.base import AnalysisService


class OpenAIAnalysisService(AnalysisService):
    """Text analysis using OpenAI GPT-4o-mini."""

    def __init__(self, api_key: str):
        self.client = OpenAI(api_key=api_key)

    def analyze(self, prompt: str) -> str:
        print("\nAnalyzing transcript...")

        response = self.client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[{"role": "user", "content": prompt}]
        )

        return response.choices[0].message.content
