import unittest
from unittest.mock import patch
import pandas as pd
from asset_manager.mappers.PriceMapper import PriceMapper 
from asset_manager.mappers.AssetMapper import AssetMapper 
from asset_manager.assets.Crypto import Crypto 
from asset_manager.assets.CryptoRepo import CryptoRepo 

class CryptoRepoTest(unittest.TestCase):

    def setUp(self):

        prices = pd.read_pickle("asset_manager/tests/test_data/etheur.pkl")

        with patch.object(PriceMapper, "get_prices", return_value=prices):
            self.crypto1 = Crypto("ETH")
            self.crypto2 = Crypto("BTC")

        with patch.object(AssetMapper, "get_assets", return_value=[self.crypto1, self.crypto2]):
            self.repo = CryptoRepo()
    
    def test_get_asset(self):
        all_assets = [self.crypto1, self.crypto2]
        self.assertEqual(self.crypto1, self.repo.get_asset("ETH"))
        self.assertEqual(self.crypto2, self.repo.get_asset("BTC"))
