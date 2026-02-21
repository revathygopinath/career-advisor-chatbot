"""
chat_manager.py
---------------
Manages conversation history and session memory.
Keeps track of all messages in a structured format compatible with the Gemini API.
"""

from dataclasses import dataclass, field
from typing import List, Literal
from logger import get_logger

logger = get_logger(__name__)

# Gemini API expects roles: "user" or "model"
Role = Literal["user", "model"]

# Maximum number of messages to keep in memory (token safety)
MAX_HISTORY_MESSAGES = 8


@dataclass
class Message:
    """Represents a single message in the conversation."""
    role: Role
    content: str

    def to_dict(self) -> dict:
        """Converts to the format expected by the Gemini API."""
        return {
            "role": self.role,
            "parts": [{"text": self.content}]
        }

    def to_display_dict(self) -> dict:
        """Converts to a format suitable for Streamlit's chat display."""
        display_role = "user" if self.role == "user" else "assistant"
        return {
            "role": display_role,
            "content": self.content
        }


@dataclass
class ChatSession:
    """
    Manages the full conversation history for a single session.
    Intended to be stored in Streamlit's session_state.
    """
    messages: List[Message] = field(default_factory=list)
    total_user_messages: int = 0
    total_tokens_used: int = 0

    def add_user_message(self, content: str) -> None:
        """Adds a user message to the conversation history."""
        if not content or not content.strip():
            logger.warning("Attempted to add empty user message — skipped.")
            return

        self.messages.append(
            Message(role="user", content=content.strip())
        )
        self.total_user_messages += 1
        self._trim_history()

        logger.debug(
            f"User message added. Total user messages: {self.total_user_messages}"
        )

    def add_model_message(self, content: str) -> None:
        """Adds a model (assistant) message to the conversation history."""
        if not content or not content.strip():
            logger.warning("Attempted to add empty model message — skipped.")
            return

        self.messages.append(
            Message(role="model", content=content.strip())
        )
        self._trim_history()

        logger.debug(
            f"Model message added. Current history length: {len(self.messages)}"
        )

    def _trim_history(self) -> None:
        """
        Keeps only the most recent messages to control token usage.
        """
        if len(self.messages) > MAX_HISTORY_MESSAGES:
            removed = len(self.messages) - MAX_HISTORY_MESSAGES
            self.messages = self.messages[-MAX_HISTORY_MESSAGES:]
            logger.debug(f"Trimmed {removed} old messages from history.")

    def get_history_for_api(self) -> List[dict]:
        """
        Returns conversation history formatted for the Gemini API.
        """
        return [msg.to_dict() for msg in self.messages]

    def get_history_for_display(self) -> List[dict]:
        """
        Returns conversation history formatted for Streamlit display.
        """
        return [msg.to_display_dict() for msg in self.messages]

    def update_token_count(self, tokens: int) -> None:
        """Tracks cumulative token usage for monitoring and cost awareness."""
        self.total_tokens_used += tokens
        logger.debug(
            f"Token usage updated. Total tokens used: {self.total_tokens_used}"
        )

    def clear(self) -> None:
        """Clears the entire conversation history."""
        message_count = len(self.messages)
        self.messages.clear()
        self.total_user_messages = 0
        self.total_tokens_used = 0

        logger.info(
            f"Chat session cleared. Removed {message_count} messages."
        )

    def is_empty(self) -> bool:
        """Returns True if no messages exist."""
        return len(self.messages) == 0

    @property
    def message_count(self) -> int:
        """Returns total number of messages in the conversation."""
        return len(self.messages)