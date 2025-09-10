import unittest
import json
from modules.fractals import FractalDetector

class TestFractals(unittest.TestCase):
    def setUp(self):
        # Always load config.json, no manual duplication of params
        with open("config.json") as f:
            self.config = json.load(f)
        self.detector = FractalDetector(self.config)

    def test_detect_fractals(self):
        self.detector.fetch_history()
        self.detector.detect_fractals()

        for symbol in self.config["symbols"]:
            print(f"\n=== {symbol} ===")
            for interval in self.config["intervals"]:
                print(f"--- {interval} ---")
                lines = self.detector.format_fractals(symbol, interval)
                if not lines:
                    print("No fractals found.")
                else:
                    for line in lines:
                        print(line)


if __name__ == "__main__":
    unittest.main()

# python -m tests.test_fractals
# python -m unittest discover -s tests -p "*.py"