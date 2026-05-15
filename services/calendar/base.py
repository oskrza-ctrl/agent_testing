from abc import ABC, abstractmethod
from datetime import datetime


class CalendarService(ABC):
    """Base interface for calendar event providers (Google Calendar, etc.)."""

    @abstractmethod
    def create_event(
        self,
        title: str,
        start: datetime,
        end: datetime,
        description: str = "",
    ) -> str:
        """Create a calendar event and return its provider ID."""
        ...
