class Asset:
    def __init__(self, id, name, asset_class, description, prices, returns=None):
        '''Returns is optional to save computation time while running. However when saving to persistent storage,
        returns should not be saved, this makes sure that prices and returns are kept aligned.'''

        self.db_id = id
        self.name = name
        self.asset_class = asset_class
        self.description = description
        self.prices = prices.sort_index()
        if returns is None:
            self.returns = self.prices.pct_change()
        else:
            self.returns = returns

    def get_first_date(self):
        return self.returns.index[1] #Return the second item as the first will be zero.

    def include(self, start):
        '''This method checks wether the asset should be included given a certain start date.
        args:
            start: start date/timestamp
        returns:
            boolean. if true then include.'''

        asset_start = self.get_first_date()
        asset_end = self.returns.index[-1]

        if start < asset_start or start > asset_end:
            return False
        else:
            return True

    def create_dict(self):
        dict = {
            'id': self.db_id,
            'name': self.name,
            'asset_class': self.asset_class,
            'description': self.description,
            'prices': self.prices
        }
        return dict

    def copy(self, start, end):
        '''creates a copy of itself, limited in time.'''

        kwargs = self.create_dict()
        kwargs['prices'] = self.prices[start:end]
        kwargs['returns'] = self.returns[start:end]

        return Asset(**kwargs)
