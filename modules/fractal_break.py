import logging
from datetime import datetime

logger = logging.getLogger("smc")

class FractalBreakManager:
    def __init__(self, config: dict):
        self.config = config
        self.breakouts = {}

    def detect_breakouts(self, symbol: str, interval: str, candles: list, fractals: list):
        """
        Detect breakout of fractals based on high/low only.
        - HFractal is broken if any later candle's high > fractal.high
        - LFractal is broken if any later candle's low < fractal.low
        """

        results = []
        for f in fractals:
            broken = False
            if f["type"] == "HFractal":
                for c in candles:
                    if c["closeTime"] > f["time"] and c["high"] > f["price"]:
                        if self.config["print_breakouts"]:
                            logger.info(
                                f"HBreak detected for {symbol}-{interval} at "
                                f"{datetime.fromtimestamp(c['closeTime'] / 1000)}, "
                                f"fractal={f['price']} candle.high={c['high']}"
                            )
                        broken = True
                        break

            elif f["type"] == "LFractal":
                for c in candles:
                    if c["closeTime"] > f["time"] and c["low"] < f["price"]:
                        if self.config["print_breakouts"]:
                            logger.info(
                                f"LBreak detected for {symbol}-{interval} at "
                                f"{datetime.fromtimestamp(c['closeTime'] / 1000)}, "
                                f"fractal={f['price']} candle.low={c['low']}"
                            )
                        broken = True
                        break

            if not broken:
                results.append(f)

        # Store normal (not broken) fractals
        self.breakouts[(symbol, interval)] = results
        return results
    
    def process_all(self, fractals_dict: dict, history_dict: dict):
        """Run breakout detection for all symbols/intervals."""
        for symbol, intervals in fractals_dict.items():
            for interval, fractals in intervals.items():
                candles = history_dict[symbol][interval]
                self.detect_breakouts(symbol, interval, candles, fractals)

    def format_normal_fractals(self, symbol: str, interval: str, tz):
        """Return normal (not broken) fractals formatted for printing."""
        out = []
        for f in self.breakouts.get((symbol, interval), []):
            ts = datetime.fromtimestamp(f["time"] / 1000, tz=tz)
            out.append(f"{f['type']} at {ts.strftime('%H:%M')}, price={f['price']}")
        return out
