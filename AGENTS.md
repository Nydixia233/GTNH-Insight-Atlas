# Agent Rules

This repository is a source-traceable documentation and site project. It does not develop Minecraft mod code.

## Iron Rules

1. Missing `value`, `source`, `source.version`, or `verification` on a fact is a build failure.
2. Vue components must not hard-code mechanic constants. Read them from validated data.
3. Key mechanic values must link to `data/` facts or locked source lines.
4. Do not use Obsidian-style `[[wikilink]]`; use relative Markdown links.
5. GT5U fact `source.version` must equal `5.09.52.594`.

## Source Policy

Large local references live in `_local/` and are ignored by git except `_local/README.md`. Only short, cited snippets may be copied into `content/**/snippets/`.

## Verification

Before claiming completion, run the relevant validation command:

- `python -m scripts.atlas.validate_data`
- `python -m scripts.atlas.source_refs --strict`
- `python -m pytest scripts/atlas/tests`
- `pnpm build`

If `_local/gt5u-src` is unavailable, non-strict source checks may warn instead of failing. Strict checks are expected for local development.
