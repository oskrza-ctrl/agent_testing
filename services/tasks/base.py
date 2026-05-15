from abc import ABC, abstractmethod
from datetime import date
from typing import Optional


class TasksService(ABC):
    """Base interface for task creation providers (Google Tasks, Todoist, etc.)."""

    @abstractmethod
    def create_task(self, title: str, notes: str = "", due_date: Optional[date] = None) -> str:
        """Create a task and return its provider ID."""
        ...
