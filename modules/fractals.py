import pytz
import logging
from utils import rest_api
from datetime import datetime

logger = logging.getLogger("smc")

class FractalDetector:
    REQUIRED_KEYS = [
        "symbols",
        "intervals",
        "history_limit",
        "fractal_window",
        "price_epsilon",
        "timezone",
    ]

    def __init__(self, config: dict):
        # Validate config
        missing = [k for k in self.REQUIRED_KEYS if k not in config]
        if missing:
            raise ValueError(f"Missing required config keys: {', '.join(missing)}")

        self.config = config
        self.history = {}
        self.fractals = {}
        self.tz = pytz.timezone(config["timezone"])  # required key

    def fetch_history(self):
        """Fetch candles for all symbols and intervals."""
        for symbol in self.config["symbols"]:
            self.history[symbol] = {}
            for interval in self.config["intervals"]:
                try:
                    candles = rest_api.get_last_candles(
                        symbol, interval, limit=self.config["history_limit"]
                    )
                    norm = []
                    for c in candles:
                        if isinstance(c, list):
                            norm.append(
                                {
                                    "closeTime": int(c[6]),
                                    "open": float(c[1]),
                                    "high": float(c[2]),
                                    "low": float(c[3]),
                                    "close": float(c[4]),
                                }
                            )
                        else:
                            # BingX v3 returns "time" = openTime, so we add closeTime manually
                            open_ts = int(c.get("time", c["openTime"]))
                            norm.append(
                                {
                                    "closeTime": open_ts + self._interval_to_ms(interval),
                                    "open": float(c["open"]),
                                    "high": float(c["high"]),
                                    "low": float(c["low"]),
                                    "close": float(c["close"]),
                                }
                            )
                    norm.sort(key=lambda x: x["closeTime"])
                    self.history[symbol][interval] = norm
                except Exception as e:
                    logger.error(f"Failed to fetch history for {symbol}-{interval}: {e}")
                    self.history[symbol][interval] = []

    def detect_fractals(self):
        """Detect fractals for all history."""
        window = self.config["fractal_window"]
        half = window // 2
        eps = self.config["price_epsilon"]

        for symbol, intervals in self.history.items():
            self.fractals[symbol] = {}
            for interval, candles in intervals.items():
                fr_list = []
                for i in range(half, len(candles) - half):
                    center = candles[i]
                    left = candles[i - half:i]
                    right = candles[i + 1:i + 1 + half]

                    if all(center["high"] > n["high"] + eps for n in left + right):
                        fr_list.append(
                            {"type": "HFractal", "time": center["closeTime"], "price": center["high"]}
                        )
                        continue

                    if all(center["low"] < n["low"] - eps for n in left + right):
                        fr_list.append(
                            {"type": "LFractal", "time": center["closeTime"], "price": center["low"]}
                        )

                self.fractals[symbol][interval] = list(reversed(fr_list))

    def format_fractals(self, symbol: str, interval: str):
        """Format fractals list for display."""
        out = []
        for f in self.fractals.get(symbol, {}).get(interval, []):
            ts = datetime.fromtimestamp(f["time"] / 1000, tz=self.tz)
            out.append(f"{f['type']} at {ts.strftime('%H:%M')}, price={f['price']}")
        return out
    
    def _interval_to_ms(self, interval: str) -> int:
        """Convert interval (e.g. '1m', '1h') to milliseconds."""
        unit = interval[-1]
        value = int(interval[:-1])
        if unit == "m":
            return value * 60_000
        if unit == "h":
            return value * 60 * 60_000
        if unit == "d":
            return value * 24 * 60 * 60_000
        raise ValueError(f"Unsupported interval: {interval}")

# python -m modules.fractals