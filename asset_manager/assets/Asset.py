from ..mappers.PriceMapper import PriceMapper
from ..connectors import KrakenConnector
import datetime

class Asset:
    def __init__(self, asset_id):
        self.asset_id = asset_id
        self.price_mapper = PriceMapper()
        self.prices = self.price_mapper.get_prices(asset_id)
        self.last_saved_price = self.get_last_price_date()

    def get_last_price_date(self):
        if len(self.prices.index)==0:
            return datetime.datetime(2020, 1, 1, 0, 0, tzinfo=datetime.timezone.utc)
        return self.prices.index[-1]

    def __eq__(self, other):
        if not isinstance(other, self.__class__):
            return false
        return self.asset_id == other.asset_id

    def __hash__(self):
        return self.asset_id.__hash__()
    