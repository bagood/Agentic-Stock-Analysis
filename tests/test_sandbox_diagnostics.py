import os
import subprocess
import unittest
from unittest.mock import patch

from detailedAnalysis.sandbox_diagnostics import collect_diagnostics, main


class SandboxDiagnosticsTests(unittest.TestCase):
    def test_mount_denial_is_visible_without_credentials_or_model_call(self):
        with patch.dict(os.environ, {"CODEX_API_KEY": "secret", "OPENAI_API_KEY": "secret"}), patch(
            "detailedAnalysis.sandbox_diagnostics.shutil.which", return_value="/bin/tool"
        ), patch("detailedAnalysis.sandbox_diagnostics.subprocess.run", return_value=
            subprocess.CompletedProcess([], 1, b"", b"bwrap: Failed to make / slave: Permission denied")
        ) as capture:
            report = collect_diagnostics()
        self.assertIn("Failed to make / slave", report["probes"][-1]["stderr"])
        for call in capture.call_args_list:
            self.assertNotIn("CODEX_API_KEY", call.kwargs["env"])
            self.assertNotIn("OPENAI_API_KEY", call.kwargs["env"])
            self.assertNotIn("exec", call.args[0])
        self.assertEqual(capture.call_args_list[-1].args[0][-1], "/bin/true")

    def test_missing_codex_returns_failure_and_keeps_other_probe_results(self):
        with patch("detailedAnalysis.sandbox_diagnostics.shutil.which", return_value=None), patch(
            "builtins.print"
        ) as output:
            self.assertEqual(main(), 1)
        self.assertIn("executable not found", output.call_args.args[0])
