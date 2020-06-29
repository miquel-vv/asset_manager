from .MapperConnection import MapperConnection
from asset_manager.assets.Asset import Asset 
import pandas as pd

class AssetMapper:
    def __init__(self, asset_class=Asset):
        self.engine = MapperConnection()
        self.asset_class = asset_class
    
    def get_assets(self):
        asset_type = self.asset_class.__name__.upper()
        assets_df = pd.read_sql_query("select * from assets", con=self.engine)
        asset_list = [self.asset_class(a["asset_id"]) for _,a in assets_df.iterrows() if a["asset_class"]==asset_type] 

        return asset_list