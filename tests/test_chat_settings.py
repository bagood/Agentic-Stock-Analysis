import os
import unittest
from unittest.mock import patch

from app.settings import ChatSettings


class ChatSettingsTests(unittest.TestCase):
    def test_loads_defaults(self) -> None:
        names = [
            "ORGANIZER_BASE_URL",
            "CHAT_MCP_URL",
            "CHAT_CODEX_EXECUTABLE",
            "CHAT_CODEX_TIMEOUT_SECONDS",
            "CHAT_ORGANIZER_TIMEOUT_SECONDS",
            "CHAT_ORGANIZER_RETRY_ATTEMPTS",
            "CHAT_ORGANIZER_RETRY_BACKOFF_SECONDS",
            "CHAT_MAX_CONCURRENCY",
            "CHAT_MAX_MESSAGE_CHARS",
            "CHAT_MAX_RESPONSE_BYTES",
        ]
        environment = {
            key: value for key, value in os.environ.items() if key not in names
        }
        with patch.dict(os.environ, environment, clear=True):
            settings = ChatSettings.from_env()

        self.assertEqual(settings.organizer_base_url, "http://localhost:8001")
        self.assertEqual(settings.mcp_url, "http://localhost:8004/mcp")
        self.assertEqual(settings.max_concurrency, 2)
        self.assertEqual(settings.organizer_retry_attempts, 3)
        self.assertEqual(settings.organizer_retry_backoff_seconds, 0.1)

    def test_rejects_invalid_url_and_nonpositive_limit(self) -> None:
        with (
            patch.dict(os.environ, {"CHAT_MCP_URL": "not-a-url"}, clear=True),
            self.assertRaisesRegex(ValueError, "CHAT_MCP_URL"),
        ):
            ChatSettings.from_env()

        with (
            patch.dict(
                os.environ,
                {"CHAT_MAX_CONCURRENCY": "0"},
                clear=True,
            ),
            self.assertRaisesRegex(ValueError, "CHAT_MAX_CONCURRENCY"),
        ):
            ChatSettings.from_env()

        with (
            patch.dict(
                os.environ,
                {"CHAT_ORGANIZER_RETRY_ATTEMPTS": "0"},
                clear=True,
            ),
            self.assertRaisesRegex(ValueError, "CHAT_ORGANIZER_RETRY_ATTEMPTS"),
        ):
            ChatSettings.from_env()


if __name__ == "__main__":
    unittest.main()
