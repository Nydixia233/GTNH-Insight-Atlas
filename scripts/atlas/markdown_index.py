from __future__ import annotations

import argparse
import json
from pathlib import Path

from scripts.atlas.markdown_utils import first_h1, read_markdown, title_from_path

AXES = [
    ("progression", "Progression"),
    ("topics", "Topics"),
    ("foundations", "Foundations"),
    ("reference", "Reference"),
]


def page_title(path: Path) -> str:
    metadata, markdown = read_markdown(path)
    return metadata.get("title") or first_h1(markdown) or title_from_path(path)


def vitepress_link(content_root: Path, path: Path) -> str:
    rel = path.relative_to(content_root)
    without_suffix = rel.with_suffix("").as_posix()
    if without_suffix.endswith("/index"):
        without_suffix = without_suffix[: -len("index")]
    return f"/{without_suffix}"


def build_axis_items(content_root: Path, axis: str) -> list[dict[str, str]]:
    axis_root = content_root / axis
    if not axis_root.exists():
        return []
    items: list[dict[str, str]] = []
    for path in sorted(axis_root.rglob("*.md")):
        items.append({"text": page_title(path), "link": vitepress_link(content_root, path)})
    return items


def build_markdown_index(root: Path) -> dict:
    content_root = root / "content"
    sidebar = [
        {"text": label, "items": build_axis_items(content_root, axis)}
        for axis, label in AXES
    ]
    search = []
    if content_root.exists():
        paths = sorted(
            content_root.rglob("*.md"),
            key=lambda item: (0 if item.relative_to(content_root).as_posix() == "index.md" else 1, item.as_posix()),
        )
        for path in paths:
            metadata, markdown = read_markdown(path)
            search.append(
                {
                    "title": metadata.get("title") or first_h1(markdown) or title_from_path(path),
                    "path": path.relative_to(content_root).as_posix(),
                    "link": vitepress_link(content_root, path),
                }
            )
    return {"sidebar": sidebar, "search": search}


def main() -> int:
    parser = argparse.ArgumentParser(description="Build VitePress sidebar/search metadata")
    parser.add_argument("--root", type=Path, default=Path(__file__).resolve().parents[2])
    parser.add_argument("--output", type=Path, default=None)
    args = parser.parse_args()
    root = args.root.resolve()
    output = args.output or (root / "generated" / "markdown-index.json")

    data = build_markdown_index(root)
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"wrote {output.relative_to(root).as_posix()}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
