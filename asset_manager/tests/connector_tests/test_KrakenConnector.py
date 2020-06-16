import unittest
from unittest import mock
from datetime import datetime, timezone
import requests
import json
import pandas as pd
from asset_manager.connectors import KrakenConnector

def mock_response_kraken(*args, **kwargs):
    class MockRespons():
        def __init__(self, data, code):
            self.data = data
            self.status_code = code

        def json():
            return self.data
    
    if args[0] == "https://api.kraken.com/0/public/Time":
        with open("test_data/servertime.json") as f:
            data = json.load(f)
        return MockResponse(data, 200)
    elif args[0] == "https://api.kraken.com/0/public/OHLC?since=1592125740&pair=ETHEUR":
        with open("test_data/etheur.json") as f:
            data = json.load(f)
        return MockResponse(data, 200)
    else:
        return MockResponse({'error': 'URL not found'},404)

class KrakenConnectorTest(unittest.TestCase):
    def test_pair(self):
        kc = KrakenConnector("XETHZEUR")
        self.assertEqual(kc.asset_pair, "XETHZEUR")
    
    @mock.patch('requests.get', side_effect = mock_response_kraken)
    def test_get_data(self, mocked_get):
        test_data = pd.read_pickle('asset_manager/tests/test_data/etheur.pkl')
        kc = KrakenConnector("XETHZEUR")
        start_date = datetime(2020, 6, 14, 9, 10, tzinfo=timezone.utc)
        result = kc.get_data(start_date,'s')

        self.assertTrue(test_data.equals(result), 
                        "Data gathered through (mocked) api call did not equal dataframe from pickle (etheur.pkl)")


if __name__ == "__main__":
    unittest.main()