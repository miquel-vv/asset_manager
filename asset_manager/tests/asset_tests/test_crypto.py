import unittest
from unittest.mock import patch, MagicMock
from asset_manager.connectors.KrakenConnector import KrakenConnector
from asset_manager.assets.Crypto import Crypto
from asset_manager.mappers.PriceMapper import PriceMapper
import pandas as pd

class CryptoTest(unittest.TestCase):
    def setUp(self):
        self.prices = pd.read_pickle("asset_manager/tests/test_data/etheur.pkl")
        with patch.object(PriceMapper, "get_prices", return_value=self.prices):
            self.crypto1 = Crypto("ETH")
            self.crypto2 = Crypto("BT")

        self.last_date = self.prices.index[-1] 

    def test_load_prices(self):
        self.crypto1.kraken_connector.get_prices = MagicMock(return_value="UP-TO-DATE")
        self.crypto1.load_prices(1)
        self.crypto1.kraken_connector.get_prices.assert_called_with(self.last_date, "ETHEUR", 1)

        self.crypto2.kraken_connector.get_prices = MagicMock(return_value="UP-TO-DATE")
        self.crypto2.load_prices(5)
        self.crypto2.kraken_connector.get_prices.assert_called_with(self.last_date, "XBTEUR", 5)

        self.crypto2.prices = self.crypto2.prices.iloc[0:0]
        self.crypto2.kraken_connector.get_prices = MagicMock(return_value=self.prices[:5])
        self.crypto2.price_mapper.save_prices = MagicMock(return_value=True)
        self.crypto2.load_prices(1)
        self.assertEqual("BT", self.crypto2.price_mapper.save_prices.call_args[0][0])
        self.assertEqual(1 , self.crypto2.price_mapper.save_prices.call_args[0][2])
        self.assertTrue(self.prices[:5].equals(self.crypto2.price_mapper.save_prices.call_args[0][1]))

        self.crypto2.kraken_connector.get_prices = MagicMock(return_value=self.prices[5:])
        self.crypto2.price_mapper.save_prices = MagicMock(return_value=True)
        self.crypto2.load_prices(1)
        self.assertTrue(self.prices.equals(self.crypto2.prices), "Prices df was not appended correctly to the existing prices table.")