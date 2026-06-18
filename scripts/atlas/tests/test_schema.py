from __future__ import annotations

import json
from copy import deepcopy
from pathlib import Path

from jsonschema import Draft202012Validator


ROOT = Path(__file__).resolve().parents[3]


def fact_schema() -> dict:
    return json.loads((ROOT / "data/schemas/fact.schema.json").read_text(encoding="utf-8"))


def valid_fact() -> dict:
    return {
        "id": "oc.duration-divisor-normal",
        "label": "Duration divisor per normal overclock",
        "value": 2,
        "unit": "multiplier",
        "source": [
            {
                "file": "gregtech/api/util/OverclockCalculator.java",
                "line": 35,
                "version": "5.09.52.594",
                "expect": "protected double durationDecreasePerOC = 2;",
            }
        ],
        "verification": {"status": "source-only", "method": "source-line"},
    }


def test_fact_schema_is_valid_json_schema() -> None:
    Draft202012Validator.check_schema(fact_schema())


def test_valid_fact_passes_schema() -> None:
    errors = list(Draft202012Validator(fact_schema()).iter_errors(valid_fact()))
    assert errors == []


def test_required_fact_fields_are_enforced() -> None:
    validator = Draft202012Validator(fact_schema())

    for field in ["value", "source", "verification"]:
        fact = valid_fact()
        fact.pop(field)
        assert list(validator.iter_errors(fact)), field


def test_source_version_is_locked() -> None:
    validator = Draft202012Validator(fact_schema())
    fact = valid_fact()
    fact["source"][0]["version"] = "5.09.52.525"

    errors = list(validator.iter_errors(fact))
    assert errors
    assert "5.09.52.594" in str(errors[0])


def test_source_line_must_be_positive_integer() -> None:
    validator = Draft202012Validator(fact_schema())
    fact = deepcopy(valid_fact())
    fact["source"][0]["line"] = 0

    assert list(validator.iter_errors(fact))
