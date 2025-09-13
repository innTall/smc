from dataclasses import dataclass
from datetime import datetime

@dataclass
class Candle:
    symbol: str
    interval: str
    open: float
    high: float
    low: float
    close: float
    volume: float
    time: datetime

@dataclass
class Fractal:
    symbol: str
    interval: str
    time: datetime      # time of the central candle
    type: str           # "HFractal" or "LFractal"
    level: float        # high (HFractal) or low (LFractal) # localized datetime
