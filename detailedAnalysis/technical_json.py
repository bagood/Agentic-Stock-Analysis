"""Strict JSON decoding: reject nonstandard constants and duplicate keys."""
import json


def _constant(value):
    raise ValueError("Nonstandard JSON constant")


def _object(pairs):
    result = {}
    for key, value in pairs:
        if key in result:
            raise ValueError("Duplicate JSON key")
        result[key] = value
    return result


def load_json(body: str | bytes):
    return json.loads(body, parse_constant=_constant, object_pairs_hook=_object)
