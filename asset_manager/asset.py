class Asset:
    def __init__(self, id, name, asset_class, description, prices):
        self.db_id = id
        self.name = name
        self.asset_class = asset_class
        self.description = description
        self.prices = prices.sort_index()
        self.returns = self.prices.pct_change()

    def get_first_date(self):
        return self.returns.index[1] #Return the second item as the first will be zero.