from services.analysis.base import AnalysisService


class AnalysisAgent:
    """Runs the analysis step on a transcript and returns Markdown."""

    def __init__(self, service: AnalysisService):
        self.service = service

    def run(self, transcript: str) -> str:
        return self.service.analyze(transcript)
