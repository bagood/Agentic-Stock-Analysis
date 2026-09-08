import os
import tempfile
import unittest
from pathlib import Path

from app.errors import CodexExecutionError, CodexTimeoutError
from app.integrations.codex_runner import CodexRunner


class CodexRunnerTests(unittest.IsolatedAsyncioTestCase):
    def build_runner(self, executable: str, timeout: float = 2) -> CodexRunner:
        return CodexRunner(
            executable=executable,
            mcp_url="http://agentic-mcp:8000/mcp",
            timeout_seconds=timeout,
            max_concurrency=1,
            max_response_bytes=1000,
        )

    def test_command_is_ephemeral_read_only_and_uses_only_configured_mcp(
        self,
    ) -> None:
        runner = self.build_runner("codex")
        command = runner._command(Path("/tmp/reply.txt"))

        self.assertIn("--ephemeral", command)
        self.assertIn("--ignore-user-config", command)
        self.assertIn("--ignore-rules", command)
        self.assertIn("plugins", command)
        self.assertIn("read-only", command)
        self.assertIn('shell_environment_policy.inherit="none"', command)
        self.assertIn(
            "mcp_servers.agentic_stock_analysis.url="
            '"http://agentic-mcp:8000/mcp"',
            command,
        )
        self.assertEqual(command[-1], "-")

    async def test_returns_buffered_final_message(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            executable = Path(directory) / "fake-codex"
            executable.write_text(
                """#!/bin/sh
while [ "$#" -gt 0 ]; do
    if [ "$1" = "--output-last-message" ]; then
        shift
        printf 'final answer' > "$1"
        exit 0
    fi
    shift
done
exit 2
""",
                encoding="utf-8",
            )
            executable.chmod(0o755)

            reply = await self.build_runner(str(executable)).run("question")

        self.assertEqual(reply, "final answer")

    async def test_nonzero_exit_is_failure(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            executable = Path(directory) / "fake-codex"
            executable.write_text("#!/bin/sh\nexit 2\n", encoding="utf-8")
            executable.chmod(0o755)

            with self.assertRaises(CodexExecutionError):
                await self.build_runner(str(executable)).run("question")

    async def test_timeout_terminates_process(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            executable = Path(directory) / "fake-codex"
            executable.write_text("#!/bin/sh\nsleep 5\n", encoding="utf-8")
            executable.chmod(0o755)

            with self.assertRaises(CodexTimeoutError):
                await self.build_runner(str(executable), timeout=0.01).run(
                    "question"
                )

    def test_readiness_requires_executable(self) -> None:
        missing = str(Path(tempfile.gettempdir()) / "missing-chat-codex")
        self.assertFalse(os.path.exists(missing))
        self.assertFalse(self.build_runner(missing).is_ready())


if __name__ == "__main__":
    unittest.main()
