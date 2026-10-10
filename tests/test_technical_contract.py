import unittest

from pydantic import ValidationError

from detailedAnalysis.technical_contract import TechnicalResponse
from tests.technical_fixtures import supplied, synthetic


class TechnicalContractTests(unittest.TestCase):
    def test_complete_supplied_fixtures_survive_validation(self):
        for window, count in (("5dd", 180), ("10dd", 193)):
            body = supplied(window)
            result = TechnicalResponse.model_validate(body)
            self.assertEqual(result.model_dump(), body)
            self.assertEqual(len(result.indicators), count)
            self.assertEqual(result.quality.null_counts_by_session, [55 if window == "5dd" else 57] * 3)
            self.assertEqual(result.quality.data_age_calendar_days, 1)
        self.assertLessEqual(supplied()["indicators"].keys(), supplied("10dd")["indicators"].keys())

    def test_zero_null_flags_precision_and_reversals_are_preserved(self):
        body = synthetic()
        result = TechnicalResponse.model_validate(body)
        self.assertEqual(result.model_dump(), body)
        self.assertIs(type(result.indicators["ATR Bearish"][0]), int)
        self.assertEqual(result.indicators["RSI Value"], [50, 55, 53])
        self.assertIsNone(result.indicators["MACD Percent"][1])

    def test_invalid_envelopes_fail(self):
        changes = [
            ("schema_version", "1.0"), ("feature_catalog_version", "2.0"), ("requested_sessions", 2),
            ("returned_sessions", 3.0), ("order", "newest_to_oldest"),
            ("market_timezone", "UTC"), ("selection_policy", "today"),
            ("dates", ["2026-10-07", "2026-10-07", "2026-10-09"]),
            ("dates", ["2026-10-09", "2026-10-08", "2026-10-07"]),
            ("dates", ["2026-02-30", "2026-10-08", "2026-10-09"]),
            ("data_as_of", "2026-10-08"), ("indicators", {}),
            ("ticker", "ABC"), ("forecast_type", "20dd"), ("extra", 1),
        ]
        for key, value in changes:
            with self.subTest(key=key, value=value):
                body = synthetic()
                body[key] = value
                with self.assertRaises(ValidationError):
                    TechnicalResponse.model_validate(body)
        for key in synthetic():
            with self.subTest(missing=key):
                body = synthetic()
                del body[key]
                with self.assertRaises(ValidationError):
                    TechnicalResponse.model_validate(body)

    def test_quality_and_provenance_cross_checks(self):
        changes = [
            ("quality", "request_date", "2026-10-09"),
            ("quality", "data_age_calendar_days", 2),
            ("quality", "freshness_status", "current"),
            ("quality", "null_counts_by_session", [0, 0, 0]),
            ("quality", "null_counts_by_session", [True, 2, 1]),
            ("feature_filter", "included_count", 3),
            ("feature_filter", "selected_union_count", 4),
            ("feature_filter", "excluded_not_selected_count", -1),
            ("feature_filter", "model_version", True),
            ("feature_filter", "strategy", "intersection"),
            ("feature_filter", "sources", synthetic()["feature_filter"]["sources"][::-1]),
            ("feature_filter", "sources", supplied("10dd")["feature_filter"]["sources"]),
        ]
        for block, key, value in changes:
            with self.subTest(block=block, key=key):
                body = synthetic()
                body[block][key] = value
                with self.assertRaises(ValidationError):
                    TechnicalResponse.model_validate(body)

    def test_bad_numeric_values_names_and_lengths_fail(self):
        for value in (True, "50", float("nan"), float("inf"), -float("inf")):
            body = synthetic()
            body["indicators"]["RSI Value"][0] = value
            with self.subTest(value=value), self.assertRaises(ValidationError):
                TechnicalResponse.model_validate(body)
        for name in ("", " RSI Value", "Date"):
            body = synthetic()
            body["indicators"][name] = body["indicators"].pop("RSI Value")
            with self.subTest(name=name), self.assertRaises(ValidationError):
                TechnicalResponse.model_validate(body)
        for values in ([50, 55], [50, 55, 53, 52]):
            body = synthetic()
            body["indicators"]["RSI Value"] = values
            with self.assertRaises(ValidationError):
                TechnicalResponse.model_validate(body)

    def test_observed_gaps_are_allowed(self):
        body = synthetic()
        body["dates"][0] = "2026-10-02"
        self.assertEqual(TechnicalResponse.model_validate(body).dates[0], "2026-10-02")
