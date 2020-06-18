import unittest
import os
from unittest.mock import patch
import sqlalchemy as db
import pandas as pd
from asset_manager.mappers import AssetMapper, PriceMapper
from asset_manager.assets import Asset

class AssetMapperTest(unittest.TestCase):

    def setUp(self):
        self.engine = db.create_engine("postgresql+psycopg2://asset_manager:" + os.environ["PSQL_PASSWORD"] + "@localhost/asset_management_test_db")
        with self.engine.connect() as con:
            con.execute("insert into assets(asset_id) values ('ETH')")
    
    def tearDown(self):
        self.engine = db.create_engine("postgresql+psycopg2://asset_manager:" + os.environ["PSQL_PASSWORD"] + "@localhost/asset_management_test_db")
        with self.engine.connect() as con:
            con.execute("delete from assets where true")

    def test_get_assets(self):
        prices = pd.read_pickle('asset_manager/tests/test_data/etheur.pkl')
        with patch.object(PriceMapper, 'get_prices', return_value=prices):
            test_assets = [Asset("ETH")]
            loaded_assets = AssetMapper(self.engine).get_assets()

        self.assertEqual(test_assets, loaded_assets)