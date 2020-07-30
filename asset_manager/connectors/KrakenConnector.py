import datetime
import requests
import pandas as pd
from asset_manager.assets.Order import Bid, Ask
from asset_manager.assets.OrderBook import OrderBook

class KrakenConnector:
    def __init__(self):
        self.url = "https://api.kraken.com/0/public/{lookup}"

    def get_prices(self, start_date, asset_pair, interval=1):
        start_date = datetime.datetime.timestamp(start_date)
        params = {"since": start_date, "pair": asset_pair, "interval": interval}
        prices_url = self.url.format(lookup = "OHLC") 
        data = self.send_get_request(prices_url, params)["result"]

        data = self.get_first_data_content(data)

        if start_date == data[0][0]:
            return "UP-TO-DATE"
        return self.transform_price_to_dataframe(data)

    def get_order_book(self, asset_pair):
        current_timestamp = datetime.datetime.utcnow()
        current_timestamp = current_timestamp.replace(tzinfo=datetime.timezone.utc)
                
        params = {"pair": asset_pair} 
        order_book_url=self.url.format(lookup="Depth")
        data = self.send_get_request(order_book_url, params)["result"]

        data = self.get_first_data_content(data)
        bids = self.create_bids(data["bids"])
        asks = self.create_asks(data["asks"])

        return OrderBook(current_timestamp, bids, asks)
        
    def create_bids(self, bids):
        return [Bid(b[0], b[1], b[2]) for b in bids]

    def create_asks(self, asks):
        return [Ask(a[0], a[1], a[2]) for a in asks]

    def get_first_data_content(self, data):
        """Kraken changes the assetpair name and uses it as a key, 
        since we don't know it we need to loop to find the data
        and hope it is the first value."""

        i=0
        for key, value in data.items():
            if key != "last":
                i+=1
                single_data = value

        if i!=1:
            raise ValueError("Data incorrectly parsed.")

        return single_data


    def send_get_request(self, url, params):
        response = requests.get(url, params)
        if response.status_code != 200:
            raise ConnectionError("""Status code: {0} received by sending url to
                                  {1} with parameters {2}.""".format(response.status_code, url, params))
        
        return response.json()
        
    def transform_price_to_dataframe(self, data):
        df = pd.DataFrame(data) 
        df.columns = ["time", "open", "high", "low", "close", "vwap", "volume", "trades_count"] 
        df.index = pd.to_datetime(df["time"], utc=True, unit='s')
        df.drop("time", axis=1, inplace=True)
        df = df.astype({
            "open": "float64",
            "high": "float64",
            "low": "float64",
            "close": "float64",
            "vwap": "float64",
            "volume": "float64",
            "trades_count": "int64"
        })
        
        return df

        
