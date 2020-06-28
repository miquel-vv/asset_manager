import unittest
import datetime
import os
import pickle
import sqlalchemy as db
import pandas as pd

from asset_manager.mappers.PriceMapper import PriceMapper

class KrakenConnectorTest(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        engine = db.create_engine("postgresql+psycopg2://asset_manager:" + os.environ["PSQL_PASSWORD"] + "@localhost/asset_management_test_db")
        create_prices_table = db.sql.text("""CREATE TABLE prices(
                                                time TIMESTAMP WITH TIME ZONE, 
                                                asset_id VARCHAR, 
                                                open NUMERIC(12,6), 
                                                high NUMERIC(12,6), 
                                                low NUMERIC(12,6), 
                                                close NUMERIC(12,6),
                                                vwap NUMERIC(12, 6),
                                                volume NUMERIC(16, 8),
                                                trades_count INTEGER,
                                                span INTEGER
                                            );"""
                                          )
        with engine.connect() as con:
            con.execute(create_prices_table)

    @classmethod
    def tearDownClass(cls):
        engine = db.create_engine("postgresql+psycopg2://asset_manager:" + os.environ["PSQL_PASSWORD"] + "@localhost/asset_management_test_db")
        with engine.connect() as con:
            con.execute("DROP TABLE prices;")

    def setUp(self):
        self.engine = db.create_engine('postgresql+psycopg2://asset_manager:' + os.environ['PSQL_PASSWORD'] + '@localhost/asset_management_test_db')
        with self.engine.connect() as con:
            con.execute("DELETE FROM prices WHERE True")
        self.price_mapper=PriceMapper(self.engine)
    
    def test_save_prices(self):
        complete_df = pd.read_pickle("tests/test_data/etheur.pkl")

        first_five = complete_df[:5]

        self.price_mapper.save_prices("ETH", first_five, 1) 
        first_five_saved = pd.read_sql_query("SELECT * FROM prices", con=self.engine, index_col=["time"])
        first_five_saved.drop(["asset_id", "span"], axis=1, inplace=True) 

        self.assertTrue(first_five.equals(first_five_saved), 
                        "Dataframe saved through mapper and retreived from database does not equal original from pickle (etheur.pkl).")

        self.price_mapper.save_prices("ETH", complete_df[5:], 1)

        all_saved = pd.read_sql_query("SELECT * FROM prices", con=self.engine, index_col=["time"])
        all_saved.drop(["asset_id", "span"], axis=1, inplace=True) 

        self.assertTrue(complete_df.equals(all_saved),
                        "Dataframe saved through mapper and retreived from database does not equal original from pickle (etheur.pkl).")
    
    def test_get_prices(self):
        prices = pd.read_pickle("tests/test_data/etheur.pkl")
        length = len(prices.index)
        span_list = [1] * length
        asset_id_list = ["ETH"] * length
        prices_with_asset = prices.assign(asset_id=asset_id_list, span=span_list)
        prices_with_asset.to_sql("prices", if_exists="append", con=self.engine)

        prices_from_mapper = self.price_mapper.get_prices("ETH")

        self.assertTrue(prices.equals(prices_from_mapper))
    
    def test_last_saved_date(self):
        self.assertEqual(None, self.price_mapper.get_last_saved_date("ETH"))
        prices = pd.read_pickle("tests/test_data/etheur.pkl")
        asset_id_list = ["ETH"] * len(prices.index)
        prices_with_asset = prices.assign(asset_id=asset_id_list)
        prices_with_asset.to_sql("prices", if_exists="append", con=self.engine)
        last_date = self.price_mapper.get_last_saved_date("ETH")
        self.assertEqual(last_date, datetime.datetime(2020,6,14,9,23, tzinfo=datetime.timezone.utc))
    

if __name__=="__main__":
    unittest.main()