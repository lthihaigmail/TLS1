"""Nghiệm thu AI Procurement + AI HR (cùng engine, khác thẩm quyền)."""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))
from tsl import Constitution, EnforcementEngine, Action, ALLOW, BLOCK

C = Constitution.load(os.path.join(os.path.dirname(__file__), "..", "constitution", "apd-constitution.yaml"))
E = EnforcementEngine(C)


def v(name, emp):
    return E.evaluate(Action(name, employee=emp))


def test_proc_check_stock_allowed():
    assert v("check_stock", "ai_procurement").verdict == ALLOW

def test_proc_po_blocked_to_ops():
    d = v("place_purchase_order", "ai_procurement")
    assert d.verdict == BLOCK and d.route_to == "ops_lead"

def test_proc_new_supplier_to_board():
    d = v("approve_supplier", "ai_procurement")
    assert d.verdict == BLOCK and d.route_to == "board"

def test_hr_screen_cv_allowed():
    assert v("screen_cv", "ai_hr").verdict == ALLOW

def test_hr_hiring_decision_blocked():
    d = v("make_hiring_decision", "ai_hr")
    assert d.verdict == BLOCK and d.route_to == "sales_director"

def test_hr_sign_offer_to_board():
    d = v("sign_offer", "ai_hr")
    assert d.verdict == BLOCK and d.route_to == "board"

def test_hr_salary_disclosure_blocked():
    assert v("disclose_salary_data", "ai_hr").verdict == BLOCK
