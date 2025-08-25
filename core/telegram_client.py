import os
import time
import requests
from dotenv import load_dotenv

class TelegramClient:
    def __init__(self, config):
        load_dotenv()  # ensure .env is loaded

        # From config.json
        self.enabled = config["telegram"].get("enabled", False)
        self.debug_signals = config["telegram"].get("debug_signals", False)

        # From .env (never in config.json)
        self.token = os.getenv("TELEGRAM_BOT_TOKEN")
        self.chat_id = os.getenv("TELEGRAM_CHAT_ID")

        # Init state
        self._last_sent = 0

        print(
            f"[Telegram INIT] enabled={self.enabled}, "
            f"debug_signals={self.debug_signals}, "
            f"token={'yes' if self.token else 'no'}, "
            f"chat_id={'yes' if self.chat_id else 'no'}"
        )

    def send(self, text):
        if not self.enabled:
            print("[Telegram SEND] skipped (disabled in config)")
            return

        if not self.token or not self.chat_id:
            print("[Telegram SEND] skipped (missing credentials in .env)")
            return

        print(f"[Telegram SEND] trying: {text}")
        
        # Optional: flood control (avoid Telegram ban if signals spam)
        now = time.time()
        if now - self._last_sent < 1:  # 1 sec gap between messages
            return
        self._last_sent = now

        url = f"https://api.telegram.org/bot{self.token}/sendMessage"
        try:
            r = requests.post(url, json={"chat_id": self.chat_id, "text": text})
            if r.status_code != 200:
                print(f"[Telegram ERROR] {r.status_code}: {r.text}")
            else:
                print(f"[Telegram OK] sent: {text}")
        except Exception as e:
            print(f"[Telegram ERROR] Exception: {e}")

# python core/telegram_client.py