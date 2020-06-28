import unittest
from unittest.mock import patch
import pandas as pd
import datetime
from asset_manager.assets.Asset import Asset 
from asset_manager.mappers.PriceMapper import PriceMapper

class AssetTest(unittest.TestCase):

    def setUp(self):
        self.asset = Asset("ETH")
        
    def test_last_date(self):
        last_date = datetime.datetime(2020,6,14,9,23, tzinfo=datetime.timezone.utc)
        with patch.object(PriceMapper, "get_last_saved_date", return_value=datetime.datetime(2020,6,14,9,23, tzinfo=datetime.timezone.utc)):
            date_from_asset = self.asset.get_last_price_date()
        self.assertEqual(last_date, date_from_asset)

        no_asset=Asset("DOESNT EXIST") 
        self.assertEqual(datetime.datetime(2020,1,1,0,0, tzinfo=datetime.timezone.utc), no_asset.get_last_price_date())
    
    def test_equality(self):
        new_asset = Asset("ETH")
        self.assertEqual(new_asset, self.asset)

    def test_hash(self):
        first_set = {self.asset}
        second_set = {self.asset}

        new_asset = Asset("ETH")

        second_set.add(new_asset)

        self.assertEqual(first_set, second_set)
