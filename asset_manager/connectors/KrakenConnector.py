from datetime import datetime
import requests
import pandas as pd

class KrakenConnector:
    def __init__(self):
        self.url = "https://api.kraken.com/0/public/{lookup}"

    def get_prices(self, start_date, asset_pair, interval=1):
        start_date = datetime.timestamp(start_date)
        params = {"since": start_date, "pair": asset_pair, "interval": interval}
        prices_url = self.url.format(lookup = "OHLC") 
        data = self.send_get_request(prices_url, params)["result"]

        i=0
        for key, value in data.items():
            if key != "last":
                i+=1
                data = value

        if i!=1:
            raise ValueError("Data incorrectly parsed.")

        if start_date == data[0][0]:
            return "UP-TO-DATE"
        return self.transform_to_dataframe(data)

    def send_get_request(self, url, params):
        response = requests.get(url, params)
        if response.status_code != 200:
            raise ConnectionError("""Status code: {0} received by sending url to
                                  {1} with parameters {2}.""".format(response.status_code, url, params))
        
        return response.json()
        
    def transform_to_dataframe(self, data):
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

        