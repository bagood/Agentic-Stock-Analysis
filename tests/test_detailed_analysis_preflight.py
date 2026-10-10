import importlib
import io
import os
import tempfile
import unittest
from contextlib import redirect_stderr
from pathlib import Path
from unittest.mock import patch

from app.errors import CodexExecutionError
from detailedAnalysis.preflight import check_feature_cards, preflight
from tests.technical_fixtures import synthetic

batch = importlib.import_module('run_detailed_analysis')
analysis = importlib.import_module('detailedAnalysis.main')


class PreflightTests(unittest.TestCase):
    def test_blocked_batch_preserves_reports_before_any_request(self):
        for window in ('5', '10'):
            with tempfile.TemporaryDirectory() as directory:
                report = Path(directory) / f'{window}dd' / 'KEEP.md'
                report.parent.mkdir()
                report.write_bytes(b'previous\x00report')
                with patch.dict(os.environ, {'DETAILED_ANALYSIS_RESULT':directory}, clear=False), patch.object(
                    batch, 'load_env'
                ), patch.object(batch, 'preflight', side_effect=CodexExecutionError('namespace denied')), patch.object(
                    batch, 'fetch_json'
                ) as fetch, patch.object(batch, 'prepare_output_dir') as prepare, patch.object(
                    batch, 'run_detailed_analysis'
                ) as generate, redirect_stderr(io.StringIO()) as error:
                    self.assertEqual(batch.main(window), 1)
                fetch.assert_not_called()
                prepare.assert_not_called()
                generate.assert_not_called()
                self.assertEqual(report.read_bytes(), b'previous\x00report')
                self.assertIn('namespace denied', error.getvalue())

    def test_direct_call_preflights_before_technical_api(self):
        with patch.object(analysis, 'preflight', side_effect=CodexExecutionError('blocked')), patch.object(
            analysis, 'TechnicalAPIClient'
        ) as client, patch.object(analysis, 'run_codex') as codex, redirect_stderr(io.StringIO()):
            self.assertEqual(analysis.main('AALI', 'instructions/stock-upside-analysis-5-instructions.md',
                '5 trading sessions', 'http://unused', '/tmp/unused', forecast_type='5dd'), 1)
        client.assert_not_called()
        codex.assert_not_called()

    def test_smoke_command_uses_sandbox_and_does_not_generate(self):
        project = analysis.PROJECT_DIR
        instructions = project / 'instructions/stock-upside-analysis-5-instructions.md'
        with patch('detailedAnalysis.preflight.shutil.which', return_value='/bin/codex'), patch(
            'detailedAnalysis.preflight.capture', return_value=(0, '', '')
        ) as capture:
            checked = preflight(project, instructions)
        command = capture.call_args.args[0]
        self.assertEqual(command[:2], ['codex', 'sandbox'])
        self.assertIn(str(project / 'instructions/features/INDEX.md'), command)
        self.assertNotIn('exec', command)
        self.assertEqual(checked.instructions, instructions)

    def test_missing_card_blocks_known_feature_but_unknown_remains_allowed(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            (root / 'instructions/features').mkdir(parents=True)
            (root / 'instructions/technical_feature_catalog_v1.json').write_text('{"features":{"RSI Value":{}}}')
            (root / 'instructions/features/INDEX.md').write_text('- [RSI Value](rsi-value.md)\n')
            check_feature_cards(root, {'Unknown': []})
            with self.assertRaises(CodexExecutionError):
                check_feature_cards(root, {'RSI Value': []})

    def test_project_config_is_rejected_before_process_start(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            (root / '.codex').mkdir()
            (root / '.codex/config.toml').write_text('[mcp_servers.stale]\nurl="http://localhost:1/mcp"')
            with patch('detailedAnalysis.preflight.capture') as capture, self.assertRaises(CodexExecutionError):
                preflight(root, root/'instructions.md')
            capture.assert_not_called()
