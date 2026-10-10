import importlib
import io
import json
import tempfile
import unittest
from contextlib import redirect_stderr
from pathlib import Path
from unittest.mock import patch

import httpx

from app.errors import CodexExecutionError
from detailedAnalysis.technical_api import TechnicalConfig
from tests.technical_fixtures import synthetic

analysis = importlib.import_module("detailedAnalysis.main")


class DetailedAnalysisPipelineTests(unittest.TestCase):
    def run_pipeline(self, body=None, *, window="5dd", status=200, config=None,
                     codex_error=None, transport_error=None):
        directory = tempfile.TemporaryDirectory()
        self.addCleanup(directory.cleanup)
        instructions = Path(directory.name) / "instructions.md"
        strategy_path = analysis.PROJECT_DIR / "instructions" / (
            "stock-upside-analysis-5-instructions.md" if window == "5dd"
            else "stock-upside-analysis-10-instructions.md"
        )
        instructions.write_text(strategy_path.read_text())
        def handler(request):
            if transport_error:
                raise httpx.ConnectError("failed", request=request)
            if status == 200:
                return httpx.Response(200, json=body if body is not None else synthetic(window))
            return httpx.Response(status, json=body)
        http = httpx.Client(transport=httpx.MockTransport(handler))
        self.addCleanup(http.close)
        # Inject only HTTP; execute actual adapter, contract, and prompt.
        with patch("httpx.Client", return_value=http), patch.object(
            analysis, "run_codex", side_effect=codex_error
        ) as codex, redirect_stderr(io.StringIO()) as errors:
            result = analysis.main(
                " aali ", str(instructions), "5 trading sessions" if window == "5dd" else "10 trading sessions",
                "https://data.example.test", directory.name,
                forecast_type=window,
                technical_config=config if config is not None else TechnicalConfig(),
            )
        return result, codex, errors.getvalue()

    def test_both_horizons_use_documented_features_without_generated_context(self):
        for window in ("5dd", "10dd"):
            body = synthetic(window)
            result, codex, errors = self.run_pipeline(body, window=window)
            self.assertEqual(result, 0, errors)
            codex.assert_called_once()
            prompt, output, working_dir = codex.call_args.args
            self.assertEqual(output.name, "AALI.md")
            self.assertEqual(codex.call_args.kwargs, {"enable_search": True})
            self.assertEqual(prompt.count("<TECHNICAL_DATA_JSON>"), 1)
            encoded = prompt.split("<TECHNICAL_DATA_JSON>\n")[1].split("\n</TECHNICAL_DATA_JSON>")[0]
            self.assertEqual(json.loads(encoded), body)
            self.assertNotIn("\n", encoded)
            self.assertNotIn("<TRUSTED_FEATURE_DEFINITIONS_JSON>", prompt)
            self.assertNotIn("<CONSUMER_ASSESSMENT_JSON>", prompt)
            self.assertNotIn("Technical API v2 caller guidance (trusted)", prompt)
            self.assertIn("instructions/features/README.md", prompt)
            self.assertIn("instructions/features/INDEX.md", prompt)
            self.assertIn("read its matching card before interpreting it", prompt)

    def test_failures_prevent_codex_execution(self):
        cases = [({"detail":{"code":"insufficient_sessions","message":"unavailable","ticker":"AALI","forecast_type":"5dd"}},409,None),
                 ({"detail":{"code":"ohlcv_data_missing","message":"unavailable","ticker":"AALI","forecast_type":"5dd"}},409,None),
                 ({"schema_version":"1.0"},200,None)]
        for key in ("ohlcv", "ohlcv_metadata"):
            missing = synthetic()
            del missing[key]
            cases.append((missing, 200, None))
        unsupported_catalog = synthetic()
        unsupported_catalog["feature_catalog_version"] = "2.0"
        cases.append((unsupported_catalog,200,None))
        old = synthetic()
        old["quality"].update(request_date="2026-10-12",data_age_calendar_days=3)
        cases.append((old,200,TechnicalConfig(30,2)))
        mismatch = synthetic()
        mismatch["ticker"] = "BBCA"
        cases.append((mismatch,200,None))
        for body, status, config in cases:
            result, codex, errors = self.run_pipeline(body, status=status, config=config)
            self.assertEqual(result, 1)
            codex.assert_not_called()
            self.assertIn("Error:", errors)
        result, codex, errors = self.run_pipeline(transport_error=True)
        self.assertEqual(result, 1)
        codex.assert_not_called()
        self.assertIn("transport", errors)

    def test_codex_failure_does_not_claim_report_success(self):
        result, codex, errors = self.run_pipeline(codex_error=CodexExecutionError("failed"))
        self.assertEqual(result, 1)
        codex.assert_called_once()
        self.assertIn("failed", errors)

    def test_uncatalogued_feature_uses_documented_interpretation_limitations(self):
        body = synthetic()
        body["indicators"]["Unknown"] = body["indicators"].pop("RSI Value")
        result, codex, errors = self.run_pipeline(body)
        self.assertEqual(result, 0, errors)
        prompt = codex.call_args.args[0]
        encoded = prompt.split("<TECHNICAL_DATA_JSON>\n")[1].split("\n</TECHNICAL_DATA_JSON>")[0]
        self.assertEqual(json.loads(encoded), body)
        self.assertIn("explicit interpretation limitation", prompt)
