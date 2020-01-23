import pandas as pd
import numpy as np
from .asset import Asset
from scipy.optimize import minimize, LinearConstraint, Bounds

def sharpe_ratio(weights, means, cov, optimizer=True):
    weights = np.matrix(weights)
    ret = np.asscalar(means * weights.transpose())
    step_before_var = weights * cov
    var = step_before_var * weights.transpose()
    dev = np.asscalar(np.sqrt(var))

    ratio = ret/dev

    if optimizer:
        return -ratio # negative because scipy minimizes this function, however bigger is better.
    else:
        return ratio, ret, dev

class OptimalAllocation:
    
    def __init__(self):
        self.assets = None
        self.asset_df = None

    def __call__(self, assets):
        self.assets = assets
        self.assets_to_df()
        return self.allocate()

    def assets_to_df(self):
        '''Creates a dataframe from the returns of the assets.
        returns:
            a df based on the returns of the assets in the universe.'''
        
        asset_dict = {asset.name: asset.returns for asset in self.assets}
        self.asset_df = pd.DataFrame(asset_dict)

    def allocate(self):
        means = self.asset_df.mean()
        stock_index = means.index
        
        initial_weights = [1/len(means)] * len(means) #equal weights initially
        lower_bound = [0] * len(means)
        upper_bound = [1] * len(means)

        means = np.matrix(means)
        cov = np.matrix(self.asset_df.cov()) 
        bounds = Bounds(lower_bound, upper_bound)

        optimal_solution = minimize(
            sharpe_ratio, 
            initial_weights,
            args=(means, cov),
            method='SLSQP',
            constraints=({'type': 'eq', 'fun': lambda x: 1 - sum(x)}),
            bounds=bounds
        )

        if not optimal_solution.success:
            raise Exception('Optimization failed: {}.'.format(optimal_solution.message))

        optimal_weights = pd.Series(optimal_solution.x, index=stock_index)
        optimal_sharpe, ret, dev = sharpe_ratio(optimal_solution.x, means, cov, optimizer=False)

        return optimal_weights, optimal_sharpe, ret, dev



