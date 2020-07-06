import pandas as pd
import sqlalchemy as db
from .MapperConnection import MapperConnection

class PriceMapper:
    def __init__(self):
        self.engine=MapperConnection()
        self.base_get_query = "SELECT {fields} FROM prices WHERE asset_id LIKE '{asset_id}' {customs}"

    def save_prices(self, asset_id, prices, interval=None):
        length = len(prices.index)
        asset_id_list = [asset_id] * length
        prices_table = prices.assign(asset_id=asset_id_list)

        if not "span" in prices_table.columns:
            if interval is None:
                raise ValueError("Either an interval or a span columnn must be provided.")
            span_list = [interval] * length
            prices_table = prices.assign(asset_id=asset_id_list, span=span_list)

        if not 'origin' in prices_table.columns:
            origins = ['O'] * length
            prices_table = prices_table.assign(origin=origins)

        with self.engine.connect() as conn:
            prices_table.to_sql("prices", if_exists="append", con=conn)

    def get_prices(self, asset_id, start_date=None, end_date=None):
        
        custom = ""
        if start_date is not None:
            custom = "and time >= '{0}' ".format(start_date.strftime("%Y/%m/%d %H:%M:%S"))
        if end_date is not None:
            custom += "and time <= '{0}' ".format(end_date.strftime("%Y/%m/%d %H:%M:%S"))
        
        custom += "order by time"

        with self.engine.connect() as conn:
            prices = pd.read_sql_query(self.base_get_query.format(fields="*",asset_id=asset_id, customs=custom),
                                       con=conn,
                                       index_col=["time"])

        prices.drop(["asset_id"], axis=1, inplace=True) 
        return prices
    
    def get_last_saved_date(self, asset_id):
        with self.engine.connect() as conn:
            time = pd.read_sql_query(self.base_get_query.format(fields="max(time)", asset_id=asset_id, customs=""),
                                     con=conn)

        try:
            return time["max"][0]
        except IndexError:
            return None
    
    def get_first_saved_date(self, asset_id):
        with self.engine.connect() as conn:
            time = pd.read_sql_query(self.base_get_query.format(fields="min(time)", asset_id=asset_id, customs=""),
                                     con=conn)
            
        try:
            return time["min"][0]
        except IndexError:
            return None