#!/usr/bin/env python3
"""Demo TẤT CẢ nhân viên: mỗi con thử 1 action 'can' và 1 action 'cannot'."""
from tsl import Constitution, AIEmployee, EnforcementEngine, Action, MockProvider

ICON = {"ALLOW": "[ALLOW]   ", "BLOCK": "[BLOCK]   ", "REQUIRE_HUMAN_APPROVAL": "[APPROVE?]"}


def main():
    c = Constitution.load("constitution/apd-constitution.yaml")
    e = EnforcementEngine(c)
    wf = c.data["ai_workforce"]
    print(f"Constitution {c.id} v{c.version} | {len(wf)} nhân viên AI trên cùng Hiến pháp")
    print("=" * 78)
    for eid, prof in wf.items():
        auth = prof.get("authority", {})
        title = eid.replace("ai_", "AI ").replace("_", " ").title()
        samples = []
        if auth.get("can"):
            samples.append(auth["can"][0])
        if auth.get("cannot"):
            samples.append(auth["cannot"][0])
        line = []
        for a in samples:
            d = e.evaluate(Action(a, employee=eid))
            route = f"→{d.route_to}" if d.route_to else ""
            line.append(f"{ICON.get(d.verdict, d.verdict).strip()} {a}{(' '+route) if route else ''}")
        print(f"{title:22} | " + "   |   ".join(line))
    print("=" * 78)
    print("Cùng runtime + engine. Thêm nhân viên = thêm khối Hiến pháp. Không đụng code.")


if __name__ == "__main__":
    main()
