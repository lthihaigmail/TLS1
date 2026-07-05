"""Audit log — ghi mọi tương tác & quyết định ra JSONL (phục vụ audit & cải tiến)."""
from __future__ import annotations
import json, time
from pathlib import Path


class Audit:
    def __init__(self, path: str | Path = "data/audit.jsonl"):
        self.path = Path(path)
        self.path.parent.mkdir(parents=True, exist_ok=True)

    def log(self, event: str, **fields) -> None:
        rec = {"ts": time.strftime("%Y-%m-%dT%H:%M:%S"), "event": event, **fields}
        with self.path.open("a", encoding="utf-8") as f:
            f.write(json.dumps(rec, ensure_ascii=False) + "\n")
