#!/usr/bin/env python3
"""Console chat: nhập tin nhắn khách, xem AI phản hồi + phán quyết engine.

    python console.py           # dùng LLM mock
    TSL_LLM_PROVIDER=openai python console.py   # dùng LLM thật (cần OPENAI_API_KEY)
"""
from tsl import Constitution, AIEmployee


def main():
    c = Constitution.load("constitution/apd-constitution.yaml")
    emp = AIEmployee(c, "ai_sales")
    print(f"AI Sales ({c.company.get('short_name','')}) sẵn sàng. Gõ 'quit' để thoát.\n")
    while True:
        try:
            msg = input("Khách > ").strip()
        except (EOFError, KeyboardInterrupt):
            break
        if msg.lower() in ("quit", "exit", ""):
            break
        turn = emp.handle(msg)
        print(f"AI    > {turn.reply}\n")


if __name__ == "__main__":
    main()
