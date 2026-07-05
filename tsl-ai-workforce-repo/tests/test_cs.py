"""Nghiệm thu AI Customer Service — thẩm quyền riêng, cùng engine."""
import os, sys, tempfile
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))
from tsl import Constitution, EnforcementEngine, Action, AIEmployee, MockProvider
from tsl import Memory, ApprovalQueue, Audit, ALLOW, BLOCK

CPATH = os.path.join(os.path.dirname(__file__), "..", "constitution", "apd-constitution.yaml")
C = Constitution.load(CPATH)
E = EnforcementEngine(C)


def v(name):
    return E.evaluate(Action(name, employee="ai_customer_service")).verdict


def test_cs_track_order_allowed():
    assert v("track_order_status") == ALLOW

def test_cs_faq_allowed():
    assert v("answer_faq") == ALLOW

def test_cs_schedule_maintenance_allowed():
    assert v("schedule_maintenance") == ALLOW

def test_cs_refund_blocked():
    assert v("issue_refund") == BLOCK

def test_cs_return_blocked():
    assert v("approve_return") == BLOCK

def test_cs_compensation_blocked():
    assert v("promise_compensation") == BLOCK

def test_cs_quote_price_blocked_routes_to_sales():
    d = E.evaluate(Action("quote_price", employee="ai_customer_service"))
    assert d.verdict == BLOCK and d.route_to == "ai_sales"

def test_cs_refund_routes_to_sales_manager():
    d = E.evaluate(Action("issue_refund", employee="ai_customer_service"))
    assert d.route_to == "sales_manager"

def test_cs_pipeline_refund_creates_approval():
    with tempfile.TemporaryDirectory() as t:
        emp = AIEmployee(C, "ai_customer_service", provider=MockProvider("ai_customer_service"),
                         memory=Memory(f"{t}/m.json"), approvals=ApprovalQueue(f"{t}/a.json"), audit=Audit(f"{t}/l.jsonl"))
        turn = emp.handle("Sản phẩm lỗi tôi muốn hoàn tiền", customer="KH-X")
        assert turn.approvals and turn.approvals[0]["assigned_to"] == "sales_manager"
