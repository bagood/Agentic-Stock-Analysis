import json
import unittest
from unittest.mock import patch

import httpx

from detailedAnalysis.technical_api import DOMAIN_STATUS, TechnicalAPIClient, TechnicalConfig
from detailedAnalysis.technical_errors import (
    TechnicalAPIError, TechnicalContractError, TechnicalFreshnessError,
    TechnicalInputError, TechnicalServiceError, TechnicalTransportError,
)
from tests.technical_fixtures import synthetic


class TechnicalClientTests(unittest.TestCase):
    def client(self, handler, config=None):
        http = httpx.Client(transport=httpx.MockTransport(handler))
        self.addCleanup(http.close)
        return TechnicalAPIClient("https://data.example.test/api?market=idx",
                                  config, client=http)

    def test_requests_each_horizon_and_retains_server_provenance(self):
        for window in ("5dd", "10dd"):
            body = synthetic(window)
            def handler(request):
                self.assertEqual(request.url.path, "/api/technical/")
                self.assertEqual(dict(request.url.params), {"market": "idx", "ticker": "AALI", "forecast_type": window})
                self.assertEqual(request.extensions["timeout"]["read"], 12)
                return httpx.Response(200, json=body)
            result = self.client(handler, TechnicalConfig(12)).retrieve(" aali ", window)
            self.assertEqual(result.model_dump(), body)
            self.assertEqual(result.quality.freshness_status, "unverified_without_exchange_calendar")

    def test_all_domain_errors_retain_status_reason_and_identity(self):
        for code, status in DOMAIN_STATUS.items():
            body = {"detail": {"code": code, "message": "safe message", "ticker": "AALI", "forecast_type": "5dd"}}
            with self.subTest(code=code), self.assertRaises(TechnicalAPIError) as failure:
                self.client(lambda request: httpx.Response(status, json=body)).retrieve("AALI", "5dd")
            self.assertEqual(failure.exception.status_code, status)
            self.assertEqual(failure.exception.reason_code, code)
            self.assertEqual(failure.exception.ticker, "AALI")
            self.assertNotIn("secret", str(failure.exception))

    def test_422_validation_list_is_distinct(self):
        body = {"detail": [{"type": "missing", "loc": ["query", "forecast_type"], "msg": "Field required", "input": "secret"}]}
        with self.assertRaises(TechnicalInputError) as failure:
            self.client(lambda request: httpx.Response(422, json=body)).retrieve("AALI", "5dd")
        self.assertEqual(failure.exception.status_code, 422)
        self.assertNotIn("input", failure.exception.validation_details[0])

    def test_unknown_http_errors_are_service_failures(self):
        cases = [(503, b"unavailable"), (500, b"{}"), (302, b"{}"),
                 (404, json.dumps({"detail":{"code":"new_code","message":"test","ticker":"AALI","forecast_type":"5dd"}}).encode()),
                 (409, json.dumps({"detail":{"code":"technical_data_missing","message":"test","ticker":"AALI","forecast_type":"5dd"}}).encode()),
                 (404, json.dumps({"detail":{"code":"technical_data_missing","message":"test","ticker":"BBCA","forecast_type":"5dd"}}).encode())]
        for status, content in cases:
            with self.subTest(status=status, content=content), self.assertRaises(TechnicalServiceError):
                self.client(lambda request: httpx.Response(status, content=content)).retrieve("AALI", "5dd")

    def test_malformed_legacy_and_wrong_identity_never_pass(self):
        cases = [b"not json", b"[]", b'{"dates":[]}', b'{"schema_version":"2.0","schema_version":"2.0"}',
                 b'{"indicators":{"a":[NaN,0,0]}}']
        for key, value in (("schema_version", "1.0"), ("schema_version", "2.0"), ("feature_catalog_version", "2.0"), ("ticker", "BBCA"), ("forecast_type", "10dd")):
            body = synthetic()
            body[key] = value
            cases.append(json.dumps(body).encode())
        for content in cases:
            with self.subTest(content=content[:60]), self.assertRaises(TechnicalContractError):
                self.client(lambda request: httpx.Response(200, content=content)).retrieve("AALI", "5dd")

    def test_transport_failures_are_explicit_without_retries(self):
        for error in (httpx.ReadTimeout, httpx.ConnectError):
            calls = []
            def handler(request):
                calls.append(request)
                raise error("message containing secret URL", request=request)
            with self.assertRaises(TechnicalTransportError) as failure:
                self.client(handler).retrieve("AALI", "5dd")
            self.assertEqual(len(calls), 1)
            self.assertNotIn("secret", str(failure.exception))

    def test_input_is_validated_before_request(self):
        for ticker, window in (("ABC", "5dd"), ("AB1D", "5dd"), ("AßB", "5dd"), ("AALI", "5")):
            with self.subTest(ticker=ticker), self.assertRaises(TechnicalInputError):
                self.client(lambda request: self.fail("unexpected HTTP")).retrieve(ticker, window)
        client = self.client(lambda request: self.fail("unexpected HTTP"))
        client.base_url = "https://data.example.test:invalid"
        with self.assertRaises(TechnicalInputError):
            client.retrieve("AALI", "5dd")

    def test_freshness_budget_is_separate_from_readiness(self):
        body = synthetic()
        body["quality"]["request_date"] = "2026-10-12"
        body["quality"]["data_age_calendar_days"] = 3
        handler = lambda request: httpx.Response(200, json=body)
        result = self.client(handler, TechnicalConfig(30, 3)).retrieve("AALI", "5dd")
        self.assertEqual(result.quality.data_age_calendar_days, 3)
        self.assertEqual(result.quality.freshness_status, "unverified_without_exchange_calendar")
        with self.assertRaises(TechnicalFreshnessError):
            self.client(handler, TechnicalConfig(30, 2)).retrieve("AALI", "5dd")

    def test_configuration_is_finite_and_strict(self):
        for timeout in (0, -1, float("nan"), float("inf"), True):
            with self.assertRaises(TechnicalInputError):
                TechnicalConfig(timeout)
        for age in (0, -1, True, 1.5):
            with self.assertRaises(TechnicalInputError):
                TechnicalConfig(30, age)
        with patch.dict("os.environ", {"TECHNICAL_API_TIMEOUT_SECONDS":"12.5", "TECHNICAL_MAX_DATA_AGE_CALENDAR_DAYS":"7"}, clear=True):
            self.assertEqual(TechnicalConfig.from_environment(), TechnicalConfig(12.5, 7))
        for value in ("", "1.5", "nan", "-1"):
            with patch.dict("os.environ", {"TECHNICAL_MAX_DATA_AGE_CALENDAR_DAYS":value}, clear=True), self.assertRaises(TechnicalInputError):
                TechnicalConfig.from_environment()
