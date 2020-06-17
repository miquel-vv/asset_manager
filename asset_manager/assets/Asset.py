from ..mappers import PriceMapper
from ..connectors import KrakenConnector

class Asset:
    def __init__(self, asset_id):
        self.asset_id = asset_id
        self.price_mapper = PriceMapper()
        self.prices = self.price_mapper.get_prices(asset_id)
        self.last_saved_price = self.get_last_price_date()

    def get_last_price_date(self):
        return self.prices.index[-1]
    