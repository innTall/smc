import logging
from src.api.bingx_rest import BingXRestClient
from src.modules.fractals import detect_fractals
from src.settings import config
from src.utils.timeutils import format_dt

# --- Setup logging ---
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# --- Initialize REST client (no keys needed for public endpoints) ---
client = BingXRestClient()

# --- Parameters from config.json ---
symbol = config["symbols"][0]
interval = config["intervals"][0]
history_limit = config["history_limit"]
fractal_window = config["fractal_window"]

logger.info(f"Fetching candles for {symbol} {interval}, limit={history_limit}")
candles = client.get_klines(symbol, interval, limit=history_limit)

logger.info(f"Detecting fractals (window={fractal_window})")
fractals = detect_fractals(candles, symbol, interval, fractal_window)

print(f"\n--- {symbol} {interval} ---")
for f in fractals:
    print(f"{f.type} | {f.level} | {format_dt(f.time)}")

# python -m src.scripts.run_fractals