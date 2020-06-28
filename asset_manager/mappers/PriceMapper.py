import pandas as pd
import sqlalchemy as db
from .MapperConnection import MapperConnection

class PriceMapper:
    def __init__(self, engine=None):
        self.engine=MapperConnection().get_engine() if engine is None else engine
        self.base_get_query = "SELECT {fields} FROM prices WHERE asset_id LIKE '{asset_id}' {customs}"

    def save_prices(self, asset_id, prices, interval):
        length = len(prices.index)
        asset_id_list = [asset_id] * length
        span_list = [interval] * length
        prices_table = prices.assign(asset_id=asset_id_list, span=span_list)
        prices_table.to_sql("prices", if_exists="append", con=self.engine)

    def get_prices(self, asset_id):
        prices = pd.read_sql_query(self.base_get_query.format(fields="*",asset_id=asset_id, customs="order by time"),
                                   con=self.engine,
                                   index_col=["time"])
        prices.drop(["asset_id", "span"], axis=1, inplace=True) 
        return prices
    
    def get_last_saved_date(self, asset_id):
        time = pd.read_sql_query(self.base_get_query.format(fields="max(time)", asset_id=asset_id, customs=""),
                                 con=self.engine)

        try:
            return time["max"][0]
        except IndexError:
            return None