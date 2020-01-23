import pandas as pd
import datetime
from .asset_generator import AssetGenerator
from .asset import Asset

class Universe():

    def __init__(self):
        generator = AssetGenerator()
        self.assets = generator.get_all_assets()
        self.start_date, self.end_date, self.timeline = self.create_timeline()

    def get_first_date(self):
        return max(self.assets, key = lambda x: x.get_first_date()).get_first_date()

    def create_timeline(self):
        start_date = self.get_first_date()
        end_date = datetime.datetime(2019,12,6)

        days = (end_date-start_date).days

        timeline = [start_date + datetime.timedelta(i) for i in range(days)]

        return start_date, end_date, timeline

    def execute_strategy(self, strat, start=None, end=None, date_range=None):
        weights, ratio, ret, dev = strat(self.get_assets(date_range=date_range))
        print('Sharpe ratio: ' + str(ratio))
        print('Return: ' + str(ret))
        print('St. Dev: ' + str(dev))
        return weights

    def get_assets(self, start=None, end=None, date_range=None):
        if date_range is None:
            start = self.start_date if start is None else start
            end = self.end_date if end is None else end
            return [asset.copy(pd.date_range(start=start, end=end)) for asset in self.assets if asset.include(start)]
        else:
            return [asset.copy(date_range=date_range) for asset in self.assets if asset.include(date_range[0])]
