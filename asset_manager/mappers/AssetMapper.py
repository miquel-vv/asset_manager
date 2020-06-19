from .MapperConnection import MapperConnection
from asset_manager.assets.Asset import Asset 
import pandas as pd

class AssetMapper:
    def __init__(self, engine=None, asset_class=Asset):
        self.engine = MapperConnection().get_engine() if engine is None else engine
        self.asset_class = asset_class
    
    def get_assets(self):
        asset_type = self.asset_class.__name__.upper()
        assets_df = pd.read_sql_query("select * from assets", con=self.engine)
        asset_list = [self.asset_class(a["asset_id"]) for _,a in assets_df.iterrows() if a["asset_type"]==asset_type] 

        return asset_list