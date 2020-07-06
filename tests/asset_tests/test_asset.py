import unittest
from unittest.mock import patch
import pandas as pd
import datetime
from asset_manager.assets.Asset import Asset
from asset_manager.mappers.MapperConnection import MapperConnection
from asset_manager.mappers.PriceMapper import PriceMapper

def mocked_mapper(*args, **kwargs):
    class MockMapper():
        def __init__(self):
            pass

        def get_last_saved_date(self):
            return datetime.datetime(2020,6,14,9,23, tzinfo=datetime.timezone.utc)

        def get_first_saved_date(self):
            return datetime.datetime(2020,6,14,9,10, tzinfo=datetime.timezone.utc)
        
    return MockMapper()


class AssetTest(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        MapperConnection("testengine")

    def setUp(self):
        self.asset = Asset("T")
    
    def test_last_date(self):
        last_date = datetime.datetime(2020,6,14,9,23, tzinfo=datetime.timezone.utc)

        with patch.object(PriceMapper, "get_last_saved_date", return_value=datetime.datetime(2020,6,14,9,23, tzinfo=datetime.timezone.utc)):
            date_from_asset = self.asset.get_last_price_date()
        self.assertEqual(last_date, date_from_asset)

        no_asset=Asset("DOESNT EXIST") 
        self.assertEqual(datetime.datetime(2020,1,1,0,0, tzinfo=datetime.timezone.utc), no_asset.get_last_price_date())
    
    def test_equality(self):
        new_asset = Asset("T")
        self.assertEqual(new_asset, self.asset)

    def test_hash(self):
        first_set = {self.asset}
        second_set = {self.asset}

        new_asset = Asset("T")

        second_set.add(new_asset)

        self.assertEqual(first_set, second_set)
    
    def test_get_first_date(self):
        with patch.object(PriceMapper, "get_first_saved_date", return_value=datetime.datetime(2020,6,14,9,10, tzinfo=datetime.timezone.utc)):
            date_from_asset = self.asset.get_first_price_date()

        self.assertEqual(datetime.datetime(2020,6,14,9,10, tzinfo=datetime.timezone.utc), date_from_asset) 

    @patch.object(PriceMapper, "get_last_saved_date", return_value=datetime.datetime(2020,6,14,9,23, tzinfo=datetime.timezone.utc))
    @patch.object(PriceMapper, "get_first_saved_date", return_value=datetime.datetime(2020,6,14,9,10, tzinfo=datetime.timezone.utc))
    def test_in_range(self, mocked_last_date, mocked_first_date):
        before_start = datetime.datetime(2020, 6, 13, 9, 0, tzinfo=datetime.timezone.utc)
        in_range1 = datetime.datetime(2020, 6, 14, 9, 13, tzinfo=datetime.timezone.utc)
        in_range2 = datetime.datetime(2020, 6, 14, 9, 20, tzinfo=datetime.timezone.utc)
        after_end = datetime.datetime(2020, 6, 15, 9, 0, tzinfo=datetime.timezone.utc)

        self.assertFalse(self.asset.in_range(before_start, in_range2))
        self.assertFalse(self.asset.in_range(in_range2, after_end))
        self.assertTrue(self.asset.in_range(in_range1, in_range2))
        