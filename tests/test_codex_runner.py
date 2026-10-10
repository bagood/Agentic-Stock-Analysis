import os
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from app.errors import CodexExecutionError, CodexTimeoutError
from llm_runner.codex_runner import CodexRunner, run_codex


class SynchronousCodexRunnerTests(unittest.TestCase):
    def run_fake(self, script, *, timeout=2, search=False):
        directory = tempfile.TemporaryDirectory()
        self.addCleanup(directory.cleanup)
        root = Path(directory.name)
        executable = root / "fake-codex"
        executable.write_text("#!/usr/bin/env python3\nimport sys,json,time,os\n"
                              "args=sys.argv[1:]\noutput=args[args.index('-o')+1]\n" + script)
        executable.chmod(0o755)
        output = root / "report.md"
        output.write_text("previous report")
        self.output, self.root = output, root
        return run_codex("secret prompt", output, root, executable=str(executable),
                         timeout_seconds=timeout, enable_search=search)

    def test_healthy_run_is_isolated_and_publishes(self):
        self.run_fake("""assert '--ignore-user-config' in args
assert '--json' in args and '--search' in args
assert args[args.index('--model')+1] == 'gpt-5.6-sol'
assert 'approval_policy="never"' in args
assert '--disable' in args and 'plugins' in args
open(output,'w').write('final report')
print(json.dumps({'type':'turn.completed'}))
""", search=True)
        self.assertEqual(self.output.read_text(), 'final report')
        self.assertEqual(list(self.root.glob('.*.tmp')), [])

    def test_failed_generation_preserves_old_report_and_cleans_temporary(self):
        for script in (
            "print(json.dumps({'type':'turn.completed'}))\n",
            "open(output,'w').write(' ')\nprint(json.dumps({'type':'turn.completed'}))\n",
            "open(output,'w').write('fallback')\nprint('bwrap: No permissions to create a new namespace',file=sys.stderr)\nprint(json.dumps({'type':'turn.completed'}))\n",
            "open(output,'w').write('fallback')\nprint(json.dumps({'type':'turn.failed','error':{'message':'failed'}}))\n",
            "open(output,'w').write('partial')\ntime.sleep(5)\n",
            "sys.exit(2)\n",
        ):
            with self.subTest(script=script), self.assertRaises(CodexExecutionError):
                self.run_fake(script, timeout=.1)
            self.assertEqual(self.output.read_text(), 'previous report')
            self.assertEqual(list(self.root.glob('.*.tmp')), [])

    def test_shell_failure_can_recover_but_unrecovered_infrastructure_cannot(self):
        for recover in (False, True):
            script = """item={'id':'1','type':'command_execution','command':'cat reference','status':'failed','exit_code':1,'aggregated_output':'bwrap: No permissions to create a new namespace'}
print(json.dumps({'type':'item.completed','item':item}))
"""
            if recover:
                script += "item.update(status='completed',exit_code=0,aggregated_output='reference')\nprint(json.dumps({'type':'item.completed','item':item}))\n"
            script += "open(output,'w').write('report')\nprint(json.dumps({'type':'turn.completed'}))\n"
            if recover:
                self.run_fake(script)
            else:
                with self.assertRaises(CodexExecutionError):
                    self.run_fake(script)

    def test_stale_user_config_is_ignored_and_auth_home_preserved(self):
        with tempfile.TemporaryDirectory() as directory:
            home = Path(directory)
            (home/'config.toml').write_text('[mcp_servers.stale]\nurl="http://localhost:1/mcp"')
            (home/'auth.json').write_text('synthetic-credential')
            with patch.dict(os.environ, {'CODEX_HOME':str(home)}):
                self.run_fake("""assert '--ignore-user-config' in args
assert open(os.path.join(os.environ['CODEX_HOME'],'auth.json')).read() == 'synthetic-credential'
open(output,'w').write('report')
print(json.dumps({'type':'turn.completed'}))
""")
            self.assertTrue((home/'config.toml').exists())

    def test_ordinary_nonzero_shell_exit_is_not_infrastructure_failure(self):
        self.run_fake("""print(json.dumps({'type':'item.completed','item':{'type':'command_execution','command':'rg optional','exit_code':1,'status':'failed','aggregated_output':''}}))
open(output,'w').write('report')
print(json.dumps({'type':'turn.completed'}))
""")


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
