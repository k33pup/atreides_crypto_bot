from argparse import ArgumentParser

parser = ArgumentParser()
parser.add_argument("--clear", choices=['orders', 'binance', 'tele'], type=str, nargs="+")
parser.add_argument('--add_user')
args = parser.parse_args()
if args.clear:
    places = list(args.clear)
    if 'orders' in places:
        with open('trade_bot/logs/active orders.json', "w") as file:
            file.write("{}")
    if 'binance' in places:
        with open('trade_bot/logs/binance.log', "w") as file:
            file.write("")
    if 'tele' in places:
        with open('trade_bot/logs/teleg.log', "w") as file:
            file.write("")
