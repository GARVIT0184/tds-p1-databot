import os
from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.responses import FileResponse, JSONResponse

from telegram_bot import start_polling
from logger import LOG_FILE


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Start Telegram polling in background
    start_polling()
    yield


app = FastAPI(lifespan=lifespan)


@app.get("/")
async def root():
    return {"ok": True}


@app.get("/health")
async def health():
    return {
        "ok": True,
        "status": "running"
    }


@app.get("/run.jsonl")
async def runlog():
    if not os.path.exists(LOG_FILE):
        open(LOG_FILE, "w").close()

    return FileResponse(
        LOG_FILE,
        media_type="application/json"
    )


@app.exception_handler(Exception)
async def all_exception_handler(request, exc):
    return JSONResponse(
        status_code=500,
        content={
            "ok": False,
            "error": str(exc)
        }
    )
