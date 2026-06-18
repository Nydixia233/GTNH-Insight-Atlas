from __future__ import annotations

import argparse
import json
import re
from pathlib import Path
from typing import Any

from scripts.atlas import SOURCE_REF_RE, STATUS_MAP
from scripts.atlas.markdown_utils import first_h1, read_markdown, title_from_path
from scripts.atlas.validate_data import load_fact_documents

FACT_CARD_RE = re.compile(r"<FactCard\s+[^>]*id=[\"']([^\"']+)[\"'][^>]*/?>")


def flatten_facts(root: Path) -> list[dict[str, Any]]:
    facts: list[dict[str, Any]] = []
    seen: set[str] = set()
    for document, document_facts in load_fact_documents(root).items():
        for fact in document_facts:
            fact_id = fact["id"]
            if fact_id in seen:
                raise ValueError(f"duplicate fact id: {fact_id}")
            seen.add(fact_id)
            facts.append({**fact, "document": document})
    return facts


def count_source_refs(markdown: str) -> int:
    without_links = re.sub(r"\]\([^)]+\)", "]()", markdown)
    without_tags = re.sub(r"<[^>]+>", " ", without_links)
    return len(SOURCE_REF_RE.findall(without_tags))


def extract_fact_references(markdown: str) -> list[str]:
    return FACT_CARD_RE.findall(markdown)


def page_metadata(root: Path, path: Path) -> dict[str, Any]:
    frontmatter, markdown = read_markdown(path)
    rel = path.relative_to(root / "content").as_posix()
    axis = rel.split("/", 1)[0] if "/" in rel else "foundation"
    title = frontmatter.get("title") or first_h1(markdown) or title_from_path(path)
    slug = frontmatter.get("slug") or (path.parent.name if path.name == "index.md" else path.stem)
    return {
        "title": title,
        "slug": slug,
        "axis": frontmatter.get("axis", axis),
        "status": frontmatter.get("status", "draft"),
        "version_anchor": frontmatter.get("version_anchor", ""),
        "source_version": frontmatter.get("source_version", ""),
        "sources": frontmatter.get("sources", []),
        "path": rel,
        "source_ref_count": count_source_refs(markdown),
        "fact_refs": extract_fact_references(markdown),
    }


def extract_site_data(root: Path) -> dict[str, Any]:
    facts = flatten_facts(root)
    fact_ids = {fact["id"] for fact in facts}
    pages: list[dict[str, Any]] = []
    content_root = root / "content"
    if content_root.exists():
        for path in sorted(content_root.rglob("*.md")):
            page = page_metadata(root, path)
            for fact_id in page["fact_refs"]:
                if fact_id not in fact_ids:
                    raise ValueError(f"undefined fact id {fact_id} in {page['path']}")
            pages.append(page)

    statuses = {
        status: sum(1 for fact in facts if fact["verification"]["status"] == status)
        for status in STATUS_MAP
    }
    return {
        "facts": facts,
        "pages": pages,
        "stats": {
            "fact_count": len(facts),
            "page_count": len(pages),
            "statuses": statuses,
        },
    }


def main() -> int:
    parser = argparse.ArgumentParser(description="Extract site data for VitePress")
    parser.add_argument("--root", type=Path, default=Path(__file__).resolve().parents[2])
    parser.add_argument("--output", type=Path, default=None)
    args = parser.parse_args()
    root = args.root.resolve()
    output = args.output or (root / "generated" / "site-data.json")

    data = extract_site_data(root)
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"wrote {output.relative_to(root).as_posix()}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
