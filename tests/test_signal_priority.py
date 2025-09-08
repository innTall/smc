import unittest
from datetime import datetime
from core import signal_engine  # new module we will create

@unittest.skip("Priority logic removed for now")
class TestSignalPriority(unittest.TestCase):
    def test_high_tf_priority(self):
        # fake candle closes at the same timestamp
        fake_data = {
            "BTCUSDT": {
                "15m": {"timestamp": 1690000000000, "close": 27345.5},
                "1h": {"timestamp": 1690000000000, "close": 27350.0},
                "4h": None
            }
        }

        selected = signal_engine.select_high_tf(fake_data)
        # Should pick 1h, because 4h is None
        self.assertEqual(selected["interval"], "1h")
        self.assertEqual(selected["close"], 27350.0)

    def test_highest_tf_wins(self):
        fake_data = {
            "BTCUSDT": {
                "15m": {"timestamp": 1690000000000, "close": 27345.5},
                "1h": {"timestamp": 1690000000000, "close": 27350.0},
                "4h": {"timestamp": 1690000000000, "close": 27400.0}
            }
        }
        selected = signal_engine.select_high_tf(fake_data)
        # 4h has priority
        self.assertEqual(selected["interval"], "4h")
        self.assertEqual(selected["close"], 27400.0)

if __name__ == "__main__":
    unittest.main()

# python -m tests.test_signal_priority
# python -m unittest discover -s tests -p "test_*.py"