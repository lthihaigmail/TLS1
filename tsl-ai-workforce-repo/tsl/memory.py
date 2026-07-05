"""Organization Memory — lưu trí nhớ khách & tổ chức ra file JSON.

Bản pilot dùng file JSON cho đơn giản; production thay bằng DB/vector store
mà KHÔNG đổi interface.
"""
from __future__ import annotations
import json
from pathlib import Path


class Memory:
    def __init__(self, path: str | Path = "data/memory.json"):
        self.path = Path(path)
        self.path.parent.mkdir(parents=True, exist_ok=True)
        if self.path.exists():
            self.store = json.loads(self.path.read_text(encoding="utf-8"))
        else:
            self.store = {"customers": {}, "organization": []}

    def get_customer(self, name: str) -> dict:
        return self.store["customers"].get(name, {})

    def remember_customer(self, name: str, field: str, value) -> None:
        self.store["customers"].setdefault(name, {})[field] = value
        self._flush()

    def add_lesson(self, project: str, lesson: str) -> None:
        self.store["organization"].append({"project": project, "lesson": lesson})
        self._flush()

    def _flush(self) -> None:
        self.path.write_text(json.dumps(self.store, ensure_ascii=False, indent=2),
                             encoding="utf-8")
