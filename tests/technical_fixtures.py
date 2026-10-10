import copy
import json
from pathlib import Path

FIXTURES = Path(__file__).parent / "fixtures"


def supplied(window="5dd"):
    return json.loads((FIXTURES / f"technical_aali_{window}_v2.json").read_text())


def synthetic(window="5dd"):
    """Synthetic edge-case values; never represented as a real backend snapshot."""
    body = copy.deepcopy(supplied(window))
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
