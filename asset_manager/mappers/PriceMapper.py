import pandas as pd
import sqlalchemy as db
from .MapperConnection import MapperConnection

class PriceMapper:
    def __init__(self, engine=None):
        self.engine=MapperConnection().get_engine() if engine is None else engine

    def save_prices(self, asset_id, prices, interval):
        length = len(prices.index)
        asset_id_list = [asset_id] * length
        span_list = [interval] * length
        prices_table = prices.assign(asset_id=asset_id_list, span=span_list)
        prices_table.to_sql("prices", if_exists="append", con=self.engine)

    def get_prices(self, asset_id):
        prices = pd.read_sql_query("SELECT * FROM prices WHERE asset_id LIKE '{0}' order by time".format(asset_id), con=self.engine, index_col=["time"])
        prices.drop(["asset_id", "span"], axis=1, inplace=True) 
        return prices