#!/usr/bin/env python3
"""Nghiệm thu TỔNG QUÁT cho MỌI nhân viên trong Hiến pháp.

Với mỗi nhân viên: mọi action 'can' phải CHO PHÉP; mọi action 'cannot' phải bị
CHẶN hoặc CẦN DUYỆT (kèm định tuyến người duyệt nếu có).
    python run_acceptance.py  ->  data/acceptance-report.md
"""
from pathlib import Path
import time
from tsl import Constitution, EnforcementEngine, Action, ALLOW, BLOCK, REQUIRE


def main():
    c = Constitution.load("constitution/apd-constitution.yaml")
    e = EnforcementEngine(c)
    wf = c.data["ai_workforce"]
    out = ["# Báo cáo nghiệm thu — TSL AI Workforce (đủ bộ)", "",
           f"Constitution: {c.id} v{c.version} · {time.strftime('%Y-%m-%d %H:%M:%S')}",
           f"Số nhân viên: **{len(wf)}**", ""]
    total_pass = total = 0
    detail = []
    for eid, prof in wf.items():
        auth = prof.get("authority", {})
        can = auth.get("can", [])
        cannot = auth.get("cannot", [])
        rows, ep, en = [], 0, 0
        for a in can:
            d = e.evaluate(Action(a, employee=eid))
            ok = d.verdict == ALLOW
            ep += ok; en += 1
            rows.append(f"| {a} | CHO PHÉP | {d.verdict} | {'ĐẠT' if ok else 'SAI'} |")
        for a in cannot:
            d = e.evaluate(Action(a, employee=eid))
            ok = d.verdict in (BLOCK, REQUIRE)
            ep += ok; en += 1
            route = f" → {d.route_to}" if d.route_to else ""
            rows.append(f"| {a} | CHẶN/DUYỆT | {d.verdict}{route} | {'ĐẠT' if ok else 'SAI'} |")
        total_pass += ep; total += en
        title = eid.replace("ai_", "AI ").replace("_", " ").title()
        detail += [f"## {title} — {ep}/{en} ĐẠT", "",
                   "| Action | Kỳ vọng | Engine | KQ |", "|---|---|---|---|", *rows, ""]
    out.insert(4, f"**Tổng: {total_pass}/{total} ĐẠT** — "
              + ("PASS, đủ điều kiện nghiệm thu." if total_pass == total else "FAIL, cần rà lại.") + "\n")
    out += detail
    Path("data").mkdir(exist_ok=True)
    Path("data/acceptance-report.md").write_text("\n".join(out), encoding="utf-8")
    print(f"Nhân viên: {len(wf)} | Nghiệm thu: {total_pass}/{total} "
          + ("PASS" if total_pass == total else "FAIL"))
    print("-> data/acceptance-report.md")
    return 0 if total_pass == total else 1


if __name__ == "__main__":
    raise SystemExit(main())
