from __future__ import annotations

import argparse
import re
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Iterable

from scripts.atlas import LOCKED_VERSION, SOURCE_REF_RE, SRC_ROOT
from scripts.atlas.validate_data import load_fact_documents


@dataclass(frozen=True)
class SourceMessage:
    severity: str
    message: str
    document: str = ""
    fact_id: str = ""


def find_source_refs(text: str) -> list[str]:
    text = re.sub(r"\]\([^)]+\)", "]()", text)
    text = re.sub(r"<[^>]+>", " ", text)
    return SOURCE_REF_RE.findall(text)


def check_source_entries(
    entries: Iterable[dict[str, Any]],
    src_root: Path = SRC_ROOT,
    strict: bool = True,
) -> list[SourceMessage]:
    messages: list[SourceMessage] = []
    for entry in entries:
        rel_file = str(entry.get("file", ""))
        line = int(entry.get("line", 0) or 0)
        expect = entry.get("expect")
        version = entry.get("version")
        path = src_root / rel_file

        if version != LOCKED_VERSION:
            messages.append(
                SourceMessage(
                    "error" if strict else "warning",
                    f"{rel_file}:{line} uses unsupported version {version!r}",
                )
            )
            continue

        if not path.exists():
            messages.append(
                SourceMessage(
                    "error" if strict else "warning",
                    f"source file missing: {rel_file}",
                )
            )
            continue

        lines = path.read_text(encoding="utf-8").splitlines()
        if line < 1 or line > len(lines):
            messages.append(SourceMessage("error", f"line out of range: {rel_file}:{line}"))
            continue

        if expect and expect not in lines[line - 1]:
            messages.append(
                SourceMessage(
                    "error",
                    f"expected snippet not found in {rel_file}:{line}: {expect}",
                )
            )
    return messages


def check_all(root: Path, strict: bool = True) -> list[SourceMessage]:
    messages: list[SourceMessage] = []
    for document, facts in load_fact_documents(root).items():
        for fact in facts:
            fact_id = str(fact.get("id", ""))
            messages.extend(
                SourceMessage(
                    msg.severity,
                    msg.message,
                    document,
                    fact_id,
                )
                for msg in check_source_entries(fact.get("source", []), SRC_ROOT, strict=strict)
            )
    return messages


def main() -> int:
    parser = argparse.ArgumentParser(description="Check Atlas source references")
    parser.add_argument("--root", type=Path, default=Path(__file__).resolve().parents[2])
    parser.add_argument("--strict", action="store_true")
    args = parser.parse_args()

    messages = check_all(args.root.resolve(), strict=args.strict)
    for message in messages:
        print(f"{message.severity.upper()}: {message.message}")
    return 1 if any(message.severity == "error" for message in messages) else 0


if __name__ == "__main__":
    raise SystemExit(main())
