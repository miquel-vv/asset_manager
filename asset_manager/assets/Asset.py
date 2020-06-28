from ..mappers.PriceMapper import PriceMapper
from ..connectors import KrakenConnector
import datetime

class Asset:
    def __init__(self, asset_id):
        self.asset_id = asset_id
        self.price_mapper = PriceMapper()
        self.prices=None

    def get_last_price_date(self):
        last_date = self.price_mapper.get_last_saved_date(self.asset_id)
        if self.prices is not None:
            last_date_prices = self.prices.index[-1]
            if last_date_prices >= last_date:
                last_date = last_date_prices
            else:
                self.prices = None

        if last_date is None: 
            return datetime.datetime(2020, 1, 1, 0, 0, tzinfo=datetime.timezone.utc)
        return last_date

    def __eq__(self, other):
        if not isinstance(other, self.__class__):
            return false
        return self.asset_id == other.asset_id

    def __hash__(self):
        return self.asset_id.__hash__()
    