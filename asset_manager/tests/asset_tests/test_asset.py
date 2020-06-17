import unittest
from unittest.mock import patch
import pandas as pd
import datetime
from asset_manager.assets import Asset
from asset_manager.mappers import PriceMapper

class AssetTest(unittest.TestCase):

    def setUp(self):
        prices = pd.read_pickle('asset_manager/tests/test_data/etheur.pkl')
        with patch.object(PriceMapper, 'get_prices', return_value=prices):
            self.asset = Asset("ETH")

    def test_last_date(self):
        last_date = datetime.datetime(2020,6,14,9,23, tzinfo=datetime.timezone.utc)
        self.assertEquals(last_date, self.asset.get_last_price_date())
