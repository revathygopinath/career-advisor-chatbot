"""
gemini_client.py
----------------
Gemini client using stateless generate_content (production-safe).
"""

import time
from typing import Tuple
from google import genai
from google.genai import types

from config import (
    GEMINI_API_KEY,
    MODEL_NAME,
    TEMPERATURE,
    MAX_OUTPUT_TOKENS,
)
from prompt_manager import get_system_prompt, get_fallback_message
from chat_manager import ChatSession
from logger import get_logger

logger = get_logger(__name__)


class GeminiClient:
    def __init__(self):
        self.client = genai.Client(api_key=GEMINI_API_KEY)
        self.model_name = MODEL_NAME

        self.config = types.GenerateContentConfig(
            temperature=TEMPERATURE,
            max_output_tokens=MAX_OUTPUT_TOKENS,
        )

        logger.info(f"GeminiClient initialized | model={self.model_name}")

    def _build_prompt(self, user_message: str, session: ChatSession) -> str:
        """
        Builds a single prompt containing:
        - System instructions
        - Conversation history
        - Current user input
        """

        prompt = get_system_prompt() + "\n\n"

        for msg in session.messages:
            role = "USER" if msg.role == "user" else "ASSISTANT"
            prompt += f"{role}: {msg.content}\n"

        prompt += f"\nUSER: {user_message}\nASSISTANT:"
        return prompt

    def send_message(
        self,
        user_message: str,
        session: ChatSession,
    ) -> Tuple[str, int]:

        start_time = time.time()

        try:
            final_prompt = self._build_prompt(user_message, session)

            response = self.client.models.generate_content(
                model=self.model_name,
                contents=final_prompt,
                config=self.config,
            )

            elapsed = round(time.time() - start_time, 2)
            text = response.text or get_fallback_message()
            tokens = (
                response.usage_metadata.total_token_count
                if response.usage_metadata
                else 0
            )

            logger.info(
                f"Gemini response OK | elapsed={elapsed}s | tokens={tokens}"
            )

            return text.strip(), tokens

        except Exception:
            logger.exception("Gemini API call failed")
            return get_fallback_message(), 0


def get_gemini_client() -> GeminiClient:
    return GeminiClient()