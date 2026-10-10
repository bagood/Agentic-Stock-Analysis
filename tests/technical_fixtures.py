import copy
import json
from pathlib import Path

FIXTURES = Path(__file__).parent / "fixtures"


def supplied(window="5dd"):
    return json.loads((FIXTURES / f"technical_aali_{window}_v2.json").read_text())


def schema_21(window="5dd"):
    """Legacy indicator snapshot plus synthetic OHLCV, not a live 2.1 snapshot."""
    body = copy.deepcopy(supplied(window))
    body["schema_version"] = "2.1"
    body["ohlcv"] = {
        "open": [7000, 7050, 7100],
        "high": [7100, 7150, 7200],
        "low": [6950, 7000, 7050],
        "close": [7050, 7100, 7150],
        "volume": [0, 1300000, None],
    }
    body["ohlcv_metadata"] = {
        "source": "technical_csv", "price_currency": "unknown",
        "volume_unit": "unknown", "price_adjustment": "unknown",
    }
    body["quality"]["ohlcv_null_counts_by_session"] = [0, 0, 1]
    return body


def synthetic(window="5dd"):
    """Synthetic edge-case values; never represented as a real backend snapshot."""
    body = schema_21(window)
    body["indicators"] = {
        "RSI Value": [50, 55, 53],
        "ATR Bearish": [0, 0, 0],
        "Foreign Net Intensity 1D": [None, None, None],
        "MACD Percent": [0.02, None, 0.030000000000000002],
    }
    body["quality"]["null_counts_by_session"] = [1, 2, 1]
    body["feature_filter"].update(included_count=4, selected_union_count=5,
                                   selected_unavailable_count=1, excluded_not_selected_count=2)
    return body
