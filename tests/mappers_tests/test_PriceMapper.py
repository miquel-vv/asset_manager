import unittest
import datetime
import os
import pickle
import sqlalchemy as db
import pandas as pd

from asset_manager.mappers.PriceMapper import PriceMapper
from asset_manager.mappers.MapperConnection import MapperConnection

class PriceMapperTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        MapperConnection("testengine")

    def setUp(self):
        self.engine = MapperConnection()
        with self.engine.connect() as con:
            con.execute("DELETE FROM prices WHERE True")
        self.price_mapper=PriceMapper()
    
    def test_save_prices(self):
        complete_df = pd.read_pickle("tests/test_data/etheur.pkl")

        first_five = complete_df[:5]

        self.price_mapper.save_prices("T", first_five, 1) 
        first_five_saved = pd.read_sql_query("SELECT * FROM prices", con=self.engine, index_col=["time"])
        first_five_saved.drop(["asset_id", "span"], axis=1, inplace=True) 

        self.assertTrue(first_five.equals(first_five_saved), 
                        "Dataframe saved through mapper and retreived from database does not equal original from pickle (etheur.pkl).")

        self.price_mapper.save_prices("T", complete_df[5:], 1)

        all_saved = pd.read_sql_query("SELECT * FROM prices", con=self.engine, index_col=["time"])
        all_saved.drop(["asset_id", "span"], axis=1, inplace=True) 

        self.assertTrue(complete_df.equals(all_saved),
                        "Dataframe saved through mapper and retreived from database does not equal original from pickle (etheur.pkl).")
    
    def test_get_prices(self):
        prices = pd.read_pickle("tests/test_data/etheur.pkl")
        subset_prices = prices[4:12]
        length = len(prices.index)
        span_list = [1] * length
        asset_id_list = ["T"] * length
        prices_with_asset = prices.assign(asset_id=asset_id_list, span=span_list)
        prices_with_asset.to_sql("prices", if_exists="append", con=self.engine)

        
        subset_prices_from_mapper = self.price_mapper.get_prices("T", 
                                                                 datetime.datetime(2020, 6, 14, 11, 14, tzinfo=datetime.timezone.utc),
                                                                 datetime.datetime(2020, 6, 14, 11, 21, tzinfo=datetime.timezone.utc))
        prices_from_mapper = self.price_mapper.get_prices("T")

        self.assertTrue(prices.equals(prices_from_mapper), "Prices not loaded correctly.")
        self.assertTrue(subset_prices.equals(subset_prices_from_mapper), "Filtering prices on dates was not as expected.")
    
    def test_last_saved_date(self):
        self.assertEqual(None, self.price_mapper.get_last_saved_date("T"))
        prices = pd.read_pickle("tests/test_data/etheur.pkl")
        asset_id_list = ["T"] * len(prices.index)
        prices_with_asset = prices.assign(asset_id=asset_id_list)
        prices_with_asset.to_sql("prices", if_exists="append", con=self.engine)
        last_date = self.price_mapper.get_last_saved_date("T")
        self.assertEqual(last_date, datetime.datetime(2020,6,14,9,23, tzinfo=datetime.timezone.utc))
    

if __name__=="__main__":
    unittest.main()