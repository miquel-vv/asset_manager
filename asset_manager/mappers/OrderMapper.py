from .MapperConnection import MapperConnection
import pandas as pd
import datetime

class OrderMapper:
    def __init__(self):
        self.engine=MapperConnection()
        self.base_get_query = "SELECT {fields} FROM orders WHERE asset_id LIKE '{asset_id}' {customs}" 
    
    def save_orders(self, orders_dataframe):
        with self.engine.connect() as conn:
            orders_dataframe.to_sql("orders", if_exists="append", con=conn)

    def last_saved_date(self, asset_id):
        with self.engine.connect() as conn:
            time = pd.read_sql_query(self.base_get_query.format(
                fields="max(order_time) max",
                asset_id=asset_id,
                customs=""
            ), con=conn)            

        try:
            last_saved_date = time["max"][0]
        except:
            last_saved_date = datetime.datetime(1900, 1, 1, 0, 0, 
                                                tzinfo=datetime.timezone.utc) 

        last_saved_date = last_saved_date if last_saved_date is not None else datetime.datetime(1900,1,1,0,0,
                                                                                                tzinfo=datetime.timezone.utc)
        return last_saved_date
