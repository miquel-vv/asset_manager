import argparse
from ..assets.Controller import Controller

def parse_args(argv=None):
    parser = argparse.ArgumentParser(description="Cml tool for asset_manager.")
    parser.add_argument("-u",
                        "--update_prices", 
                        nargs=1, 
                        help="updates the prices of passed asset_id or all if all is passed.")
    parser.add_argument("-o",
                        "--update_orderbooks",
                        nargs=1,
                        help="updates the order books for all the assets.")
    return parser.parse_args()

def update_prices(asset_id):
    controller = Controller()
    if asset_id=="all":
        print("Updating all...")
        controller.update_all_prices()
    else:
        print("Updating {0}...".format(asset_id))
        controller.update_prices(asset_id)
    
    print("Done updating prices.")

def update_order_book(asset_id):
    controller = Controller()
    if asset_id=="all":
        print("Updating all order books...")
        controller.update_all_orders()
    else:
        print("Updating {0}...".format(asset_id))
        controller.update_orders(asset_id)
    print("Done updating orders")

def main():
    args = parse_args()

    if args.update_prices is not None:
        print("Starting up asset_manager...")
        update_prices(args.update_prices[0])
    if args.update_orderbooks is not None:
        print("Initiating order book update...")
        update_order_book(args.update_orderbooks[0])
