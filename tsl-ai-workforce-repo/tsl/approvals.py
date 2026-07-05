"""Approval queue — escalation THẬT: mỗi BLOCK/REQUIRE tạo một yêu cầu duyệt.

Bản pilot lưu JSON; production thay bằng CRM/task system mà không đổi interface.
"""
from __future__ import annotations
import json, time, uuid
from pathlib import Path


class ApprovalQueue:
    def __init__(self, path: str | Path = "data/approvals.json"):
        self.path = Path(path)
        self.path.parent.mkdir(parents=True, exist_ok=True)
        self.items = json.loads(self.path.read_text(encoding="utf-8")) if self.path.exists() else []

    def create(self, *, action: str, rule: str, route_to: str | None,
               customer: str | None, context: str) -> dict:
        item = {
            "id": "APR-" + uuid.uuid4().hex[:8],
            "created": time.strftime("%Y-%m-%dT%H:%M:%S"),
            "status": "pending", "action": action, "rule": rule,
            "assigned_to": route_to, "customer": customer, "context": context,
        }
        self.items.append(item)
        self._flush()
        return item

    def pending(self) -> list:
        return [i for i in self.items if i["status"] == "pending"]

    def resolve(self, approval_id: str, status: str = "approved") -> bool:
        for i in self.items:
            if i["id"] == approval_id:
                i["status"] = status
                self._flush()
                return True
        return False

    def _flush(self) -> None:
        self.path.write_text(json.dumps(self.items, ensure_ascii=False, indent=2), encoding="utf-8")
