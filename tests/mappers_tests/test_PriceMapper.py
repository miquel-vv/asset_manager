import unittest
import datetime
import os
import pickle
import sqlalchemy as db
import pandas as pd

from asset_manager.mappers.PriceMapper import PriceMapper
from asset_manager.mappers.MapperConnection import MapperConnection

def get_enriched_data(data):
        length = len(data.index)
        span_list = [1] * length
        asset_id_list = ["T"] * length
        origins = ["O"] * length
        full_detail = data.assign(asset_id=asset_id_list, span=span_list, origin=origins)
        return full_detail

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
        with self.engine.connect() as conn:
            first_five_saved = pd.read_sql_query("SELECT * FROM prices", con=conn, index_col=["time"])
        first_five_saved.drop(["asset_id", "span", "origin"], axis=1, inplace=True) 
        self.assertTrue(first_five.equals(first_five_saved), 
                        "Dataframe saved through mapper and retreived from database does not equal original from pickle (etheur.pkl).")

        self.price_mapper.save_prices("T", complete_df[5:], 1)
        with self.engine.connect() as conn:
            all_saved = pd.read_sql_query("SELECT * FROM prices", con=conn, index_col=["time"])
        all_saved.drop(["asset_id", "span", 'origin'], axis=1, inplace=True) 
        self.assertTrue(complete_df.equals(all_saved),
                        "Dataframe saved through mapper and retreived from database does not equal original from pickle (etheur.pkl).")
        
        origins = ['A'] * len(complete_df.index)
        artificial_prices = complete_df.assign(origin=origins)
        self.price_mapper.save_prices('A', artificial_prices, 1) 
        with self.engine.connect() as conn:
            check_artificial = pd.read_sql_query("SELECT * FROM prices where asset_id='A'", con=conn, index_col=["time"])
        check_artificial.drop(["asset_id", "span"], axis=1, inplace=True)
        self.assertTrue(artificial_prices.equals(check_artificial), 
                        "Data saved with the artificial origin set, was not saved correctly.")

    
    def test_get_prices(self):
        prices = pd.read_pickle("tests/test_data/etheur.pkl")
        prices_full_detail = get_enriched_data(prices)

        with self.engine.connect() as conn:
            prices_full_detail.to_sql("prices", if_exists="append", con=conn)
        
        subset_prices_from_mapper = self.price_mapper.get_prices("T", 
                                                                 datetime.datetime(2020, 6, 14, 11, 14, tzinfo=datetime.timezone.utc),
                                                                 datetime.datetime(2020, 6, 14, 11, 21, tzinfo=datetime.timezone.utc))
        prices_from_mapper = self.price_mapper.get_prices("T")

        prices = prices_full_detail.drop(["asset_id"], axis=1)
        subset_prices = prices[4:12]
        self.assertTrue(prices.equals(prices_from_mapper), "Prices not loaded correctly.")
        self.assertTrue(subset_prices.equals(subset_prices_from_mapper), "Filtering prices on dates was not as expected.")
    
    def test_last_saved_date(self):
        self.assertEqual(None, self.price_mapper.get_last_saved_date("T"))
        prices = pd.read_pickle("tests/test_data/etheur.pkl")
        prices_full_detail = get_enriched_data(prices) 

        with self.engine.connect() as conn:
            prices_full_detail.to_sql("prices", if_exists="append", con=conn)

        last_date = self.price_mapper.get_last_saved_date("T")
        self.assertEqual(last_date, datetime.datetime(2020,6,14,9,23, tzinfo=datetime.timezone.utc))
    

if __name__=="__main__":
    unittest.main()