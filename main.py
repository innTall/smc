import json
import logging
from utils.rest_api import get_last_confirmed_candle
from core.telegram_bot import send_signal
from core.signal_engine import format_message
from modules.fractals import FractalDetector
from modules.fractal_break import FractalBreakManager

def setup_logger(config: dict):
    """Setup application logger from config.json."""
    level_str = config.get("logging", {}).get("level", "INFO").upper()
    level = getattr(logging, level_str, logging.INFO)
    logging.basicConfig(
        level=level,
        format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )

    # Silence urllib3 unless explicitly enabled
    if not config.get("debug_requests", False):
        logging.getLogger("urllib3").setLevel(logging.WARNING)

    return logging.getLogger("smc")

def main():
    with open("config.json") as f:
        config = json.load(f)

    logger = setup_logger(config)
    logger.info("Starting bot...")

    # Step 1: (Optional) Send last confirmed candles to Telegram
    if config["send_last_confirmed"]:
        for symbol in config["symbols"]:
            for interval in config["intervals"]:
                try:
                    candle = get_last_confirmed_candle(symbol, interval)
                    message = format_message(symbol, interval, candle, config)
                    logger.debug(f"Sending signal: {message}")
                    send_signal(message)
                except Exception as e:
                    logger.error(f"Failed for {symbol}-{interval}: {e}")

    # Step 2: (Optional) Detect fractals and print normal ones
    if config["print_normal_fractals"]:
        detector = FractalDetector(config)
        detector.fetch_history()
        detector.detect_fractals()

        break_mgr = FractalBreakManager(config)
        break_mgr.process_all(detector.fractals, detector.history)
        
        # ✅ Loop over all symbols and intervals
        for symbol in config["symbols"]:
            for interval in config["intervals"]:
                normals = break_mgr.format_normal_fractals(symbol, interval, detector.tz)
                if normals:
                    print(f"\n=== {symbol} --- {interval} ===")
                    for f in normals:
                        print(f)

if __name__ == "__main__":
    main()

# python main.py