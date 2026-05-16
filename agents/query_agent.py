from pathlib import Path
from typing import List, Dict

from services.rag.base import RAGService
from services.prompt_loader import load_prompt


class QueryAgent:
    """Conversational agent that answers questions about the user's Knowledge Base."""

    MAX_HISTORY = 10  # number of messages (user+assistant pairs) passed to the LLM

    def __init__(self, service: RAGService, prompts_dir: Path):
        self.service       = service
        self.history: List[Dict] = []
        system_prompt      = load_prompt(prompts_dir, "query_agent.md")
        self._system_msg   = {"role": "system", "content": system_prompt}

    def chat(self, user_message: str) -> str:
        # Build context: system prompt + trimmed history
        trimmed_history = self.history[-self.MAX_HISTORY:]
        messages_with_system = [self._system_msg] + trimmed_history

        response = self.service.query(user_message, messages_with_system)

        # Persist exchange to history
        self.history.append({"role": "user",      "content": user_message})
        self.history.append({"role": "assistant",  "content": response})

        return response

    def reset(self) -> None:
        self.history.clear()
