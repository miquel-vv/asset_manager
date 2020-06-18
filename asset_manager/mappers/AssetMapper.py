from .MapperConnection import MapperConnection
import asset_manager.assets as assets
import pandas as pd

class AssetMapper:
    def __init__(self, engine=None):
        self.engine = MapperConnetion().get_engine() if engine is None else engine
    
    def get_assets(self):
        assets_df = pd.read_sql_query("select * from assets", con=self.engine)
        asset_list = [assets.Asset(a["asset_id"]) for _,a in assets_df.iterrows()]

        return asset_list