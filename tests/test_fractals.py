import unittest
from datetime import datetime, timedelta
from src.types.models import Candle
from src.modules.fractals import detect_fractals

class TestFractals(unittest.TestCase):
    def setUp(self):
        # Create artificial candle data
        base_time = datetime(2025, 9, 13, 0, 0)
        self.candles = []
        prices = [10, 12, 15, 20, 18, 16, 14, 12, 8, 6, 7, 9, 11, 13, 10]
        for i, p in enumerate(prices):
            self.candles.append(
                Candle(
                    symbol="TEST",
                    interval="1h",
                    open=p,
                    high=p+1,
                    low=p-1,
                    close=p,
                    volume=1.0,
                    time=base_time + timedelta(hours=i)
                )
            )

    def test_detect_fractals(self):
        fractals = detect_fractals(self.candles, "TEST", "1h", fractal_window=3)
        self.assertGreater(len(fractals), 0)
        types = {f.type for f in fractals}
        self.assertIn("HFractal", types)
        self.assertIn("LFractal", types)

if __name__ == "__main__":
    unittest.main()

# python -m tests.test_fractals
# python -m unittest tests/test_fractals.py