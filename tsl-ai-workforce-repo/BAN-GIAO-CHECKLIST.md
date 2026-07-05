# TSL AI Workforce — Checklist bàn giao (v2.0 · ĐỦ BỘ 14 nhân viên)

Toàn bộ đội hình nhân viên số chạy trên **một Hiến pháp + một engine**.

| Nhân viên | Mã | Phòng ban | Được làm (mẫu) | Chặn/Escalate (mẫu) |
|-----------|----|-----------|----------------|---------------------|
| AI Sales | AI-00045 | Sales | recommend_solution, create_quote… | approve_discount_above_5_percent, approve_credit_terms… |
| AI Customer Service | AI-00046 | CS | answer_faq, track_order_status… | issue_refund, promise_compensation… |
| AI Procurement | AI-00047 | Mua hàng | check_stock, suggest_reorder… | place_purchase_order, approve_supplier… |
| AI HR | AI-00048 | Nhân sự | screen_cv, schedule_interview… | make_hiring_decision, sign_offer… |
| AI Finance | AI-00049 | Tài chính | record_invoice, aging_report… | approve_payment, issue_disbursement… |
| AI Marketing | AI-00050 | Marketing | draft_content, schedule_post… | publish_paid_ads, spend_budget… |
| AI Engineer | AI-00051 | Kỹ thuật | size_configuration, technical_faq… | approve_final_design, change_safety_spec… |
| AI QA | AI-00052 | QA | log_defect, run_checklist… | approve_shipment, waive_defect… |
| AI Planner | AI-00053 | Kế hoạch | build_schedule, capacity_check… | commit_delivery_date, approve_resource_reallocation… |
| AI Legal | AI-00054 | Pháp chế | flag_contract_risk, explain_clause… | approve_contract, sign_contract… |
| AI Warehouse | AI-00055 | Kho vận | check_inventory, pick_list… | approve_stock_writeoff, release_goods_without_payment… |
| AI Trainer | AI-00056 | Đào tạo | build_training_plan, create_quiz… | certify_competency, approve_promotion… |
| AI COO | AI-00057 | Vận hành | ops_dashboard, kpi_report… | approve_capex, change_org_structure… |
| AI CEO | AI-00058 | Điều hành | strategy_brief, okr_review… | make_strategic_decision, approve_budget… |

## Nghiệm thu (tự động, toàn bộ)
- pytest: **34 passed**
- acceptance: **97/97 PASS** — mọi 'can' → CHO PHÉP, mọi 'cannot' → CHẶN/DUYỆT đúng người.
- Server multi-employee: `/chat {employee}` phục vụ cả 14; hàng đợi duyệt dùng chung.

## Vì sao bán được "đủ bộ" một lần
- Kiến trúc Runtime: thêm nhân viên = thêm khối Hiến pháp (can/cannot/escalate) + 1 nhánh ngữ cảnh.
- KHÔNG sửa enforcement/runtime. 10 nhân viên cuối được bật bằng đúng cơ chế đó.
- Chi phí biên ~ 0 → gói "đủ bộ" có biên lợi nhuận cao nhất.

## Go-live phía khách (mỗi phòng ban)
- [ ] Thay chính sách/thẩm quyền thật cho từng phòng vào Hiến pháp.
- [ ] Nối kênh cho các nhân viên cần chạy trước (Sales, CS...).
- [ ] Bật dần theo mức sẵn sàng của từng phòng ban.
