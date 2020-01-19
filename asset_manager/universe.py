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

    def execute_strategy(self, strat, start=None, end=None):
        start = self.start_date if start is None else start
        end = self.end_date if end is None else end

        return strat([asset.copy(start, end) for asset in self.assets if asset.include(start)])