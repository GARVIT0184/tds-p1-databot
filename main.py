from fastapi import FastAPI, Request
from telegram_bot import handle_message
import uvicorn

app = FastAPI(title="Data Analyst Telegram Bot")


@app.get("/")
async def root():
    return {"status": "running"}


@app.post("/webhook")
async def webhook(request: Request):
    data = await request.json()
    await handle_message(data)
    return {"ok": True}


if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=False
    )
