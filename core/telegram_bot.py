import os
import requests
import logging
from dotenv import load_dotenv

load_dotenv()
logger = logging.getLogger("smc")

BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")


def send_signal(message: str) -> None:
    if not BOT_TOKEN or not CHAT_ID:
        raise ValueError("Telegram credentials not found in .env")

    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    payload = {"chat_id": CHAT_ID, "text": message}
    logger.debug(f"Sending Telegram message: {payload}")

    response = requests.post(url, json=payload)
    if response.status_code != 200:
        logger.error(f"Telegram error: {response.text}")
    response.raise_for_status()
