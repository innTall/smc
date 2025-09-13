import unittest
from unittest.mock import patch, MagicMock
from src.api.bingx_rest import BingXRestClient
from src.types.models import Candle

class TestBingXRest(unittest.TestCase):

    @patch("src.api.bingx_rest.requests.get")
    def test_get_klines_with_data_wrapper(self, mock_get):
        # Mock BingX response with "data" wrapper
        mock_response = MagicMock()
        mock_response.json.return_value = {
            "code": 0,
            "msg": "",
            "data": [
                {"open": "100", "high": "110", "low": "90", "close": "105", "volume": "1000", "time": 1700000000000}
            ]
        }
        mock_response.status_code = 200
        mock_get.return_value = mock_response

        client = BingXRestClient(api_key="key", secret_key="secret", timezone="Europe/Madrid")
        candles = client.get_klines("BTC-USDT", "1h", 5)

        self.assertEqual(len(candles), 1)
        self.assertIsInstance(candles[0], Candle)
        self.assertEqual(candles[0].open, 100.0)
        self.assertEqual(candles[0].symbol, "BTC-USDT")
        self.assertEqual(candles[0].interval, "1h")

if __name__ == "__main__":
    unittest.main()

# python -m tests.test_bingx_rest
# python -m unittest discover -s tests -p "test_*.py"