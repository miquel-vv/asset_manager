import argparse
from ..assets.Controller import Controller

def parse_args(argv=None):
    parser = argparse.ArgumentParser(description="Cml tool for asset_manager.")
    parser.add_argument("-u", 
                        "--update_prices", 
                        nargs=1, 
                        help="updates the prices of passed asset_id or all if all is passed.")
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

def main():
    args = parse_args()

    if args.update_prices is not None:
        print("Starting op asset_manager...")
        update_prices(args.update_prices[0])
