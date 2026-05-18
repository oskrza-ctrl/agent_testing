from abc import ABC, abstractmethod
from datetime import date
from typing import Optional


class TasksService(ABC):
    """Base interface for task creation providers (Google Tasks, Todoist, etc.)."""

    @abstractmethod
    def create_task(self, title: str, notes: str = "", due_date: Optional[date] = None) -> str:
        """Create a task and return its provider ID."""
        ...

    @abstractmethod
    def list_tasks(self) -> list[dict]:
        """Return pending tasks as list of {id, title, due}."""
        ...

    @abstractmethod
    def complete_task(self, task_id: str) -> None:
        """Mark a task as completed by its provider ID."""
        ...
