from __future__ import annotations

from pathlib import Path

from scripts.atlas.source_refs import check_source_entries, find_source_refs


def test_source_ref_regex_matches_source_references() -> None:
    text = "See gregtech/api/util/OverclockCalculator.java:35 for the divisor."

    assert find_source_refs(text) == ["gregtech/api/util/OverclockCalculator.java:35"]


def test_source_ref_regex_ignores_href_values() -> None:
    text = '<a href="gregtech/api/util/OverclockCalculator.java:35">source</a>'

    assert find_source_refs(text) == []


def test_source_entries_verify_expected_line(tmp_path: Path) -> None:
    src = tmp_path / "src"
    src.mkdir()
    java_file = src / "Example.java"
    java_file.write_text("first\nprotected double durationDecreasePerOC = 2;\n", encoding="utf-8")
    entry = {
        "file": "Example.java",
        "line": 2,
        "version": "5.09.52.594",
        "expect": "durationDecreasePerOC = 2",
    }

    assert check_source_entries([entry], src, strict=True) == []


def test_source_entries_report_content_drift(tmp_path: Path) -> None:
    src = tmp_path / "src"
    src.mkdir()
    java_file = src / "Example.java"
    java_file.write_text("first\nprotected double durationDecreasePerOC = 3;\n", encoding="utf-8")
    entry = {
        "file": "Example.java",
        "line": 2,
        "version": "5.09.52.594",
        "expect": "durationDecreasePerOC = 2",
    }

    errors = check_source_entries([entry], src, strict=True)

    assert errors
    assert "expected snippet not found" in errors[0].message


def test_missing_source_warns_without_strict(tmp_path: Path) -> None:
    entry = {
        "file": "Missing.java",
        "line": 1,
        "version": "5.09.52.594",
        "expect": "anything",
    }

    messages = check_source_entries([entry], tmp_path, strict=False)

    assert messages
    assert messages[0].severity == "warning"
