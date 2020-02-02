from .asset_picker import OptimalAllocation
import pandas as pd

'''
To Do:
    -Create the yeary allocation strategy.
'''

class SharpeStrategy():

    def __init__(self, uni, start, end, min_return, reallocate='Y', sharpe_period='M', min_weight=0.1):
        self.uni = uni
        self.asset_picker = OptimalAllocation(min_return)
        self.sharpe_period = sharpe_period
        self.min_weight = min_weight
        self.period_allocation = {}
        if start.month == 1 and start.day == 1:
            start - pd.Timedelta(days=1)                 #The pd date_range will take the next 31-dec as date. So set it earlier to not loose a year. 
        self.period = pd.date_range(start, end, freq=reallocate)

    def execute(self):
        for i, date in enumerate(self.period):
            start = date + pd.Timedelta(days=1)
            end = self.period[i+1]

            year_range = pd.date_range(start=start, end=end, freq=self.sharpe_period)
            self.period_allocation[start.year] = self.get_allocation(year_range)

        return self.period_allocation


    def get_allocation(self, year_range):
        assets = self.uni.get_assets(date_range=year_range)
        allocation,_,_,_ = self.asset_picker(assets)
        allocation = allocation[allocation >= self.min_weight]
        return allocation


