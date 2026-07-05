"""TSL AI Workforce — reference implementation.

Constitution (luật) -> Runtime (bộ não LLM) -> Enforcement (lớp cứng).
Đổi doanh nghiệp = đổi Constitution, KHÔNG sửa code.
"""
from .constitution import Constitution
from .enforcement import EnforcementEngine, Action, Decision, ALLOW, BLOCK, REQUIRE
from .employee import AIEmployee, Turn
from .llm import get_provider, MockProvider
from .memory import Memory
from .approvals import ApprovalQueue
from .audit import Audit

__all__ = [
    "Constitution", "EnforcementEngine", "Action", "Decision",
    "ALLOW", "BLOCK", "REQUIRE", "AIEmployee", "Turn",
    "get_provider", "MockProvider", "Memory", "ApprovalQueue", "Audit",
]
