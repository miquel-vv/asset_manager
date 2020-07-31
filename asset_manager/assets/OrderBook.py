import datetime
import pandas as pd
from ..mappers.OrderMapper import OrderMapper

class OrderBook:
    def __init__(self, timestamp, bids, asks):
        self.datetime_open = timestamp
        self.bids = bids
        self.asks = asks
        self.order_mapper = OrderMapper()

    def save(self, asset_id):
        start_time = self.get_last_saved_order_date(asset_id)
        new_orders = self.to_dataframe(asset_id, start_time)
        self.order_mapper.save_orders(new_orders)

    def get_last_saved_order_date(self, asset_id):
        return self.order_mapper.last_saved_date(asset_id)

    def to_dataframe(self, asset_id, start_time):

        bid_times = [b.datetime_placed for b in self.bids if b.datetime_placed > start_time]
        bid_prices = [b.price for b in self.bids if b.datetime_placed > start_time]
        bid_volumes = [b.volume for b in self.bids if b.datetime_placed > start_time]
        bid_types = ["bid"]*len(bid_times)

        ask_times = [a.datetime_placed for a in self.asks if a.datetime_placed > start_time]
        ask_prices = [a.price for a in self.asks if a.datetime_placed > start_time]
        ask_volumes = [a.volume for a in self.asks if a.datetime_placed > start_time]
        ask_types = ["ask"]*len(ask_times)

        total_length = (len(bid_times) + len(ask_times))

        order_dataframe = pd.DataFrame({
            "asset_id": [asset_id] * total_length,
            "order_book_time": [self.datetime_open] * total_length, 
            "order_time": bid_times + ask_times,
            "price": bid_prices + ask_prices,
            "volume": bid_volumes + ask_volumes,
            "type": bid_types + ask_types
        })
        order_dataframe = order_dataframe.set_index(["asset_id", "order_time"])

        return order_dataframe
