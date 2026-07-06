# TSL AI Workforce

![CI](https://github.com/lthihaigmail/TLS1/actions/workflows/ci.yml/badge.svg)
· **Demo trực tuyến:** https://lthihaigmail.github.io/TLS1/

> Doanh nghiệp nạp tri thức thành **Hiến pháp máy đọc được** (TSL Constitution), và các **nhân viên số AI** chạy đúng theo Hiến pháp đó — có thẩm quyền giới hạn, có KPI, biết escalate. Mọi hành động đi qua **lớp enforcement tất định** trước khi thực thi. Đổi doanh nghiệp = đổi Hiến pháp, **không sửa code**.

Tác giả: **Emmy Lê Thị Hải** — System Leadership Coach (TSL) · Bản mẫu: An Phương Distribution (APD).

---

## Ý tưởng cốt lõi

```
Constitution (YAML)  →  AIEmployee (LLM runtime)  →  Enforcement (lớp cứng)  →  thực thi / escalate
        luật                  đề xuất <action>            chặn / duyệt / cho phép
```

- **Constitution Engine** — chuyển tri thức quản trị thành cấu trúc máy đọc & *thực thi* được.
- **AI Employee Runtime** — một bộ máy chạy mọi nhân viên AI; đổi công ty = đổi Hiến pháp.
- **Enforcement** — lớp policy tất định đứng ngoài LLM: LLM chỉ đề xuất, engine mới quyết định.
- **Organization Memory** — trí nhớ khách & tổ chức (JSON, thay được bằng DB).

## Đội hình (14 nhân viên AI)

| Nhóm | Nhân viên |
|------|-----------|
| Điều hành | AI CEO, AI COO |
| Doanh thu & Khách hàng | AI Sales, AI Marketing, AI Customer Service |
| Cung ứng & Vận hành | AI Procurement, AI Warehouse, AI Planner, AI QA |
| Chuyên môn & Hỗ trợ | AI Engineer, AI Finance, AI HR, AI Legal, AI Trainer |

Mỗi nhân viên có `can` / `cannot` / `escalate_to` khai báo trong `constitution/apd-constitution.yaml`.

## Chạy nhanh (không cần API key)

```bash
pip install -r requirements.txt
python run_demo.py          # demo cả 14 nhân viên qua pipeline
python -m pytest -q         # nghiệm thu tự động
python run_acceptance.py    # sinh data/acceptance-report.md
python console.py           # chat thử CLI
```

## Chạy server (webhook + chat UI)

```bash
uvicorn server:app --host 0.0.0.0 --port 8000
# http://localhost:8000  — chat UI (chọn nhân viên)
# POST /chat  {message, customer, employee}
# POST /webhook/zalo  — adapter Zalo OA
# GET  /approvals  — hàng đợi duyệt đang chờ
```

Dùng LLM thật: `cp .env.example .env` rồi đặt `TSL_LLM_PROVIDER=openai|anthropic` + API key.

Docker: `docker build -t ai-workforce . && docker run -p 8000:8000 ai-workforce`

## Cấu trúc repo

```
tsl/                     # package lõi: constitution, enforcement, employee, llm, memory, approvals, audit
constitution/            # Hiến pháp máy đọc được (YAML)
tests/                   # pytest — nghiệm thu tự động
server.py                # FastAPI: webhook + REST + chat UI
run_demo.py              # demo 14 nhân viên
run_acceptance.py        # sinh báo cáo nghiệm thu
console.py               # chat CLI
web/                     # bộ demo HTML (mở web/index.html)
docs/                    # đề xuất, đặc tả, hướng dẫn triển khai, chiến lược (Word/PDF/MD)
```

## Bộ demo trực quan (mở `web/index.html`)

Trước/Sau · Bản đồ vận hành · TSL OS Console · Enforcement Studio · Hiến pháp · Demo hội thoại.

## Nguyên tắc kỹ thuật

- Enforcement là lớp **cứng** — không phụ thuộc "LLM có nghe lời".
- Không hardcode chính sách trong code — mọi ngưỡng đọc từ Hiến pháp.
- `fallback_to_human`: không chắc → đẩy cho người.
- Thêm nhân viên = thêm khối trong Hiến pháp (+ 1 nhánh ngữ cảnh provider). Không đụng enforcement/runtime.

## Trạng thái

pytest **34 passed** · acceptance **97/97 PASS** (14 nhân viên).
CI (GitHub Actions) tự chạy `pytest` + `run_acceptance.py` mỗi lần push lên `main`.

## License

Proprietary — © 2026 Emmy Lê Thị Hải. Xem [LICENSE](LICENSE).
