from .Asset import Asset
from ..connectors import KrakenConnector
import pandas as pd

class Crypto(Asset):

    def __init__(self, asset_id):
        super().__init__(asset_id)
        self.kraken_connector = KrakenConnector()
        self.asset_pair = "{0:X>3}EUR".format(asset_id)
        self.span = 1

    def update_order_book(self):
        self.order_book = self.kraken_connector.get_order_book(self.asset_pair)

    def save_orders(self):
        self.order_book.save(self.asset_id)

    def update_prices(self, interval):
        last_date = self.get_last_price_date()
        new_prices = self.kraken_connector.get_prices(last_date, self.asset_pair, interval)
        if not isinstance(new_prices, pd.DataFrame) and new_prices=="UP-TO-DATE":
            return
        self.price_mapper.save_prices(self.asset_id, new_prices, interval)
        if self.prices is None:
            self.prices = new_prices
        else:
            self.prices = self.prices.append(new_prices, verify_integrity=True)
