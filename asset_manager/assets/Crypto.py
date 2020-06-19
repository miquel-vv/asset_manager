from .Asset import Asset
from ..connectors import KrakenConnector

class Crypto(Asset):

    def __init__(self, asset_id):
        super().__init__(asset_id)
        self.kraken_connector = KrakenConnector()
        self.asset_pair = "X{0:X>3}ZEUR".format(asset_id)

    def load_prices(self, interval):
        last_date = self.get_last_price_date()
        new_prices = self.kraken_connector.get_prices(last_date, self.asset_pair, interval)
        if new_prices=="UP-TO-DATE":
            return
        self.price_mapper.save_prices(self.asset_id, new_prices)
        self.prices.append(new_prices)
