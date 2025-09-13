import os
import requests
import logging

class TelegramClient:
    def __init__(self, bot_token: str = None, chat_id: str = None):
        self.bot_token = bot_token or os.getenv("TELEGRAM_BOT_TOKEN")
        self.chat_id = chat_id or os.getenv("TELEGRAM_CHAT_ID")
        self.logger = logging.getLogger(__name__)
        if not self.bot_token or not self.chat_id:
            raise ValueError("Telegram BOT_TOKEN and CHAT_ID must be provided")

    def send_message(self, text: str):
        url = f"https://api.telegram.org/bot{self.bot_token}/sendMessage"
        payload = {"chat_id": self.chat_id, "text": text}
        try:
            resp = requests.post(url, json=payload, timeout=10)
            resp.raise_for_status()
            self.logger.info(f"Message sent to Telegram chat {self.chat_id}")
            return resp.json()
        except Exception as e:
            self.logger.error(f"Failed to send message: {e}")
            raise
