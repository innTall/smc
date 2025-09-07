import json
import logging
from datetime import datetime, timezone

from utils.rest_api import get_last_confirmed_candle, get_last_candles
from core.telegram_bot import send_signal


def setup_logger(config: dict):
    level_str = config.get("logging", {}).get("level", "INFO").upper()
    level = getattr(logging, level_str, logging.INFO)
    logging.basicConfig(
        level=level,
        format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )
    return logging.getLogger("smc")


def format_message(symbol: str, interval: str, candle: dict) -> str:
    ts = datetime.fromtimestamp(candle["timestamp"] / 1000, tz=timezone.utc)
    return (
        f"Symbol: {symbol}\n"
        f"Interval: {interval}\n"
        f"Last confirmed Close: {candle['close']}\n"
        f"Timestamp: {ts.strftime('%Y-%m-%d %H:%M UTC')}"
    )


def main():
    with open("config.json") as f:
        config = json.load(f)

    logger = setup_logger(config)
    logger.info("Starting bot...")

    for symbol in config["symbols"]:
        for interval in config["intervals"]:
            try:
                candle = get_last_confirmed_candle(symbol, interval)
                message = format_message(symbol, interval, candle)
                logger.debug(f"Sending signal: {message}")
                send_signal(message)
            except Exception as e:
                logger.error(f"Failed for {symbol}-{interval}: {e}")

    # Example: fetch last 10 candles BTCUSDT, 1h
    candles = get_last_candles("BTCUSDT", "1h", limit=10)
    logger.debug("Fetched last 10 BTCUSDT 1h candles")
    for c in candles:
        logger.debug(c)


if __name__ == "__main__":
    main()

# python main.py