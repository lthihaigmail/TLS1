"""Parser cho khối <action> mà LLM phát ra."""
from __future__ import annotations
import re
from .enforcement import Action

_BLOCK = re.compile(r"<action>(.*?)</action>", re.S)
_NUM_FIELDS = {"discount_percent", "gross_margin_percent", "contract_value"}


def parse_actions(text: str, employee: str = "ai_sales") -> list[Action]:
    actions = []
    for block in _BLOCK.findall(text):
        kv = {}
        for line in block.strip().splitlines():
            if ":" in line:
                k, v = line.split(":", 1)
                k, v = k.strip(), v.strip()
                kv[k] = float(v) if k in _NUM_FIELDS and v.replace(".", "").isdigit() else v
        if "name" in kv:
            actions.append(Action(
                name=kv["name"], employee=employee, step=kv.get("step"),
                discount_percent=kv.get("discount_percent", 0.0),
                gross_margin_percent=kv.get("gross_margin_percent", 100.0),
                contract_value=kv.get("contract_value", 0.0)))
    return actions


def strip_actions(text: str) -> str:
    return _BLOCK.sub("", text).strip()
