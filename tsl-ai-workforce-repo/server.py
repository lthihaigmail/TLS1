#!/usr/bin/env python3
"""TSL AI Workforce — server multi-employee (AI Sales + AI Customer Service).

    uvicorn server:app --host 0.0.0.0 --port 8000
Endpoints:
    GET  /                 Chat UI demo (chọn nhân viên)
    GET  /health           Kiểm tra sống + danh sách nhân viên
    POST /chat             {message, customer?, employee?} -> reply/decisions/approvals
    POST /webhook/zalo      Adapter Zalo OA (employee? mặc định ai_sales)
    GET  /approvals        Hàng đợi duyệt đang chờ
"""
from __future__ import annotations
from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse, JSONResponse
from tsl import Constitution, AIEmployee, ApprovalQueue, Audit

app = FastAPI(title="TSL AI Workforce", version="1.1")
_C = Constitution.load("constitution/apd-constitution.yaml")
_Q = ApprovalQueue()          # hàng đợi duyệt DÙNG CHUNG toàn tổ chức
_AUD = Audit()
_EMPLOYEES = {eid: AIEmployee(_C, eid, approvals=_Q, audit=_AUD)
              for eid in _C.data.get("ai_workforce", {})}


def _turn(t):
    return {"reply": t.reply,
            "decisions": [{"action": a.name, "verdict": d.verdict, "rule": d.rule, "route": d.route_to}
                          for a, d in t.decisions],
            "approvals": [x["id"] for x in t.approvals]}


def _emp(name): return _EMPLOYEES.get(name or "ai_sales", _EMPLOYEES["ai_sales"])


@app.get("/health")
def health():
    return {"status": "ok", "constitution": _C.id, "version": _C.version,
            "employees": list(_EMPLOYEES)}


@app.post("/chat")
async def chat(req: Request):
    b = await req.json()
    t = _emp(b.get("employee")).handle(b.get("message", ""), b.get("customer"))
    return JSONResponse(_turn(t))


@app.post("/webhook/zalo")
async def zalo(req: Request):
    b = await req.json()
    sender = (b.get("sender") or {}).get("id") or b.get("user_id")
    text = (b.get("message") or {}).get("text") or b.get("text", "")
    t = _emp(b.get("employee")).handle(text, customer=sender)
    return JSONResponse({"reply": t.reply, **_turn(t)})


@app.get("/approvals")
def approvals():
    return JSONResponse(_Q.pending())


@app.get("/", response_class=HTMLResponse)
def home():
    opts = "".join(f'<option value={e}>{e.replace("ai_","AI ").replace("_"," ").title()}</option>' for e in _EMPLOYEES)
    return ("""<!doctype html><html lang=vi><meta charset=utf-8>
<title>TSL AI Workforce — Demo</title>
<style>body{font-family:-apple-system,Arial,sans-serif;max-width:640px;margin:30px auto;padding:0 16px;background:#f5f4ef;color:#1b1b19}
h1{font-size:18px;color:#085041}#log{background:#fff;border:.5px solid #d2cfc4;border-radius:12px;padding:14px;min-height:220px}
.b{margin:8px 0;padding:8px 12px;border-radius:12px;max-width:82%;font-size:14px;line-height:1.5}
.u{background:#efeee8;margin-left:auto;border-radius:12px 12px 2px 12px}.a{background:#e1f5ee;border-radius:12px 12px 12px 2px}
.row{display:flex}.v{font-size:12px;color:#854f0b;margin:4px 0}
select,input{height:40px;padding:0 12px;border:.5px solid #d2cfc4;border-radius:8px;font-size:14px}
input{width:100%;margin-top:10px}</style>
<h1>TSL AI Workforce · Hiến pháp APD</h1>
<label>Nhân viên: <select id=emp>__OPTIONS__</select></label>
<div id=log style=margin-top:10px></div>
<input id=msg placeholder="Nhập tin nhắn khách rồi Enter..." autofocus>
<script>
const log=document.getElementById('log'),msg=document.getElementById('msg'),emp=document.getElementById('emp');
function add(t,cls){const d=document.createElement('div');d.className='row';const b=document.createElement('div');b.className='b '+cls;b.textContent=t;if(cls=='u')d.style.justifyContent='flex-end';d.appendChild(b);log.appendChild(d);log.scrollTop=log.scrollHeight;}
msg.addEventListener('keydown',async e=>{if(e.key!=='Enter'||!msg.value.trim())return;const t=msg.value.trim();msg.value='';add(t,'u');
const r=await fetch('/chat',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({message:t,customer:'demo',employee:emp.value})});
const j=await r.json();add(j.reply,'a');if(j.decisions&&j.decisions.length){const v=document.createElement('div');v.className='v';v.textContent='engine: '+j.decisions.map(d=>d.verdict+(d.route?'→'+d.route:'')).join(', ');log.appendChild(v);}});
</script></html>""").replace("__OPTIONS__", opts)
