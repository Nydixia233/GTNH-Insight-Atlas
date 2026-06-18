from __future__ import annotations

from pathlib import Path

import pytest

from scripts.atlas.link_graph import build_link_graph


def write(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")


def test_link_graph_extracts_relative_and_fact_edges(tmp_path: Path) -> None:
    write(
        tmp_path / "content/topics/ebf/index.md",
        """# EBF

[Overclock](../../foundations/overclock.md)
[External](https://example.com)
<FactCard id="ebf.heat-gate" />
""",
    )
    write(tmp_path / "content/foundations/overclock.md", "# Overclock\n")

    graph = build_link_graph(tmp_path)

    assert {"from": "topics/ebf/index.md", "to": "foundations/overclock.md", "type": "doc"} in graph["edges"]
    assert {"from": "topics/ebf/index.md", "to": "ebf.heat-gate", "type": "fact"} in graph["edges"]
    assert all("example.com" not in edge["to"] for edge in graph["edges"])


def test_link_graph_marks_dangling_links(tmp_path: Path) -> None:
    write(tmp_path / "content/topics/ebf/index.md", "[Missing](missing.md)\n")

    graph = build_link_graph(tmp_path)

    assert graph["dangling"]
    assert graph["dangling"][0]["target"] == "topics/ebf/missing.md"


def test_link_graph_rejects_wikilinks(tmp_path: Path) -> None:
    write(tmp_path / "content/topics/ebf/index.md", "[[Forbidden]]\n")

    with pytest.raises(ValueError, match="wikilink"):
        build_link_graph(tmp_path)
