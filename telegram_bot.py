import os
import json
import threading
import time
import requests

from llm import solve_question
from logger import log_run

BOT_TOKEN = os.getenv("BOT_TOKEN") or os.getenv("TELEGRAM_BOT_TOKEN")

if not BOT_TOKEN:
    raise RuntimeError("BOT_TOKEN not found.")

BASE_URL = f"https://api.telegram.org/bot{BOT_TOKEN}"

offset = 0

# Keep last conversations (multi-turn)
chat_history = {}


def send_json(chat_id, obj):
    """
    Send EXACTLY one JSON object.
    """
    requests.post(
        f"{BASE_URL}/sendMessage",
        json={
            "chat_id": chat_id,
            "text": json.dumps(obj, ensure_ascii=False)
        },
        timeout=60,
    )


def get_history(chat_id):
    if chat_id not in chat_history:
        chat_history[chat_id] = []
    return chat_history[chat_id]


def append_history(chat_id, role, text):
    history = get_history(chat_id)

    history.append(
        {
            "role": role,
            "content": text
        }
    )

    # Keep only last 20 turns
    if len(history) > 20:
        history[:] = history[-20:]


def process_message(message):
    chat_id = message["chat"]["id"]

    text = message.get("text", "")

    append_history(chat_id, "user", text)

    history = get_history(chat_id)

    try:

        answer = solve_question(history)

        append_history(
            chat_id,
            "assistant",
            json.dumps(answer)
        )

        log_url = log_run(
            text,
            answer
        )

        reply = {
            "answer": answer,
            "log_url": log_url
        }

    except Exception:

        reply = {
            "answer": "internal error",
            "log_url": log_run(
                text,
                "internal error"
            ),
        }

    send_json(chat_id, reply)


def poll():
    global offset

    while True:

        try:

            response = requests.get(
                f"{BASE_URL}/getUpdates",
                params={
                    "timeout": 60,
                    "offset": offset,
                },
                timeout=70,
            )

            updates = response.json()

            if not updates["ok"]:
                continue

            for update in updates["result"]:

                offset = update["update_id"] + 1

                if "message" not in update:
                    continue

                process_message(update["message"])

        except Exception as e:
            print(e)
            time.sleep(3)


def start_polling():
    thread = threading.Thread(
        target=poll,
        daemon=True,
    )

    thread.start()
