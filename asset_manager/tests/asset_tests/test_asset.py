import unittest
from unittest.mock import patch
import pandas as pd
import datetime
from asset_manager.assets.Asset import Asset 
from asset_manager.mappers.PriceMapper import PriceMapper

class AssetTest(unittest.TestCase):

    def setUp(self):
        self.prices = pd.read_pickle('asset_manager/tests/test_data/etheur.pkl')
        with patch.object(PriceMapper, 'get_prices', return_value=self.prices):
            self.asset = Asset("ETH")

    def test_last_date(self):
        last_date = datetime.datetime(2020,6,14,9,23, tzinfo=datetime.timezone.utc)
        self.assertEqual(last_date, self.asset.get_last_price_date())

        self.asset.prices = self.prices.iloc[0:0]
        self.assertEqual(datetime.datetime(2020,1,1,0,0, tzinfo=datetime.timezone.utc), self.asset.get_last_price_date())
    
    def test_equality(self):
        with patch.object(PriceMapper, 'get_prices', return_value=self.prices):
            new_asset = Asset("ETH")
        self.assertEqual(new_asset, self.asset)

    def test_hash(self):
        first_set = {self.asset}
        second_set = {self.asset}

        with patch.object(PriceMapper, 'get_prices', return_value=self.prices):
            new_asset = Asset("ETH")

        second_set.add(new_asset)

        self.assertEqual(first_set, second_set)
