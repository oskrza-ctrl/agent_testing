from abc import ABC, abstractmethod

from services.analysis.analysis_result import AnalysisResult


class AnalysisService(ABC):
    """Base interface for text analysis providers.

    Implement this to add a new provider (e.g. LocalModelAnalysisService).
    """

    @abstractmethod
    def analyze(self, prompt: str) -> AnalysisResult:
        """Send a fully assembled prompt and return a structured AnalysisResult."""
        ...
