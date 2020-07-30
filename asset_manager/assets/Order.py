import datetime
from abc import ABC

class Order(ABC):
    def __init__(self, price, volume, timestamp):
        self.price = price
        self.volume = volume
        self.datetime_placed = self.transform_to_utc_datetime(timestamp)

    def transform_to_utc_datetime(self, timestamp):
        date = datetime.datetime.fromtimestamp(timestamp)
        date = date.replace(tzinfo=datetime.timezone.utc)
        return date

    def get_order_type(self):
        return self.__class__.__name__.lower()

class Bid(Order):
    pass

class Ask(Order):
    pass
