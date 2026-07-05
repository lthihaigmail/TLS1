"""Constitution loader — đọc Hiến pháp máy đọc được (YAML)."""
from __future__ import annotations
import yaml
from pathlib import Path


class Constitution:
    def __init__(self, data: dict):
        self.data = data

    @classmethod
    def load(cls, path: str | Path) -> "Constitution":
        with open(path, "r", encoding="utf-8") as f:
            return cls(yaml.safe_load(f))

    # --- accessors tiện dụng ---
    @property
    def id(self) -> str:
        return self.data.get("meta", {}).get("constitution_id", "UNKNOWN")

    @property
    def version(self) -> str:
        return str(self.data.get("meta", {}).get("version", "0"))

    @property
    def company(self) -> dict:
        return self.data.get("company", {})

    @property
    def policies(self) -> dict:
        return self.data.get("policies", {})

    @property
    def approval(self) -> dict:
        return self.data.get("approval", {})

    @property
    def enforcement(self) -> dict:
        return self.data.get("enforcement", {})

    def employee(self, emp_id: str) -> dict:
        return self.data.get("ai_workforce", {}).get(emp_id, {})

    def authority(self, emp_id: str) -> dict:
        return self.employee(emp_id).get("authority", {})

    def discount_limit(self) -> float:
        return float(self.policies.get("sales", {}).get("discount_limit_percent", 5))

    def min_margin(self) -> float:
        return float(self.policies.get("sales", {}).get("min_gross_margin_percent", 12))

    def board_threshold(self) -> float:
        return float(self.policies.get("payment", {}).get("max_credit_limit_vnd", 500_000_000))
