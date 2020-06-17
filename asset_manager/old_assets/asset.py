'''
To Do:
    -Add store self function that pickles itself.
    -Add update price method that looks for its latest price.
    -(if ever) Add get news tone to look for the news sentiment around a certain asset.
'''


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
        self_dict = {
            'id': self.db_id,
            'name': self.name,
            'asset_class': self.asset_class,
            'description': self.description,
            'prices': self.prices
        }
        return self_dict

    def copy(self, date_range=None):
        ''' Creates a copy of itself, based on the dates provided. i.e. a version of itself over only
            one year, or with prices calculated monthly.
            args:
                start: first moment
                end: last moment
                frequency: the interval between two prices, see pandas Offset aliases for options.
            returns:
                A copy of itself.
        '''
    
        kwargs = self.create_dict()
        if date_range is None:
            kwargs['returns'] = self.returns
        else:
            kwargs['prices'] = self.prices.reindex(date_range)

        return Asset(**kwargs)