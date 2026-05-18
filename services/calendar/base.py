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

    @abstractmethod
    def list_past_events(self, max_results: int = 20) -> list[dict]:
        """Return past events as list of {id, title, start}."""
        ...

    @abstractmethod
    def delete_event(self, event_id: str) -> None:
        """Delete a calendar event by its provider ID."""
        ...
