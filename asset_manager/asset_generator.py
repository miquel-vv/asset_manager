import sqlalchemy as db
import pandas as pd
from .asset import Asset

class AssetGenerator():
    def __init__(self):
        engine = db.create_engine('postgres+psycopg2://asset_manager:pwd@localhost/asset_managment')
        self.assets = pd.read_sql_query(
            'select * from assets', 
            con=engine
        )
        self.prices = pd.read_sql_query(
            'select * from price', 
            con=engine, 
            index_col=['asset_id', 'date']
        )

    def get_all_assets(self):
        '''Retrurns a list with all assets.'''

        assets = []
        for _, asset in self.assets.iterrows():
            kwargs = asset.to_dict()
            kwargs['prices'] = self.get_prices_of_asset(kwargs['id'])
            assets.append(Asset(**kwargs))
        
        return assets

    def get_prices_of_asset(self, asset_id):
        '''Looks in the prices table for the price of a specific asset.
        args:
            asset_id: The id of an asset in the original asset list.
        returns:
            A pandas series containing the prices and the dates as timestamp.
        '''
        return self.prices.loc[asset_id]['end_of_day']
