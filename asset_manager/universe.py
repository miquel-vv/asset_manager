import pandas as pd
import datetime
from .asset_generator import AssetGenerator
from .asset import Asset

class Universe():

    def __init__(self):
        generator = AssetGenerator()
        self.assets = generator.get_all_assets()
        self.start_date, self.end_date, self.timeline = self.create_timeline()

    def asset_to_df(self, start_date=None, end_date=None):
        '''Creates a dataframe from the returns of the assets.
        args:
            start_date: the date on which the df should start.
            end_date: the date on which the df should end.
        returns:
            a df based on the returns of the assets in the universe.'''
        
        start_date = self.start_date if not start_date else start_date
        end_date = self.end_date if not end_date else end_date
        asset_dict = {asset.name: asset.returns[start_date:end_date] for asset in self.assets}
        return pd.DataFrame(asset_dict, index=pd.date_range(start_date, end_date))

    def get_covariance(self, start_date=None, end_date=None):
        asset_df = self.asset_to_df(start_date, end_date)
        return asset_df.cov()

    def get_correlation(self, start_date=None, end_date=None):
        asset_df = self.asset_to_df(start_date, end_date)
        return asset_df.corr()

    def get_first_date(self):
        return max(self.assets, key = lambda x: x.get_first_date()).get_first_date()

    def create_timeline(self):
        start_date = self.get_first_date()
        end_date = datetime.datetime(2019,12,6)

        days = (end_date-start_date).days

        timeline = [start_date + datetime.timedelta(i) for i in range(days)]

        return start_date, end_date, timeline



if __name__ == '__main__':
    print(Universe().get_first_date())