import unittest
from main import format_message

class TestMain(unittest.TestCase):
    def test_format_message(self):
        candle = {"timestamp": 1690000000000, "close": 27345.5}
        config = {"timezone": "UTC"}
        msg = format_message("BTCUSDT", "1h", candle, config)
        self.assertIn("BTCUSDT", msg)
        self.assertIn("1h", msg)
        self.assertIn("27345.5", msg)

if __name__ == "__main__":
    unittest.main()

# python -m tests.test_main
# python -m unittest discover -s tests -p "*.py"