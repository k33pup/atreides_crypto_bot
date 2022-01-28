import json
from extra import settings
import csv
from datetime import datetime


def add_signal(coin_pare, route, open_price, time, tp, sl, lev):
    data = json.load(open('./swag logs/active orders.json', 'r'))
    data[coin_pare] = {'route': route, 'open_price': open_price, 'lev': lev,
                       'time': time, "tp": tp, "sl": sl}
    with open('./swag logs/active orders.json', 'w') as json_file:
        json.dump(data, json_file)


def fix_profit(coin_pare):
    data = json.load(open('./swag logs/active orders.json', 'r'))
    if not len(data[coin_pare]):
        return settings.reached_all_targets_text
    if data[coin_pare]['route'] == 'BUY':
        profit = (data[coin_pare]['sl'] / data[coin_pare]['open_price'] - 1) * 100
    else:
        profit = (data[coin_pare]['open_price'] / data[coin_pare]['sl'] - 1) * 100
    profit *= data[coin_pare]['lev']
    data.pop(coin_pare)
    with open('./swag logs/active orders.json', 'w') as json_file:
        json.dump(data, json_file)
    return profit


def fix_target(coin_pare):
    data = json.load(open('./swag logs/active orders.json', 'r'))
    if not len(data[coin_pare]):
        return settings.reached_all_targets_text
    if data[coin_pare]['route'] == 'BUY':
        profit = (data[coin_pare]['tp'][0] / data[coin_pare]['open_price'] - 1) * 100 * data[coin_pare]['lev']
    else:
        profit = (data[coin_pare]['open_price'] / data[coin_pare]['tp'][0] - 1) * 100 * data[coin_pare]['lev']
    data[coin_pare]['tp'].pop(0)
    with open('./swag logs/active orders.json', 'w') as json_file:
        json.dump(data, json_file)
    return profit


def set_sl(coin_pare, sl_price):
    data = json.load(open('./swag logs/active orders.json', 'r'))
    if not len(data[coin_pare]):
        return settings.reached_all_targets_text
    data[coin_pare]['sl'] = sl_price
    with open('./swag logs/active orders.json', 'w') as json_file:
        json.dump(data, json_file)


def add_to_history(orders_data, coin_pare, coin_price, profit):
    post = [str(datetime.now()), coin_pare, orders_data[coin_pare]['open_price'], coin_price, profit]
    with open("./swag logs/signals.csv", "a", newline='', encoding='utf-8') as csv_file:
        write_data = csv.writer(csv_file, delimiter=';')
        write_data.writerow(post)


if __name__ == '__main__':
    pass
