import json
import os
import logging
from pathlib import Path

from src.api.bingx_rest import BingXRestClient

# Project root = one level above "src"
BASE_DIR = Path(__file__).resolve().parent.parent.parent

with open(BASE_DIR / "config.json", "r", encoding="utf-8") as f:
    config = json.load(f)

# For now secrets are not used, keep empty
API_KEY = os.getenv("BINGX_API_KEY", "")
SECRET_KEY = os.getenv("BINGX_SECRET_KEY", "")

def main():
    logging.basicConfig(level=logging.INFO)

    client = BingXRestClient(
        api_key=API_KEY,
        secret_key=SECRET_KEY,
        timezone=config.get("timezone", "UTC"),
    )

    symbols = config["symbols"]
    intervals = config["intervals"]
    limit = config.get("last_values", 5)

    for symbol in symbols:
        for interval in intervals:
            try:
                candles = client.get_klines(symbol, interval, limit=limit)
                print(f"\n--- {symbol} {interval} ---")
                for c in candles:
                    print(c)
            except Exception as e:
                logging.error(f"Error fetching {symbol} {interval}: {e}")

if __name__ == "__main__":
    main()

# python -m src.scripts.run_fetch