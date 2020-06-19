from .MapperConnection import MapperConnection
import asset_manager.assets as assets
import pandas as pd

class AssetMapper:
    def __init__(self, engine=None, asset_class=assets.Asset):
        self.engine = MapperConnection().get_engine() if engine is None else engine
        self.asset_class = asset_class
    
    def get_assets(self):
        assets_df = pd.read_sql_query("select * from assets", con=self.engine)
        asset_list = [self.asset_class(a["asset_id"]) for _,a in assets_df.iterrows()] 

        return asset_list