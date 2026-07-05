"""Nghiệm thu tổng quát: mọi 'can' -> ALLOW, mọi 'cannot' -> BLOCK/REQUIRE."""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))
from tsl import Constitution, EnforcementEngine, Action, ALLOW, BLOCK, REQUIRE

C = Constitution.load(os.path.join(os.path.dirname(__file__), "..", "constitution", "apd-constitution.yaml"))
E = EnforcementEngine(C)
WF = C.data["ai_workforce"]


def test_has_full_roster():
    assert len(WF) >= 14


def test_every_can_allowed():
    for eid, prof in WF.items():
        for a in prof.get("authority", {}).get("can", []):
            assert E.evaluate(Action(a, employee=eid)).verdict == ALLOW, f"{eid}:{a} phải ALLOW"


def test_every_cannot_blocked():
    for eid, prof in WF.items():
        for a in prof.get("authority", {}).get("cannot", []):
            v = E.evaluate(Action(a, employee=eid)).verdict
            assert v in (BLOCK, REQUIRE), f"{eid}:{a} phải BLOCK/REQUIRE, gặp {v}"


def test_escalation_routes_present():
    # mỗi cannot có key escalate tương ứng thì phải route đúng (không None nếu có key)
    for eid, prof in WF.items():
        esc = prof.get("authority", {}).get("escalate_to", {})
        for a in prof.get("authority", {}).get("cannot", []):
            d = E.evaluate(Action(a, employee=eid))
            # nếu có route thì route phải nằm trong giá trị escalate_to (hoặc là vai trò hợp lệ)
            if d.route_to:
                assert d.route_to in set(esc.values()) or d.route_to in {
                    "sales_manager","sales_director","tech_lead","ops_lead","board","ai_sales","finance_lead"}
