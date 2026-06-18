from __future__ import annotations

from pathlib import Path

import pytest

from scripts.atlas.extract_site_data import extract_site_data


def write(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")


def test_extract_site_data_outputs_facts_and_pages(tmp_path: Path) -> None:
    write(
        tmp_path / "data/mechanics/example.yml",
        """
- id: example.fact
  label: Example Fact
  value: 4
  unit: count
  source:
    - file: Example.java
      line: 2
      version: 5.09.52.594
  verification:
    status: source-only
    method: fixture
""",
    )
    write(
        tmp_path / "content/foundations/example.md",
        """---
title: Frontmatter Title
slug: example
axis: foundation
status: source-only
version_anchor: GTNH 2.9.0-beta-1
source_version: GT5-Unofficial 5.09.52.594
sources: []
---
# Heading Title

See Example.java:2.
<FactCard id="example.fact" />
""",
    )

    data = extract_site_data(tmp_path)

    assert data["facts"][0]["id"] == "example.fact"
    assert data["pages"][0]["title"] == "Frontmatter Title"
    assert data["pages"][0]["source_ref_count"] == 1


def test_extract_site_data_rejects_unknown_fact_reference(tmp_path: Path) -> None:
    write(tmp_path / "data/mechanics/example.yml", "[]\n")
    write(
        tmp_path / "content/foundations/example.md",
        """# Example

<FactCard id="missing.fact" />
""",
    )

    with pytest.raises(ValueError, match="undefined fact id"):
        extract_site_data(tmp_path)
