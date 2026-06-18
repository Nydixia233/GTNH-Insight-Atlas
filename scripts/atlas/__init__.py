from __future__ import annotations

import os
import re
from dataclasses import dataclass
from pathlib import Path

SOURCE_REF_RE = re.compile(r'(?<!["\'=])\b[\w./-]+\.(?:java|kt|groovy|md|json|cfg|zs):\d+\b')
STATUS_ORDER = ("🟢", "🟡", "🔴", "🔵", "⬜")
LOCKED_VERSION = "5.09.52.594"
SRC_ROOT = Path(os.environ.get("GT5U_SRC", "_local/gt5u-src/src/main/java"))


@dataclass(frozen=True)
class StatusInfo:
    name: str
    emoji: str


STATUS_MAP = {
    "verified": StatusInfo("verified", "🟢"),
    "source-only": StatusInfo("source-only", "🔵"),
    "pending": StatusInfo("pending", "🟡"),
    "contradicted": StatusInfo("contradicted", "🔴"),
}


def status_for(name: str) -> StatusInfo:
    return STATUS_MAP[name]
