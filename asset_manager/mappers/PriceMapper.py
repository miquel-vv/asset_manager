import pandas as pd
import sqlalchemy as db
from .MapperConnection import MapperConnection

class PriceMapper:
    def __init__(self, engine=None):
        self.engine=MapperConnection().get_engine() if engine is None else engine

    def save_prices(self, asset_id, prices):
        asset_id_list = [asset_id] * len(prices.index)
        prices_table = prices.assign(asset_id=asset_id_list)
        prices_table.to_sql("prices", if_exists="append", con=self.engine)

