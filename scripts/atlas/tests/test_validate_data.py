from __future__ import annotations

from pathlib import Path

import yaml

from scripts.atlas.validate_data import validate_all, validate_fact_documents


ROOT = Path(__file__).resolve().parents[3]


def test_repository_facts_validate() -> None:
    assert validate_all(ROOT) == []


def test_validate_fact_documents_reports_missing_required_field() -> None:
    fact = {
        "id": "broken.fact",
        "label": "Broken fact",
        "unit": "count",
        "source": [{"file": "Example.java", "line": 1, "version": "5.09.52.594"}],
        "verification": {"status": "pending", "method": "fixture"},
    }

    errors = validate_fact_documents({"fixture.yml": [fact]}, ROOT)

    assert errors
    assert "value" in errors[0].message


def test_validate_fact_documents_reports_duplicate_ids() -> None:
    source = ROOT / "data/mechanics/overclock.yml"
    facts = yaml.safe_load(source.read_text(encoding="utf-8"))
    duplicated = [facts[0], dict(facts[0])]

    errors = validate_fact_documents({"duplicate.yml": duplicated}, ROOT)

    assert any("duplicate fact id" in error.message for error in errors)
