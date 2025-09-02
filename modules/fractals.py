class FractalDetector:
    def __init__(self, window=5):
        if window % 2 == 0 or window < 3:
            raise ValueError("fractal_window must be odd and >= 3")
        self.window = window
        self.half = window // 2

    def detect(self, candles):
        """
        Detect fractals in given candles list.
        Returns a list of fractal dicts.
        """
        if len(candles) < self.window:
            return []

        fractals = []
        for i in range(self.half, len(candles) - self.half):
            segment = candles[i - self.half : i + self.half + 1]
            center = candles[i]

            high = max(c["high"] for j, c in enumerate(segment) if j != self.half)
            low = min(c["low"] for j, c in enumerate(segment) if j != self.half)

            # HFractal (high fractal / bearish)
            if center["high"] > high:
                fractals.append({
                    "time": center["time"],
                    "price": center["high"],
                    "type": "HFractal",
                    "broken": False,
                    "triggered": False,
                })


            # LFractal (low fractal / bullish)
            if center["low"] < low:
                fractals.append({
                    "time": center["time"],
                    "price": center["low"],
                    "type": "LFractal",
                    "broken": False,
                    "triggered": False,
                })
        return fractals

    def last_fractal(self, candles, ftype=None):
        """
        Return the most recent fractal of given type ("LFractal"/"HFractal")
        """
        fractals = self.detect(candles)
        if not fractals:
            return None

        if ftype:
            for f in reversed(fractals):
                if f["type"] == ftype:
                    return f
            return None
        return fractals[-1]

def filter_normal_fractals(fractals, candles):
    """
    Mark fractals as broken or not, return only unbroken (normal) fractals.
    """
    results = []
    for f in fractals:
        candles_after = [c for c in candles if c["time"] > f["time"]]
        
        if f["type"] == "HFractal":
            f["broken"] = any(c["close"] > f["price"] for c in candles_after)
        else:  # LFractal
            f["broken"] = any(c["close"] < f["price"] for c in candles_after)
        
        if not f["broken"]:
            results.append(f)
    
    return results