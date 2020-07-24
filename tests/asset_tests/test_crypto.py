import unittest
from unittest.mock import patch, MagicMock
from asset_manager.connectors.KrakenConnector import KrakenConnector
from asset_manager.assets.Crypto import Crypto
from asset_manager.mappers.PriceMapper import PriceMapper
from asset_manager.mappers.MapperConnection import MapperConnection
import pandas as pd

class CryptoTest(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        MapperConnection("testengine")

    def setUp(self):
        self.prices = pd.read_pickle("tests/test_data/etheur.pkl")
        self.crypto1 = Crypto("T")
        self.crypto2 = Crypto("T2")

        self.last_date = self.prices.index[-1] 

    def test_update_prices(self):
        self.crypto1.kraken_connector.get_prices = MagicMock(return_value="UP-TO-DATE")
        with patch.object(PriceMapper, "get_last_saved_date", return_value=self.last_date):
            self.crypto1.update_prices(1)
        self.crypto1.kraken_connector.get_prices.assert_called_with(self.last_date, "XXTEUR", 1)

        self.crypto2.kraken_connector.get_prices = MagicMock(return_value="UP-TO-DATE")
        with patch.object(PriceMapper, "get_last_saved_date", return_value=self.last_date):
            self.crypto2.update_prices(5)
        self.crypto2.kraken_connector.get_prices.assert_called_with(self.last_date, "XT2EUR", 5)

        self.crypto2.kraken_connector.get_prices = MagicMock(return_value=self.prices[:5])
        self.crypto2.price_mapper.save_prices = MagicMock(return_value=True)
        with patch.object(PriceMapper, "get_last_saved_date", return_value=self.prices.index[0]):
            self.crypto2.update_prices(1)
        self.assertEqual("T2", self.crypto2.price_mapper.save_prices.call_args[0][0])
        self.assertEqual(1 , self.crypto2.price_mapper.save_prices.call_args[0][2])
        self.assertTrue(self.prices[:5].equals(self.crypto2.price_mapper.save_prices.call_args[0][1]))

        self.crypto2.kraken_connector.get_prices = MagicMock(return_value=self.prices[5:])
        self.crypto2.price_mapper.save_prices = MagicMock(return_value=True)
        with patch.object(PriceMapper, "get_last_saved_date", return_value=self.prices.index[4]):
            self.crypto2.update_prices(1)
        self.assertTrue(self.prices.equals(self.crypto2.prices), "Prices df was not appended correctly to the existing prices table.")
    
    def test_clean_prices(self):
        one_gap = pd.read_pickle("tests/test_data/gaps.pkl")
        two_gaps = one_gap.drop(one_gap.index[2])
        one_gap_filled = pd.read_pickle("tests/test_data/gaps_filled.pkl")
        two_gaps_filled = pd.read_pickle("tests/test_data/two_gaps_filled.pkl")

        self.crypto1.prices=one_gap
        self.crypto1.clean_prices()
        self.assertTrue(self.crypto1.prices.equals(one_gap_filled), "The gaps in the prices table were not filled correctly.")
        self.assertTrue(self.crypto1.prices.loc[self.crypto1.prices.origin=="O"].equals(one_gap), "The original data was altered during the cleaning process.")

        self.crypto1.prices=two_gaps
        self.crypto1.clean_prices()
        self.assertTrue(self.crypto1.prices.equals(two_gaps_filled), "The gaps in the prices table were not filled correctly.")
        self.assertTrue(self.crypto1.prices.loc[self.crypto1.prices.origin=="O"].equals(two_gaps), "The original data was altered during the cleaning process.")