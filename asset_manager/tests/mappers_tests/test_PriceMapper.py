import unittest
import os
import pickle
import sqlalchemy as db
import pandas as pd

from asset_manager.mappers import PriceMapper

class KrakenConnectorTest(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        engine = db.create_engine('postgres+psycopg2://asset_manager:' + os.environ['PSQL_PASSWORD'] + '@localhost/asset_management_test_db')
        create_prices_table = db.sql.text("""CREATE TABLE prices(
                                                time TIMESTAMP WITH TIME ZONE, 
                                                asset_id VARCHAR, 
                                                open NUMERIC(12,6), 
                                                high NUMERIC(12,6), 
                                                low NUMERIC(12,6), 
                                                close NUMERIC(12,6),
                                                vwap NUMERIC(12, 6),
                                                volume NUMERIC(16, 8),
                                                trades_count INTEGER
                                            );"""
                                          )
        with engine.connect() as con:
            con.execute(create_prices_table)

    @classmethod
    def tearDownClass(cls):
        engine = db.create_engine('postgres+psycopg2://asset_manager:' + os.environ['PSQL_PASSWORD'] + '@localhost/asset_management_test_db')
        with engine.connect() as con:
            con.execute("DROP TABLE prices;")

    def setUp(self):
        self.engine = db.create_engine('postgres+psycopg2://asset_manager:' + os.environ['PSQL_PASSWORD'] + '@localhost/asset_management_test_db')
        clear_prices = db.sql.text("DELETE FROM prices WHERE True")
        with self.engine.connect() as con:
            con.execute("DELETE FROM prices WHERE True")
    
    def test_save_prices(self):
        price_mapper = PriceMapper()
        complete_df = pd.read_pickle("asset_manager/tests/test_data/etheur.pkl")

        first_five = complete_df[:5]

        price_mapper.save_prices("ETH", first_five)

        first_five_saved = pd.read_sql_query("SELECT * FROM prices", con=self.engine, index_col=["time"])
        first_five_saved.drop("asset_id", axis=1, inplace=True) 

        self.assertTrue(first_five.equals(first_five_saved), 
                        "Dataframe saved through mapper and retreived from database does not equal original from pickle (etheur.pkl).")

        price_mapper.save_prices("ETH", complete_df[5:])

        all_saved = pd.read_sql_query("SELECT * FROM prices", con=self.engine, index_col=["time"])
        all_saved.drop("asset_id", axis=1, inplace=True) 

        self.assertTrue(complete_df.equals(all_saved),
                        "Dataframe saved through mapper and retreived from database does not equal original from pickle (etheur.pkl).")
if __name__=="__main__":
    unittest.main()