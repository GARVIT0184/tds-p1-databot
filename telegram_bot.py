
import os
import json
import requests

from llm import solve_question
from logger import log_run

BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
TELEGRAM_API = f"https://api.telegram.org/bot{BOT_TOKEN}"


async def handle_message(update: dict):
    """
    Receives Telegram webhook JSON.
    Extracts the user's message.
    Calls the LLM/data-analysis engine.
    Sends EXACTLY one JSON object back as a Telegram message.
    """

    try:
        message = update.get("message", {})
        chat_id = message.get("chat", {}).get("id")
        text = message.get("text", "")

        if not chat_id or not text:
            return

        # Solve the user's data-analysis question
        answer = solve_question(text)

        # Log the interaction
        log_url = log_run(text, answer)

        # Final response REQUIRED by the assignment
        response = {
            "answer": answer,
            "log_url": log_url
        }

        # Send exactly one JSON object
        requests.post(
            f"{TELEGRAM_API}/sendMessage",
            json={
                "chat_id": chat_id,
                "text": json.dumps(response)
            },
            timeout=30,
        )

    except Exception as e:
        print("Telegram Error:", e)
