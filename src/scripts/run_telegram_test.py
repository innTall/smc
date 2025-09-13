import logging
from src.api.telegram import TelegramClient
from dotenv import load_dotenv

load_dotenv()  # load BOT_TOKEN, CHAT_ID from .env

logging.basicConfig(level=logging.INFO)

def main():
    client = TelegramClient()
    client.send_message("Test message from fractal bot ✅")

if __name__ == "__main__":
    main()

# python -m src.scripts.run_telegram_test