from fastapi import FastAPI, Request
import asyncio
import aiosqlite

app = FastAPI()

DB = "subs.db"

@app.post("/webhook/yoomoney")
async def yoomoney_webhook(req: Request):
    data = await req.form()
    label = data.get("label")  # уникальный идентификатор платежа
    status = data.get("status")  # 'success', 'canceled', и т.д.

    if status == "success":
        async with aiosqlite.connect(DB) as db:
            await db.execute("UPDATE payments SET paid=1 WHERE label=?", (label,))
            await db.commit()
            # здесь можно вызвать grant_access через asyncio
            # например через asyncio.create_task(grant_access(...))
    return "OK"
