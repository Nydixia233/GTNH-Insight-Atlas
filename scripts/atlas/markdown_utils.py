from __future__ import annotations

import re
from pathlib import Path
from typing import Any

import yaml

FRONTMATTER_RE = re.compile(r"\A---\s*\n(.*?)\n---\s*\n", re.DOTALL)
H1_RE = re.compile(r"^#\s+(.+)$", re.MULTILINE)


def read_markdown(path: Path) -> tuple[dict[str, Any], str]:
    text = path.read_text(encoding="utf-8")
    match = FRONTMATTER_RE.match(text)
    if not match:
        return {}, text
    metadata = yaml.safe_load(match.group(1)) or {}
    return metadata, text[match.end() :]


def first_h1(markdown: str) -> str:
    match = H1_RE.search(markdown)
    return match.group(1).strip() if match else ""


def title_from_path(path: Path) -> str:
    if path.name == "index.md" and path.parent.name == "content":
        stem = "home"
    else:
        stem = path.parent.name if path.name == "index.md" else path.stem
    return stem.replace("-", " ").title()
