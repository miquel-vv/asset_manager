import datetime
import numpy as np
import pandas as pd
from .PriceGap import PriceGap

class PriceCleaner:
    def __init__(self, prices, interval_between_prices):
        self.prices_to_clean = prices
        self.interval_between_prices = interval_between_prices
        self.gaps_content = None 
    
    def get_cleaned_prices(self):
        end_of_gaps, gap_intervals = self.look_for_gaps()
        needs_cleaning = not end_of_gaps.empty 
        
        if not needs_cleaning:
            return self.prices_to_clean

        self.fill_gaps(end_of_gaps, gap_intervals)
        clean_prices = self.merge_gaps_with_prices()
        return clean_prices
    
    def look_for_gaps(self):
        real_intervals = self.prices_to_clean.index.to_series().diff().dropna() #First can't be end so drop it
        expected_interval = self.interval_between_prices
        end_of_gap_detected = real_intervals != expected_interval
        gap_intervals = real_intervals.loc[end_of_gap_detected] 
        end_of_gaps = self.prices_to_clean[1:].loc[end_of_gap_detected] #Ignore first

        return end_of_gaps, gap_intervals
    
    def fill_gaps(self, end_of_gaps, gap_intervals):
        end_of_gaps.apply(lambda x: self.get_gap_content(x, gap_intervals.loc[x.name]), axis=1)

    def merge_gaps_with_prices(self):
        clean_prices = self.prices_to_clean.append(self.gaps_content)
        return clean_prices.sort_index()
    
    def get_gap_content(self, end_of_gap, size_of_gap):
        start_time = end_of_gap.name - size_of_gap
        start_of_gap = self.prices_to_clean.loc[start_time]
        gap = PriceGap(start_of_gap, end_of_gap)
        if self.gaps_content is None:
            self.gaps_content = gap.get_content_to_fill_gap(self.interval_between_prices)
        else:
            self.gaps_content = self.gaps_content.append(gap.get_content_to_fill_gap(self.interval_between_prices))