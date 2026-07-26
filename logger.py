
import os
import json
from datetime import datetime

LOG_DIR = "logs"
LOG_FILE = os.path.join(LOG_DIR, "run.jsonl")

os.makedirs(LOG_DIR, exist_ok=True)


def log_run(question, answer):
    """
    Appends one JSON object per line to logs/run.jsonl
    Returns the public URL (replace with your deployed domain).
    """

    entry = {
        "timestamp": datetime.utcnow().isoformat() + "Z",
        "question": question,
        "answer": answer
    }

    with open(LOG_FILE, "a", encoding="utf-8") as f:
        f.write(json.dumps(entry, ensure_ascii=False) + "\n")

    # Replace YOUR-RENDER-URL after deployment
    return "https://YOUR-RENDER-URL.onrender.com/logs/run.jsonl"
