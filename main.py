from core.websocket_manager import WebSocketManager
from core.signal_engine import SignalEngine
from core.telegram_client import TelegramClient
from utils.logger import setup_logger
import json
from dotenv import load_dotenv
load_dotenv()  # this will load .env into os.environ

def load_config():
    with open("config.json", "r") as f:
        return json.load(f)

def main():
    config = load_config()
    logger = setup_logger(config["logging"]["level"])

    if config.get("source") == "api":
        raise RuntimeError(
            "[FATAL] Production bot cannot use API candles! Set source='ws' in config.json"
        )

    telegram = TelegramClient(config)
    engine = SignalEngine(config, telegram)

    ws = WebSocketManager(config, engine)
    ws.run_forever()

if __name__ == "__main__":
    main()

# python main.py