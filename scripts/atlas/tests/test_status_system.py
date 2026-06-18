from __future__ import annotations

from scripts.atlas import STATUS_MAP, status_for


def test_status_to_emoji_mapping() -> None:
    assert status_for("verified").emoji == "🟢"
    assert status_for("source-only").emoji == "🔵"
    assert status_for("pending").emoji == "🟡"
    assert status_for("contradicted").emoji == "🔴"


def test_status_map_contains_all_schema_statuses() -> None:
    assert set(STATUS_MAP) == {"verified", "source-only", "pending", "contradicted"}
