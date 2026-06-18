from __future__ import annotations

import argparse
import json
import re
from pathlib import Path

from scripts.atlas import SOURCE_REF_RE

MARKDOWN_LINK_RE = re.compile(r"(?<!!)\[([^\]]+)\]\(([^)]+)\)")
FACT_CARD_RE = re.compile(r"<FactCard\s+[^>]*id=[\"']([^\"']+)[\"'][^>]*/?>")
WIKILINK_RE = re.compile(r"\[\[[^\]]+\]\]")


def normalize_target(current: Path, target: str) -> str:
    target = target.split("#", 1)[0]
    raw = (current.parent / target).as_posix()
    parts: list[str] = []
    for part in raw.split("/"):
        if part in ("", "."):
            continue
        if part == "..":
            if parts:
                parts.pop()
            continue
        parts.append(part)
    normalized = "/".join(parts)
    if not normalized.endswith(".md"):
        normalized = f"{normalized.rstrip('/')}/index.md"
    return normalized


def build_link_graph(root: Path) -> dict:
    content_root = root / "content"
    files = sorted(path.relative_to(content_root) for path in content_root.rglob("*.md"))
    file_ids = {path.as_posix() for path in files}
    nodes = [
        {
            "id": path.as_posix(),
            "type": "doc",
            "axis": path.parts[0] if len(path.parts) > 1 else "home",
        }
        for path in files
    ]
    edges: list[dict[str, str]] = []
    dangling: list[dict[str, str]] = []

    for rel in files:
        text = (content_root / rel).read_text(encoding="utf-8")
        source_id = rel.as_posix()
        if WIKILINK_RE.search(text):
            raise ValueError(f"wikilink is forbidden in {source_id}")

        for _, target in MARKDOWN_LINK_RE.findall(text):
            if target.startswith(("http://", "https://", "#", "mailto:")):
                continue
            normalized = normalize_target(rel, target)
            if normalized in file_ids:
                edges.append({"from": source_id, "to": normalized, "type": "doc"})
            else:
                dangling.append({"from": source_id, "target": normalized})

        for fact_id in FACT_CARD_RE.findall(text):
            edges.append({"from": source_id, "to": fact_id, "type": "fact"})
            nodes.append({"id": fact_id, "type": "fact", "axis": "fact"})

        for source_ref in SOURCE_REF_RE.findall(re.sub(r"\]\([^)]+\)", "]()", text)):
            edges.append({"from": source_id, "to": source_ref, "type": "source"})
            nodes.append({"id": source_ref, "type": "source", "axis": "source"})

    deduped_nodes = list({node["id"]: node for node in nodes}.values())
    deduped_edges = list({(edge["from"], edge["to"], edge["type"]): edge for edge in edges}.values())
    return {"nodes": deduped_nodes, "edges": deduped_edges, "dangling": dangling}


def main() -> int:
    parser = argparse.ArgumentParser(description="Build Atlas link graph")
    parser.add_argument("--root", type=Path, default=Path(__file__).resolve().parents[2])
    parser.add_argument("--output", type=Path, default=None)
    args = parser.parse_args()
    root = args.root.resolve()
    output = args.output or (root / "generated" / "link-graph.json")

    data = build_link_graph(root)
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"wrote {output.relative_to(root).as_posix()}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
