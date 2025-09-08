import json
import logging
from utils.rest_api import get_last_confirmed_candle, get_last_candles
from core.telegram_bot import send_signal
from core.signal_engine import format_message

def setup_logger(config: dict):
    level_str = config.get("logging", {}).get("level", "INFO").upper()
    level = getattr(logging, level_str, logging.INFO)
    logging.basicConfig(
        level=level,
        format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )
    return logging.getLogger("smc")

def main():
    with open("config.json") as f:
        config = json.load(f)

    logger = setup_logger(config)
    logger.info("Starting bot...")

    # Step 1: (Optional) Send last confirmed candles to Telegram
    if config.get("send_last_confirmed", False):
        for symbol in config["symbols"]:
            for interval in config["intervals"]:
                try:
                    candle = get_last_confirmed_candle(symbol, interval)
                    message = format_message(symbol, interval, candle, config)
                    logger.debug(f"Sending signal: {message}")
                    send_signal(message)
                except Exception as e:
                    logger.error(f"Failed for {symbol}-{interval}: {e}")

    # Step 2: (Optional) Print last 10 candles to terminal
    if config.get("print_last_candles", False):
        for symbol in config["symbols"]:
            for interval in config["intervals"]:
                try:
                    candles = get_last_candles(symbol, interval, limit=10)
                    logger.debug(f"Fetched last 10 {symbol} {interval} candles")
                    for c in candles:
                        logger.debug(c)
                except Exception as e:
                    logger.warning(f"Could not fetch history for {symbol}-{interval}: {e}")

if __name__ == "__main__":
    main()

# python main.py