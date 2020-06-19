from asset_manager.mappers.AssetMapper import AssetMapper
from .Crypto import Crypto

class CryptoRepo:
    def __init__(self):
        self.mapper = AssetMapper(asset_class=Crypto)
        self.cryptos = self.mapper.get_assets()
    
    def get_asset(self, asset_id):
        for crypto in self.cryptos:
            if crypto.asset_id == asset_id:
                return crypto
    
    def get_assets(self):
        return self.cryptos
        