"""
gemini_client.py
----------------
Handles all communication with the Google Gemini API.
This module is completely decoupled from the UI — it knows nothing about Streamlit.
All API logic, error handling, retries, and logging live here.
"""

import time
from typing import Optional, Tuple
import google.generativeai as genai
from google.api_core import exceptions as google_exceptions

from config import config
from prompt_manager import get_system_prompt, get_fallback_message
from chat_manager import ChatSession
from logger import get_logger

logger = get_logger(__name__)


class GeminiClient:
    """
    Wrapper around the Google Gemini API.
    Handles initialization, request formatting, response parsing, and error handling.
    """

    def __init__(self):
        """Initializes the Gemini client with API credentials and model config."""
        try:
            genai.configure(api_key=config.gemini_api_key)

            # Generation config controls response behavior
            self.generation_config = genai.types.GenerationConfig(
                max_output_tokens=config.max_output_tokens,
                temperature=config.temperature,
            )

            # Safety settings — balanced for career advice context
            self.safety_settings = [
                {"category": "HARM_CATEGORY_HARASSMENT", "threshold": "BLOCK_MEDIUM_AND_ABOVE"},
                {"category": "HARM_CATEGORY_HATE_SPEECH", "threshold": "BLOCK_MEDIUM_AND_ABOVE"},
                {"category": "HARM_CATEGORY_SEXUALLY_EXPLICIT", "threshold": "BLOCK_MEDIUM_AND_ABOVE"},
                {"category": "HARM_CATEGORY_DANGEROUS_CONTENT", "threshold": "BLOCK_MEDIUM_AND_ABOVE"},
            ]

            # Initialize the generative model with system instruction
            self.model = genai.GenerativeModel(
                model_name=config.model_name,
                generation_config=self.generation_config,
                safety_settings=self.safety_settings,
                system_instruction=get_system_prompt(),
            )

            logger.info(f"GeminiClient initialized | model={config.model_name}")

        except Exception as e:
            logger.error(f"Failed to initialize GeminiClient: {e}")
            raise

    def send_message(
        self,
        user_message: str,
        session: ChatSession,
    ) -> Tuple[str, int]:
        """
        Sends a user message to the Gemini API with full conversation context.

        Args:
            user_message: The latest message from the user.
            session: The current ChatSession containing conversation history.

        Returns:
            Tuple of (response_text: str, tokens_used: int)
            On failure, returns (fallback_message: str, 0)
        """
        start_time = time.time()
        logger.info(
            f"API call initiated | turn={session.total_user_messages + 1} | "
            f"message_length={len(user_message)} chars"
        )

        try:
            # Build history excluding the current user message
            # (the current message is sent separately via send_message)
            history = session.get_history_for_api()

            # Start a chat session with existing history
            chat = self.model.start_chat(history=history)

            # Send the new user message
            response = chat.send_message(user_message)

            # Extract response text
            response_text = self._extract_response_text(response)

            # Calculate token usage
            tokens_used = self._extract_token_count(response)

            elapsed = round(time.time() - start_time, 2)
            logger.info(
                f"API call successful | elapsed={elapsed}s | "
                f"tokens_used={tokens_used} | "
                f"response_length={len(response_text)} chars"
            )

            return response_text, tokens_used

        except google_exceptions.InvalidArgument as e:
            logger.error(f"Invalid API argument: {e}")
            return (
                "⚠️ There was an issue with the request format. "
                "Please try rephrasing your message.",
                0,
            )

        except google_exceptions.ResourceExhausted as e:
            logger.error(f"API quota exceeded: {e}")
            return (
                "⚠️ I've hit my API usage limit for now. "
                "Please wait a moment and try again, or check your API quota.",
                0,
            )

        except google_exceptions.PermissionDenied as e:
            logger.error(f"API permission denied (check API key): {e}")
            return (
                "⚠️ There's an authentication issue with the API key. "
                "Please verify your GEMINI_API_KEY in the .env file.",
                0,
            )

        except google_exceptions.ServiceUnavailable as e:
            logger.error(f"Gemini API service unavailable: {e}")
            return get_fallback_message(), 0

        except Exception as e:
            logger.error(f"Unexpected error during API call: {type(e).__name__}: {e}")
            return get_fallback_message(), 0

    def _extract_response_text(self, response) -> str:
        """
        Safely extracts text from the Gemini API response object.
        Handles edge cases like blocked content or empty responses.
        """
        try:
            # Check if response was blocked by safety filters
            if not response.candidates:
                logger.warning("Response has no candidates — possibly blocked by safety filters.")
                return (
                    "I wasn't able to generate a response for that message. "
                    "Could you try rephrasing it?"
                )

            candidate = response.candidates[0]

            # Check finish reason
            finish_reason = str(candidate.finish_reason)
            if "SAFETY" in finish_reason:
                logger.warning(f"Response blocked by safety filters. Finish reason: {finish_reason}")
                return (
                    "I'm not able to respond to that particular message. "
                    "Please try asking something else about your career!"
                )

            # Extract text
            if candidate.content and candidate.content.parts:
                return candidate.content.parts[0].text

            logger.warning("Response candidate has no content parts.")
            return "I didn't generate a response. Please try again."

        except Exception as e:
            logger.error(f"Error extracting response text: {e}")
            return get_fallback_message()

    def _extract_token_count(self, response) -> int:
        """
        Extracts total token usage from the API response for monitoring.
        Returns 0 if token data is unavailable.
        """
        try:
            if hasattr(response, "usage_metadata") and response.usage_metadata:
                return response.usage_metadata.total_token_count or 0
        except Exception:
            pass
        return 0

    def health_check(self) -> bool:
        """
        Sends a lightweight test message to verify the API connection is working.
        Used on app startup to catch misconfigurations early.

        Returns:
            bool: True if API is reachable, False otherwise.
        """
        try:
            test_chat = self.model.start_chat(history=[])
            test_response = test_chat.send_message(
                "Respond with exactly one word: Ready"
            )
            self._extract_response_text(test_response)
            logger.info("Gemini API health check passed.")
            return True
        except Exception as e:
            logger.error(f"Gemini API health check failed: {e}")
            return False


# ---------------------------------------------------------------------------
# Module-level singleton — shared across the Streamlit session
# ---------------------------------------------------------------------------

def get_gemini_client() -> GeminiClient:
    """
    Returns a GeminiClient instance.
    Called from the UI layer — keeps instantiation logic here, not in app.py.
    """
    return GeminiClient()
