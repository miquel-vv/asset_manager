from .errors import OutOfRangeError
from .PriceCleaner import PriceCleaner
from ..mappers.PriceMapper import PriceMapper
from ..connectors import KrakenConnector
import pandas as pd
import datetime

class Asset:
    def __init__(self, asset_id):
        self.asset_id = asset_id
        self.price_mapper = PriceMapper()
        self.prices=None
        self.span=None

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
    
    def get_first_price_date(self):
        first_date = self.price_mapper.get_first_saved_date(self.asset_id) 
        
        if first_date is None:
            OutOfRangeError("No prices have been saved yet for asset: {0}".format(self.asset_id))
        
        return first_date

    def in_range(self, start_date=None, end_date=None):
        first_date = self.get_first_price_date()
        last_date = self.get_last_price_date()
        
        start_date=first_date if start_date is None else start_date
        end_date=last_date if end_date is None else end_date

        if start_date<first_date or start_date>last_date:
            return False
        
        if end_date<first_date or end_date>last_date:
            return False
        
        return True

    def load_prices(self, start_date, end_date):
        self.prices = self.price_mapper.get_prices(self.asset_id)

    def __eq__(self, other):
        if not isinstance(other, self.__class__):
            return False
        return self.asset_id == other.asset_id

    def __hash__(self):
        return self.asset_id.__hash__()
    
    def clean_prices(self):
        if self.span is None:
            raise AttributeError("Span must be set before cleaning the prices.")

        self.prices.sort_index(inplace=True)
        price_cleaner = PriceCleaner(self.prices, datetime.timedelta(minutes=self.span))
        self.prices = price_cleaner.get_cleaned_prices()
