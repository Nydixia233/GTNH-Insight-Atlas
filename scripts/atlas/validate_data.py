from __future__ import annotations

import argparse
import json
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Iterable

import yaml
from jsonschema import Draft202012Validator

from scripts.atlas import LOCKED_VERSION


ROOT = Path(__file__).resolve().parents[2]
FACT_SCHEMA_PATH = ROOT / "data" / "schemas" / "fact.schema.json"
FACT_SCHEMA = json.loads(FACT_SCHEMA_PATH.read_text(encoding="utf-8"))
FACT_VALIDATOR = Draft202012Validator(FACT_SCHEMA)


@dataclass(frozen=True)
class ValidationIssue:
    document: str
    fact_id: str
    message: str


def load_fact_documents(root: Path) -> dict[str, list[dict[str, Any]]]:
    documents: dict[str, list[dict[str, Any]]] = {}
    for path in sorted((root / "data").rglob("*.yml")):
        if "schemas" in path.parts:
            continue
        loaded = yaml.safe_load(path.read_text(encoding="utf-8"))
        if isinstance(loaded, list) and all(isinstance(item, dict) and "id" in item for item in loaded):
            documents[path.relative_to(root).as_posix()] = loaded
    for path in sorted((root / "data").rglob("*.yaml")):
        if "schemas" in path.parts:
            continue
        loaded = yaml.safe_load(path.read_text(encoding="utf-8"))
        if isinstance(loaded, list) and all(isinstance(item, dict) and "id" in item for item in loaded):
            documents[path.relative_to(root).as_posix()] = loaded
    return documents


def validate_fact_documents(
    documents: dict[str, Iterable[dict[str, Any]]],
    root: Path,
) -> list[ValidationIssue]:
    issues: list[ValidationIssue] = []
    seen_ids: dict[str, str] = {}

    for document, facts in documents.items():
        for index, fact in enumerate(facts):
            fact_id = str(fact.get("id", f"{document}#{index}"))
            for error in FACT_VALIDATOR.iter_errors(fact):
                issues.append(ValidationIssue(document, fact_id, error.message))
            if fact_id in seen_ids:
                issues.append(
                    ValidationIssue(
                        document,
                        fact_id,
                        f"duplicate fact id {fact_id} also found in {seen_ids[fact_id]}",
                    )
                )
            else:
                seen_ids[fact_id] = document

            for source in fact.get("source", []):
                version = source.get("version")
                if version != LOCKED_VERSION:
                    issues.append(
                        ValidationIssue(
                            document,
                            fact_id,
                            f"source.version must be {LOCKED_VERSION}, got {version!r}",
                        )
                    )
    return issues


def validate_all(root: Path) -> list[ValidationIssue]:
    return validate_fact_documents(load_fact_documents(root), root)


def main() -> int:
    parser = argparse.ArgumentParser(description="Validate Atlas fact data")
    parser.add_argument("--root", type=Path, default=ROOT)
    args = parser.parse_args()

    issues = validate_all(args.root.resolve())
    for issue in issues:
        print(f"{issue.document}: {issue.fact_id}: {issue.message}")
    return 1 if issues else 0


if __name__ == "__main__":
    raise SystemExit(main())
