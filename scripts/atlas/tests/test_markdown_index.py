from __future__ import annotations

from pathlib import Path

from scripts.atlas.markdown_index import build_markdown_index


def write(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")


def test_markdown_index_builds_sidebar_by_axis(tmp_path: Path) -> None:
    write(tmp_path / "content/index.md", "# Home\n")
    write(tmp_path / "content/topics/ebf/index.md", "# Electric Blast Furnace\n")
    write(tmp_path / "content/foundations/overclock.md", "# Overclock\n")
    write(tmp_path / "content/reference/voltage-tiers.md", "# Voltage Tiers\n")
    write(tmp_path / "content/progression/index.md", "# Progression\n")

    index = build_markdown_index(tmp_path)

    labels = [item["text"] for item in index["sidebar"]]
    assert labels == ["Progression", "Topics", "Foundations", "Reference"]
    assert index["search"][0]["title"] == "Home"
