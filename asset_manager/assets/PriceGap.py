import pandas as pd

class PriceGap:
    def __init__(self, start_of_gap, end_of_gap):
        self.start_of_gap = start_of_gap
        self.end_of_gap = end_of_gap
        self.gap_size = end_of_gap.name - start_of_gap.name
    
    def get_content_to_fill_gap(self, price_interval):
        start_time = self.start_of_gap.name + price_interval 
        end_time = self.end_of_gap.name - price_interval

        intervals_to_cover = int((self.gap_size).total_seconds()/price_interval.total_seconds())
        price_increment_per_minute = (self.end_of_gap["close"] - self.start_of_gap["close"])/intervals_to_cover

        prices = [self.start_of_gap["close"] + (price_increment_per_minute * i) for i in range(1, intervals_to_cover)]
        timestamps = [self.start_of_gap.name + (price_interval * i) for i in range(1, intervals_to_cover)]
        zeros = [0] * (intervals_to_cover - 1)
        origins = ["A"] * (intervals_to_cover - 1)
        spans = [int(price_interval.total_seconds()/60)] * (intervals_to_cover - 1) 

        content = pd.DataFrame({
            "time": timestamps,
            "open": prices,
            "high": prices,
            "low": prices,
            "close": prices,
            "vwap": zeros,
            "volume": zeros,
            "trades_count": zeros, 
            "origin": origins,
            "span": spans 
        })
        content.index = content.time

        return content.drop(["time"], axis=1) 
