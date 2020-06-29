import unittest
import os
from unittest.mock import patch
import sqlalchemy as db
import pandas as pd
from asset_manager.mappers.AssetMapper import AssetMapper
from asset_manager.mappers.PriceMapper import PriceMapper
from asset_manager.mappers.MapperConnection import MapperConnection
from asset_manager.assets.Asset import Asset
from asset_manager.assets.Crypto import Crypto

class AssetMapperTest(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        MapperConnection("testengine")

    def setUp(self):
        self.engine = MapperConnection()
        with self.engine.connect() as con:
            con.execute("insert into assets(asset_id, asset_class) values ('AST', 'ASSET')")
            con.execute("insert into assets(asset_id, asset_class) values ('T', 'CRYPTO')")
    
    def tearDown(self):
        self.engine = MapperConnection()
        with self.engine.connect() as con:
            con.execute("delete from assets where true")

    def test_get_assets(self):
        prices = pd.read_pickle("tests/test_data/etheur.pkl")
        with patch.object(PriceMapper, 'get_prices', return_value=prices):
            test_assets = [Asset("AST")]
            test_cryptos = [Crypto("T")]
            loaded_assets = AssetMapper().get_assets()
            loaded_cryptos = AssetMapper(asset_class=Crypto).get_assets()

        self.assertEqual(test_assets, loaded_assets)
        self.assertEqual(test_cryptos, loaded_cryptos)
