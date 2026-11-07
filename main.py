import os
import json
import logging
from pathlib import Path

import httpx
from fastapi import FastAPI, Request, HTTPException
from fastapi.responses import FileResponse, JSONResponse
from fastapi.staticfiles import StaticFiles

logging.basicConfig(level=logging.INFO)
log = logging.getLogger("gameverse")

BOT_TOKEN = os.getenv("BOT_TOKEN", "").strip()
APP_URL = os.getenv("APP_URL", "").strip().rstrip("/")
WEBHOOK_SECRET = os.getenv("WEBHOOK_SECRET", "").strip()
BASE_DIR = Path(__file__).resolve().parent
STATIC_DIR = BASE_DIR / "static"

app = FastAPI(title="GameVerse Telegram Mini App")
app.mount("/static", StaticFiles(directory=STATIC_DIR), name="static")


async def telegram(method: str, payload: dict):
    if not BOT_TOKEN:
        return None
    async with httpx.AsyncClient(timeout=15) as client:
        response = await client.post(
            f"https://api.telegram.org/bot{BOT_TOKEN}/{method}",
            json=payload,
        )
        response.raise_for_status()
        data = response.json()
        if not data.get("ok"):
            raise RuntimeError(data.get("description", "Telegram API error"))
        return data.get("result")


@app.on_event("startup")
async def configure_webhook():
    if BOT_TOKEN and APP_URL:
        try:
            payload = {"url": f"{APP_URL}/telegram/webhook"}
            if WEBHOOK_SECRET:
                payload["secret_token"] = WEBHOOK_SECRET
            await telegram("setWebhook", payload)
            log.info("Telegram webhook configured")
        except Exception:
            log.exception("Could not configure Telegram webhook")


@app.get("/")
async def home():
    return FileResponse(STATIC_DIR / "index.html")


@app.get("/sw.js")
async def service_worker():
    return FileResponse(
        STATIC_DIR / "sw.js",
        media_type="application/javascript",
        headers={"Service-Worker-Allowed": "/"},
    )

@app.get("/health")
async def health():
    return {"status": "ok", "app": "GameVerse", "bot_configured": bool(BOT_TOKEN)}


@app.post("/telegram/webhook")
async def telegram_webhook(request: Request):
    if not BOT_TOKEN:
        raise HTTPException(status_code=503, detail="Bot token is not configured")
    if WEBHOOK_SECRET and request.headers.get("X-Telegram-Bot-Api-Secret-Token") != WEBHOOK_SECRET:
        raise HTTPException(status_code=403, detail="Invalid webhook secret")

    update = await request.json()
    message = update.get("message") or update.get("edited_message") or {}
    chat = message.get("chat", {})
    text = (message.get("text") or "").strip()
    chat_id = chat.get("id")

    if chat_id and text.startswith("/start"):
        if APP_URL:
            reply_markup = {
                "inline_keyboard": [[{
                    "text": "🎮 Open GameVerse",
                    "web_app": {"url": APP_URL},
                }]]
            }
            reply = "Welcome to GameVerse! Choose a game and have fun."
        else:
            reply_markup = None
            reply = "GameVerse is starting up. Please try again shortly."
        payload = {"chat_id": chat_id, "text": reply}
        if reply_markup:
            payload["reply_markup"] = reply_markup
        await telegram("sendMessage", payload)
    elif chat_id and text.startswith("/help"):
        await telegram("sendMessage", {
            "chat_id": chat_id,
            "text": "Send /start to open GameVerse. Choose a game from the mini app."
        })
    return JSONResponse({"ok": True})


@app.get("/api/config")
async def config():
    return {"app_name": "GameVerse", "telegram_enabled": bool(BOT_TOKEN)}
