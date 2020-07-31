from .CryptoRepo import CryptoRepo

class Controller:
    def __init__(self):
       self.crypto_repo = CryptoRepo() 
    
    def update_prices(self, asset_name):
       crypto = self.crypto_repo.get_asset(asset_name)  
       crypto.update_prices(1)
    
    def update_all_prices(self):
        cryptos = self.crypto_repo.get_assets()
        for crypto in cryptos:
            crypto.update_prices(1)

    def update_orders(self, asset_id):
        crypto = self.crypto_repo.get_asset(asset_id)
        crypto.update_order_book()
        crypto.save_orders()
    
    def update_all_orders(self):
        cryptos = self.crypto_repo.get_assets()
        for crypto in cryptos:
            crypto.update_order_book()
            crypto.save_orders()
