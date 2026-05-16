from abc import ABC, abstractmethod
from pathlib import Path
from typing import List, Dict


class RAGService(ABC):

    @abstractmethod
    def index_kb(self, kb_dir: Path) -> int:
        """Index all markdown files in kb_dir. Returns total chunks indexed."""
        ...

    @abstractmethod
    def query(self, message: str, history: List[Dict]) -> str:
        """Search KB for relevant context and generate a response."""
        ...
