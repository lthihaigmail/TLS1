"""Kịch bản nghiệm thu tự động — khớp Mục 7 tài liệu Đặc tả."""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))
from tsl import Constitution, EnforcementEngine, Action, ALLOW, BLOCK, REQUIRE

C = Constitution.load(os.path.join(os.path.dirname(__file__), "..", "constitution", "apd-constitution.yaml"))
E = EnforcementEngine(C)


def v(act):
    return E.evaluate(act).verdict


def test_discount_ok():
    assert v(Action("create_quote", discount_percent=3, gross_margin_percent=20, contract_value=120_000_000)) == ALLOW

def test_discount_over_limit():
    assert v(Action("create_quote", discount_percent=8, gross_margin_percent=15)) == BLOCK

def test_low_margin():
    assert v(Action("create_quote", discount_percent=2, gross_margin_percent=9)) == BLOCK

def test_credit_blocked():
    assert v(Action("offer_credit_terms")) == BLOCK

def test_tech_change_requires_approval():
    assert v(Action("change_technical_spec")) == BLOCK  # nằm trong cannot -> block/escalate

def test_sign_contract_blocked():
    assert v(Action("sign_contract", contract_value=450_000_000)) == BLOCK

def test_big_contract_requires_board():
    assert v(Action("create_quote", discount_percent=1, gross_margin_percent=18, contract_value=600_000_000)) == REQUIRE

def test_gray_market_blocked():
    assert v(Action("sell_gray_market")) == BLOCK

def test_cost_disclosure_blocked():
    assert v(Action("disclose_cost_or_margin")) == BLOCK

def test_schedule_demo_allowed():
    assert v(Action("schedule_demo")) == ALLOW
