"""Test pipeline đầy đủ: handle(), memory, approval queue."""
import os, sys, tempfile
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))
from tsl import Constitution, AIEmployee, Memory, ApprovalQueue, Audit, MockProvider

CPATH = os.path.join(os.path.dirname(__file__), "..", "constitution", "apd-constitution.yaml")


def _emp(tmp):
    c = Constitution.load(CPATH)
    return AIEmployee(c, "ai_sales", provider=MockProvider(),
                      memory=Memory(f"{tmp}/m.json"),
                      approvals=ApprovalQueue(f"{tmp}/a.json"),
                      audit=Audit(f"{tmp}/log.jsonl"))


def test_allow_flow():
    with tempfile.TemporaryDirectory() as t:
        turn = _emp(t).handle("Tư vấn giải pháp tủ điện cho nhà máy", customer="NM-A")
        assert turn.executed and not turn.approvals


def test_block_creates_approval():
    with tempfile.TemporaryDirectory() as t:
        emp = _emp(t)
        turn = emp.handle("Giảm 8% chốt luôn nhé", customer="NM-B")
        assert turn.approvals, "BLOCK phải tạo yêu cầu duyệt"
        assert emp.approvals.pending(), "approval phải nằm trong hàng đợi"
        assert turn.approvals[0]["assigned_to"] == "sales_manager"


def test_memory_recall():
    with tempfile.TemporaryDirectory() as t:
        emp = _emp(t)
        emp.remember("NM-C", "thuong_hieu_ua_thich", "Siemens")
        assert emp.memory.get_customer("NM-C")["thuong_hieu_ua_thich"] == "Siemens"


def test_audit_written():
    with tempfile.TemporaryDirectory() as t:
        emp = _emp(t)
        emp.handle("Cho tôi công nợ 30 ngày", customer="NM-D")
        assert os.path.exists(f"{t}/log.jsonl")
