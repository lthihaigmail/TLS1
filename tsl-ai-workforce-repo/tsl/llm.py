"""LLM provider abstraction (role-aware mock cho demo/test).

- MockProvider(role): trả lời + khối <action> theo vai trò (ai_sales / ai_customer_service).
- OpenAIProvider / AnthropicProvider: bản thật, bật khi có API key.
"""
from __future__ import annotations
import os
import re


class BaseProvider:
    def complete(self, system_prompt: str, user_message: str) -> str:
        raise NotImplementedError


ROLE_TABLE = {
    "ai_finance":   {"default": "aging_report",        "triggers": [("duyệt", "approve_payment"), ("thanh toán", "approve_payment"), ("chi tiền", "issue_disbursement"), ("đổi tài khoản", "change_bank_details")]},
    "ai_marketing": {"default": "draft_content",       "triggers": [("chạy quảng cáo", "publish_paid_ads"), ("quảng cáo", "publish_paid_ads"), ("ngân sách", "spend_budget"), ("ký agency", "sign_agency_contract")]},
    "ai_engineer":  {"default": "size_configuration",  "triggers": [("duyệt thiết kế", "approve_final_design"), ("chốt thiết kế", "approve_final_design"), ("an toàn", "change_safety_spec"), ("chứng nhận", "certify_product")]},
    "ai_qa":        {"default": "run_checklist",       "triggers": [("cho xuất", "approve_shipment"), ("xuất hàng", "approve_shipment"), ("bỏ qua lỗi", "waive_defect"), ("đóng capa", "close_capa")]},
    "ai_planner":   {"default": "build_schedule",      "triggers": [("cam kết giao", "commit_delivery_date"), ("chốt ngày giao", "commit_delivery_date"), ("điều phối lại", "approve_resource_reallocation")]},
    "ai_legal":     {"default": "explain_clause",      "triggers": [("duyệt hợp đồng", "approve_contract"), ("ký", "sign_contract"), ("tư vấn ràng buộc", "give_binding_advice")]},
    "ai_warehouse": {"default": "check_inventory",     "triggers": [("xuất kho", "release_goods_without_payment"), ("giao khi chưa thanh toán", "release_goods_without_payment"), ("hủy tồn", "approve_stock_writeoff")]},
    "ai_trainer":   {"default": "build_training_plan", "triggers": [("cấp chứng chỉ", "certify_competency"), ("chứng nhận", "certify_competency"), ("thăng chức", "approve_promotion")]},
    "ai_coo":       {"default": "kpi_report",          "triggers": [("duyệt đầu tư", "approve_capex"), ("capex", "approve_capex"), ("thay đổi cơ cấu", "change_org_structure"), ("tuyển hay sa thải", "hire_or_fire")]},
    "ai_ceo":       {"default": "strategy_brief",      "triggers": [("quyết định chiến lược", "make_strategic_decision"), ("chốt chiến lược", "make_strategic_decision"), ("duyệt ngân sách", "approve_budget")]},
}


def _mk(action, note):
    return f"{note}\n<action>name: {action}</action>"


class _GenericMixin:
    def _generic(self, role, message):
        m = message.lower()
        spec = ROLE_TABLE[role]
        for kw, act in spec["triggers"]:
            if kw in m:
                return _mk(act, "Em ghi nhận và chuyển bộ phận có thẩm quyền ạ.")
        return _mk(spec["default"], "Dạ em hỗ trợ trong phạm vi của em ạ.")


class MockProvider(_GenericMixin, BaseProvider):
    def __init__(self, role: str = "ai_sales"):
        self.role = role

    def complete(self, system_prompt: str, user_message: str) -> str:
        if self.role == "ai_customer_service":
            return self._cs(user_message)
        if self.role == "ai_procurement":
            return self._proc(user_message)
        if self.role == "ai_hr":
            return self._hr(user_message)
        if self.role in ROLE_TABLE:
            return self._generic(self.role, user_message)
        return self._sales(user_message)

    # --------- AI Sales ---------
    def _sales(self, message: str) -> str:
        m = message.lower()
        mt = re.search(r"(\d+)\s*%", m)
        pct = float(mt.group(1)) if mt else None
        if "giá vốn" in m or "gia von" in m:
            return "Em xin phép không chia sẻ giá vốn ạ.\n<action>name: disclose_cost_or_margin</action>"
        if "công nợ" in m or "cong no" in m or "trả sau" in m:
            return "Em ghi nhận yêu cầu công nợ và chuyển duyệt ạ.\n<action>name: offer_credit_terms</action>"
        if "ký" in m and ("hợp đồng" in m or "hop dong" in m):
            return ("Em soạn bản nháp hợp đồng, nhưng không tự ký ạ.\n"
                    "<action>name: sign_contract\ncontract_value: 450000000</action>")
        if "trôi nổi" in m or "troi noi" in m:
            return "APD chỉ bán hàng chính hãng có CO/CQ ạ.\n<action>name: sell_gray_market</action>"
        if "đổi" in m and ("plc" in m or "cấu hình" in m or "cau hinh" in m):
            return "Việc đổi cấu hình cần Kỹ thuật xác nhận ạ.\n<action>name: change_technical_spec</action>"
        if "giao" in m and ("tuần" in m or "tuan" in m or "khi nào" in m):
            return "Em xác nhận tồn kho với Vận hành trước khi cam kết ngày ạ.\n<action>name: commit_delivery_date</action>"
        if pct is not None and ("giảm" in m or "bớt" in m or "giam" in m):
            margin = max(20 - pct, 8)
            return (f"Em ghi nhận đề nghị giảm {pct:.0f}% ạ.\n"
                    f"<action>name: create_quote\ndiscount_percent: {pct:.0f}\n"
                    f"gross_margin_percent: {margin:.0f}\ncontract_value: 320000000</action>")
        return ("Dạ em tư vấn giải pháp phù hợp và lập báo giá trong chính sách ạ.\n"
                "<action>name: create_quote\ndiscount_percent: 3\n"
                "gross_margin_percent: 20\ncontract_value: 120000000</action>")

    # --------- AI Customer Service ---------
    def _cs(self, message: str) -> str:
        m = message.lower()
        if "hoàn tiền" in m or "hoan tien" in m or "refund" in m:
            return ("Em rất tiếc về trải nghiệm này. Yêu cầu hoàn tiền em chuyển bộ phận có thẩm quyền ạ.\n"
                    "<action>name: issue_refund</action>")
        if "đổi trả" in m or "trả hàng" in m or "tra hang" in m or "đổi hàng" in m:
            return ("Em ghi nhận yêu cầu đổi/trả và chuyển duyệt ạ.\n<action>name: approve_return</action>")
        if "bồi thường" in m or "boi thuong" in m or "đền" in m:
            return ("Em ghi nhận và chuyển bộ phận phụ trách, em không tự hứa bồi thường ạ.\n"
                    "<action>name: promise_compensation</action>")
        if "giá" in m or "bao nhiêu tiền" in m or "báo giá" in m:
            return ("Về giá, em chuyển anh/chị cho bộ phận Kinh doanh để tư vấn chính xác ạ.\n"
                    "<action>name: quote_price</action>")
        if "bảo hành" in m or "bao hanh" in m or "bảo trì" in m or "bao tri" in m:
            return ("Em đặt lịch bảo trì/bảo hành cho mình ạ.\n<action>name: schedule_maintenance</action>")
        if "đơn" in m or "tình trạng" in m or "giao tới đâu" in m or "khi nào tới" in m or "vận đơn" in m:
            return ("Em kiểm tra tình trạng đơn hàng giúp anh/chị ngay ạ.\n<action>name: track_order_status</action>")
        if "khiếu nại" in m or "phàn nàn" in m or "than phiền" in m or "lỗi" in m:
            return ("Em rất tiếc, em ghi nhận phản ánh và tạo ticket theo dõi ạ.\n<action>name: log_ticket</action>")
        return ("Dạ em hỗ trợ giải đáp cho anh/chị ạ.\n<action>name: answer_faq</action>")


    # --------- AI Procurement ---------
    def _proc(self, message: str) -> str:
        m = message.lower()
        if "đặt hàng" in m or "tạo po" in m or "mua" in m and "500" in m or "đặt luôn" in m:
            return ("Em so sánh lead-time và tồn kho, nhưng tạo PO cần Vận hành duyệt ạ.\n"
                    "<action>name: place_purchase_order</action>")
        if "nhà cung cấp mới" in m or "ncc mới" in m or "duyệt ncc" in m:
            return ("Em đánh giá NCC, nhưng phê duyệt nhà cung cấp mới cần Ban Giám đốc ạ.\n"
                    "<action>name: approve_supplier</action>")
        if "tồn kho" in m or "còn hàng" in m or "kiểm kho" in m:
            return ("Em kiểm tra tồn kho ngay ạ.\n<action>name: check_stock</action>")
        if "đặt lại" in m or "reorder" in m or "sắp hết" in m:
            return ("Em gợi ý số lượng đặt lại theo định mức ạ.\n<action>name: suggest_reorder</action>")
        return ("Em so sánh lead-time các nhà cung cấp giúp anh/chị ạ.\n"
                "<action>name: compare_supplier_leadtime</action>")

    # --------- AI HR ---------
    def _hr(self, message: str) -> str:
        m = message.lower()
        if "tuyển luôn" in m or "chốt tuyển" in m or "nhận bạn" in m or "quyết định tuyển" in m:
            return ("Em đã sàng và xếp lịch, nhưng quyết định tuyển thuộc cấp quản lý ạ.\n"
                    "<action>name: make_hiring_decision</action>")
        if "offer" in m or "thư mời" in m or "ký hợp đồng lao động" in m:
            return ("Em soạn nháp offer, nhưng ký offer cần Ban Giám đốc ạ.\n"
                    "<action>name: sign_offer</action>")
        if "lương" in m and ("bao nhiêu" in m or "của" in m or "tiết lộ" in m):
            return ("Em xin phép không tiết lộ dữ liệu lương ạ.\n"
                    "<action>name: disclose_salary_data</action>")
        if "cv" in m or "hồ sơ" in m or "ứng viên" in m or "sàng" in m:
            return ("Em sàng lọc CV theo tiêu chí ạ.\n<action>name: screen_cv</action>")
        if "phỏng vấn" in m or "lịch" in m:
            return ("Em đặt lịch phỏng vấn cho ứng viên ạ.\n<action>name: schedule_interview</action>")
        if "jd" in m or "mô tả công việc" in m or "tin tuyển" in m:
            return ("Em soạn JD cho vị trí ạ.\n<action>name: draft_jd</action>")
        return ("Em giải đáp chính sách nhân sự cho anh/chị ạ.\n<action>name: answer_policy_faq</action>")


class OpenAIProvider(BaseProvider):
    def __init__(self, model: str = "gpt-4o-mini"):
        from openai import OpenAI
        self.client = OpenAI(api_key=os.environ["OPENAI_API_KEY"])
        self.model = model

    def complete(self, system_prompt: str, user_message: str) -> str:
        r = self.client.chat.completions.create(
            model=self.model,
            messages=[{"role": "system", "content": system_prompt},
                      {"role": "user", "content": user_message}],
            temperature=0.2)
        return r.choices[0].message.content


class AnthropicProvider(BaseProvider):
    def __init__(self, model: str = "claude-3-5-sonnet-latest"):
        import anthropic
        self.client = anthropic.Anthropic(api_key=os.environ["ANTHROPIC_API_KEY"])
        self.model = model

    def complete(self, system_prompt: str, user_message: str) -> str:
        r = self.client.messages.create(
            model=self.model, max_tokens=1024, system=system_prompt,
            messages=[{"role": "user", "content": user_message}])
        return "".join(b.text for b in r.content if b.type == "text")


def get_provider(role: str = "ai_sales") -> BaseProvider:
    p = os.environ.get("TSL_LLM_PROVIDER", "mock").lower()
    if p == "openai":
        return OpenAIProvider()
    if p == "anthropic":
        return AnthropicProvider()
    return MockProvider(role)
