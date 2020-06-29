import unittest
from unittest.mock import patch
import pandas as pd
from asset_manager.mappers.PriceMapper import PriceMapper 
from asset_manager.mappers.AssetMapper import AssetMapper 
from asset_manager.mappers.MapperConnection import MapperConnection
from asset_manager.assets.Crypto import Crypto 
from asset_manager.assets.CryptoRepo import CryptoRepo 

class CryptoRepoTest(unittest.TestCase):

    @classmethod
    def setUpClass(self):
        MapperConnection("testengine")

    def setUp(self):

        prices = pd.read_pickle("tests/test_data/etheur.pkl")

        with patch.object(PriceMapper, "get_prices", return_value=prices):
            self.crypto1 = Crypto("T")
            self.crypto2 = Crypto("T2")

        with patch.object(AssetMapper, "get_assets", return_value=[self.crypto1, self.crypto2]):
            self.repo = CryptoRepo()
    
    def test_get_asset(self):
        all_assets = [self.crypto1, self.crypto2]
        self.assertEqual(self.crypto1, self.repo.get_asset("T"))
        self.assertEqual(self.crypto2, self.repo.get_asset("T2"))
