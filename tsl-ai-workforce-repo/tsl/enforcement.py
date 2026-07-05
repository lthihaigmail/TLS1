"""Enforcement Engine — lớp policy TẤT ĐỊNH, đứng NGOÀI LLM.

Tổng quát cho MỌI nhân viên AI: đọc thẩm quyền (can/cannot/escalate) theo emp_id
từ Hiến pháp + hard rules số học. Đổi luật là đổi hành vi, không sửa code.
"""
from __future__ import annotations
from dataclasses import dataclass, field
from .constitution import Constitution

ALLOW = "ALLOW"
BLOCK = "BLOCK"
REQUIRE = "REQUIRE_HUMAN_APPROVAL"


@dataclass
class Action:
    name: str
    employee: str = "ai_sales"
    step: str | None = None
    discount_percent: float = 0.0
    gross_margin_percent: float = 100.0
    contract_value: float = 0.0
    payload: dict = field(default_factory=dict)


@dataclass
class Decision:
    verdict: str
    rule: str | None
    message: str
    route_to: str | None = None

    @property
    def allowed(self) -> bool:
        return self.verdict == ALLOW


# action -> "khả năng bị cấm" trong authority.cannot (nếu khác tên action)
_CANNOT_MAP = {
    "sign_contract": "sign_contract",
    "offer_credit_terms": "approve_credit_terms",
    "sell_gray_market": "sell_gray_market",
    "disclose_cost_or_margin": "disclose_cost_or_margin",
    "change_technical_spec": "change_technical_spec_without_tech_lead",
    "commit_delivery_date": "commit_delivery_date_without_ops",
    # CS: tên action trùng tên cannot -> map identity (mặc định), liệt kê cho rõ
    "issue_refund": "issue_refund",
    "approve_return": "approve_return",
    "promise_compensation": "promise_compensation",
    "quote_price": "quote_price",
}
# action -> key trong authority.escalate_to
_ROUTE_KEY = {
    "sign_contract": "contract_signature",
    "offer_credit_terms": "credit_request",
    "change_technical_spec": "technical_config",
    "commit_delivery_date": "delivery_commitment",
    "issue_refund": "refund_request",
    "approve_return": "refund_request",
    "promise_compensation": "refund_request",
    "quote_price": "price_question",
    "technical_fault": "technical_fault",
    "place_purchase_order": "purchase_order",
    "approve_supplier": "new_supplier",
    "make_hiring_decision": "hiring_decision",
    "sign_offer": "offer_letter",
    "approve_payment": "payment_approval",
    "issue_disbursement": "disbursement",
    "publish_paid_ads": "ad_spend",
    "spend_budget": "ad_spend",
    "sign_agency_contract": "agency_contract",
    "approve_final_design": "final_design",
    "change_safety_spec": "safety_change",
    "approve_shipment": "shipment_release",
    "waive_defect": "defect_waiver",
    "approve_resource_reallocation": "resource_reallocation",
    "approve_contract": "contract_approval",
    "release_goods_without_payment": "goods_release",
    "approve_stock_writeoff": "stock_writeoff",
    "certify_competency": "certification",
    "approve_promotion": "promotion",
    "approve_capex": "capex",
    "change_org_structure": "org_change",
    "make_strategic_decision": "strategic_decision",
    "approve_budget": "budget_approval",
}


class EnforcementEngine:
    def __init__(self, constitution: Constitution):
        self.c = constitution

    def _authority_block(self, act: Action) -> Decision | None:
        auth = self.c.authority(act.employee)
        cannot = set(auth.get("cannot", []))
        escalate = auth.get("escalate_to", {})
        mapped = _CANNOT_MAP.get(act.name, act.name)
        hit = mapped if mapped in cannot else (act.name if act.name in cannot else None)
        if hit:
            route = escalate.get(_ROUTE_KEY.get(act.name, ""), None)
            return Decision(BLOCK, f"authority:{hit}",
                            f"'{act.name}' vượt thẩm quyền của {act.employee}.", route)
        return None

    def _hard_rules(self, act: Action) -> Decision | None:
        dl, mm = self.c.discount_limit(), self.c.min_margin()
        bt = self.c.board_threshold()
        if act.name == "create_quote":
            if act.discount_percent > dl:
                return Decision(BLOCK, "block_over_discount",
                                f"Giảm giá {act.discount_percent}% vượt trần {dl}% — cần Sales Manager duyệt.",
                                "sales_manager")
            if act.gross_margin_percent < mm:
                return Decision(BLOCK, "block_low_margin",
                                f"Biên {act.gross_margin_percent}% dưới tối thiểu {mm}% — cần Giám đốc KD duyệt.",
                                "sales_director")
            if act.contract_value > bt:
                return Decision(REQUIRE, "contract_value_above_threshold",
                                f"Giá trị {act.contract_value:,.0f}đ vượt ngưỡng — cần Ban Giám đốc duyệt.",
                                "board")
        if act.step == "thiet_ke_giai_phap":
            return Decision(REQUIRE, "require_tech_review",
                            "Cấu hình kỹ thuật phải được Trưởng phòng Kỹ thuật duyệt.", "tech_lead")
        return None

    def evaluate(self, act: Action) -> Decision:
        d = self._authority_block(act) or self._hard_rules(act)
        return d or Decision(ALLOW, None, "Hợp lệ theo Hiến pháp.")
