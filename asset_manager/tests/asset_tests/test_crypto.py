import unittest
from unittest.mock import patch, MagicMock
from asset_manager.connectors.KrakenConnector import KrakenConnector
from asset_manager.assets.Crypto import Crypto
from asset_manager.mappers.PriceMapper import PriceMapper
import pandas as pd

class CryptoTest(unittest.TestCase):
    def setUp(self):
        prices = pd.read_pickle("asset_manager/tests/test_data/etheur.pkl")
        with patch.object(PriceMapper, "get_prices", return_value=prices):
            self.crypto1 = Crypto("ETH")
            self.crypto2 = Crypto("BT")

        self.last_date = prices.index[-1] 

    def test_load_prices(self):
        self.crypto1.kraken_connector.get_prices = MagicMock(return_value="UP-TO-DATE")
        self.crypto1.load_prices(1)
        self.crypto1.kraken_connector.get_prices.assert_called_with(self.last_date, "XETHZEUR", 1)

        self.crypto2.kraken_connector.get_prices = MagicMock(return_value="UP-TO-DATE")
        self.crypto2.load_prices(5)
        self.crypto2.kraken_connector.get_prices.assert_called_with(self.last_date, "XXBTZEUR", 5)
        