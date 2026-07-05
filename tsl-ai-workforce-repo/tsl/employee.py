"""AIEmployee — runtime production của một Nhân viên AI.

Luồng: recall memory -> build prompt (kèm ngữ cảnh khách) -> LLM -> parse <action>
-> Enforcement -> thực thi ALLOW / tạo Approval cho BLOCK|REQUIRE -> audit -> remember.
"""
from __future__ import annotations
from dataclasses import dataclass, field
from .constitution import Constitution
from .enforcement import EnforcementEngine, ALLOW, BLOCK, REQUIRE
from .actions import parse_actions, strip_actions
from .llm import get_provider, BaseProvider
from .memory import Memory
from .approvals import ApprovalQueue
from .audit import Audit


@dataclass
class Turn:
    reply: str
    decisions: list = field(default_factory=list)   # [(Action, Decision)]
    executed: list = field(default_factory=list)    # Action đã ALLOW
    approvals: list = field(default_factory=list)    # yêu cầu duyệt đã tạo


class AIEmployee:
    def __init__(self, constitution: Constitution, emp_id: str = "ai_sales",
                 provider: BaseProvider | None = None, memory: Memory | None = None,
                 approvals: ApprovalQueue | None = None, audit: Audit | None = None):
        self.c = constitution
        self.emp_id = emp_id
        self.engine = EnforcementEngine(constitution)
        self.provider = provider or get_provider(emp_id)
        self.memory = memory or Memory()
        self.approvals = approvals or ApprovalQueue()
        self.audit = audit or Audit()
        self.profile = constitution.employee(emp_id)

    def system_prompt(self, customer: str | None = None) -> str:
        auth = self.c.authority(self.emp_id)
        can = ", ".join(auth.get("can", []))
        cannot = ", ".join(auth.get("cannot", []))
        p = self.profile.get("personality", {})
        mem_ctx = ""
        if customer:
            m = self.memory.get_customer(customer)
            if m:
                mem_ctx = f"\nGhi nhớ về khách '{customer}': {m}."
        return f"""Bạn là {self.profile.get('identity', {}).get('employee_id', self.emp_id)} \
- nhân viên số của {self.c.company.get('short_name', '')}, vận hành theo Hiến pháp \
{self.c.id} v{self.c.version}. Bạn KHÔNG được vượt qua Hiến pháp.
Tone: {p.get('tone', 'chuyên nghiệp')}.
ĐƯỢC LÀM: {can}.
KHÔNG ĐƯỢC: {cannot}.{mem_ctx}
Khi vượt thẩm quyền: không tự quyết, escalate đúng người.
Khi thực hiện hành động có hệ quả, phát khối:
<action>name: <ten>
discount_percent: <so>
gross_margin_percent: <so>
contract_value: <so></action>
Tuyệt đối không báo "đã hoàn tất" nếu hệ thống trả BLOCK."""

    def handle(self, message: str, customer: str | None = None) -> Turn:
        raw = self.provider.complete(self.system_prompt(customer), message)
        actions = parse_actions(raw, self.emp_id)
        turn = Turn(reply=strip_actions(raw))
        for act in actions:
            d = self.engine.evaluate(act)
            turn.decisions.append((act, d))
            if d.verdict == ALLOW:
                turn.executed.append(act)
            else:
                apr = self.approvals.create(
                    action=act.name, rule=d.rule or "", route_to=d.route_to,
                    customer=customer, context=message)
                turn.approvals.append(apr)
                who = f" (chuyển: {d.route_to}, mã {apr['id']})" if d.route_to else f" (mã {apr['id']})"
                turn.reply += f"\n[Hệ thống: {d.verdict} — {d.message}{who}]"
            self.audit.log("decision", employee=self.emp_id, customer=customer,
                           action=act.name, verdict=d.verdict, rule=d.rule, route=d.route_to)
        return turn

    def remember(self, customer: str, field: str, value) -> None:
        self.memory.remember_customer(customer, field, value)
