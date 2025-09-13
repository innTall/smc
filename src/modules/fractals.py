from typing import List
from src.types.models import Candle, Fractal

def detect_fractals(
    candles: List[Candle],
    symbol: str,
    interval: str,
    fractal_window: int
) -> List[Fractal]:
    """
    Detect all fractals in the given candle history.
    fractal_window must be an odd number >= 3.
    """
    if fractal_window < 3 or fractal_window % 2 == 0:
        raise ValueError("fractal_window must be odd and >= 3")

    n = (fractal_window - 1) // 2
    fractals: List[Fractal] = []

    for i in range(n, len(candles) - n):
        center = candles[i]
        left = candles[i-n : i]
        right = candles[i+1 : i+n+1]

        # HFractal (bearish fractal at highs)
        if all(center.high > c.high for c in left + right):
            fractals.append(
                Fractal(
                    symbol=symbol,
                    interval=interval,
                    time=center.time,
                    type="HFractal",
                    level=center.high
                )
            )

        # LFractal (bullish fractal at lows)
        if all(center.low < c.low for c in left + right):
            fractals.append(
                Fractal(
                    symbol=symbol,
                    interval=interval,
                    time=center.time,
                    type="LFractal",
                    level=center.low
                )
            )

    return fractals
