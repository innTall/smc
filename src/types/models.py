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
    time: datetime  # localized datetime
