# GTNH Insight Atlas

GTNH Insight Atlas is a source-traceable knowledge atlas for GregTech: New Horizons. It rebuilds the old prose-first GTNH-Insight repository as a data-driven site: structured facts, line-level source checks, generated navigation, search, graph views, and a small set of audited vertical slices.

The first release intentionally covers only three slices:

- Electric Blast Furnace
- Overclocking
- Voltage tiers

Everything else remains in the old repository as read-only reference material.

## Three Rules

1. Version anchors are mandatory. The site-level anchor is `GTNH 2.9.0-beta-1`; source facts are locked to `GT5-Unofficial 5.09.52.594`.
2. Mechanic facts live in `data/` and must point back to source files with `file:line` evidence.
3. Components explain validated data. They do not invent or hard-code mechanic constants.

## Quick Start

```powershell
pnpm install
pip install -e .[dev]
pnpm check
pnpm dev
```

The dev server serves the VitePress site from `content/` using config in `site/.vitepress/`.

## Repository Map

```text
content/              VitePress pages and the first vertical slices
data/                 Structured mechanic facts and JSON Schemas
generated/            Generated JSON consumed by the site
legacy/               Mapping from old GTNH-Insight pages to Atlas pages
scripts/atlas/        Python validation, extraction, indexing, and graph tools
site/.vitepress/      VitePress config, theme, and Vue components
_local/               Local-only source trees, jars, configs, questbook data
```

`_local/` is ignored except for `_local/README.md`. The source checker expects GT5U sources at `_local/gt5u-src/src/main/java`, or at the path supplied by `GT5U_SRC`.

## Build Pipeline

```powershell
python -m scripts.atlas.validate_data
python -m scripts.atlas.source_refs --strict
python -m scripts.atlas.extract_site_data
python -m scripts.atlas.markdown_index
python -m scripts.atlas.link_graph
python -m pytest scripts/atlas/tests
pnpm build
```

`pnpm check` runs data validation, strict source reference checks, extraction, Python tests, and VitePress build. Strict source checks require `_local/gt5u-src`; CI runs the rest of the pipeline from tracked files.
