from abc import ABC, abstractmethod


class AnalysisService(ABC):
    """Base interface for text analysis providers.

    Implement this to add a new provider (e.g. LocalModelAnalysisService).
    """

    @abstractmethod
    def analyze(self, transcript: str) -> str:
        """Analyze a transcript and return a Markdown string."""
        ...
