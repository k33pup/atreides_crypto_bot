import os
import textwrap
import time
from math import ceil
import pandas as pd
from binance.client import Client
from pprint import pprint
from datetime import date, timedelta
from data.indicators import Analyser
import json
import csv
import logging
from extra import settings
from data.report import *

logging.basicConfig(filename="swag logs/example.log", level=logging.INFO)
log_error = logging.getLogger("RUNBOT")
log_signal = logging.getLogger("SIGNAL")


class Manager:
    def __init__(self, leverage):
        __api_key = os.environ["BINANCE_API_KEY"]
        __api_secret = os.environ["BINANCE_SECRET_API_KEY"]
        self.main_leverage = leverage
        self.client = Client(__api_key, __api_secret)
        self.take_profit = 10

    def show_coin_balance(self, coin_name):
        try:
            coin_name = coin_name.upper()
            result = 0.0
            balances_normal = [i for i in self.client.get_account()['balances'] if float(i["free"]) > 0]
            for el in balances_normal:
                if el['asset'] == coin_name:
                    result = el['free']
                    break
            return result
        except Exception as er:
            log_error.exception(er)

    def show_coin_price(self, coin_pare):
        price = " ".join(
            [i['price'] for i in self.client.futures_symbol_ticker() if i['symbol'] == coin_pare])
        return round(float(price), 3)

    def make_futures_order(self, coin_name, pair, route, value):
        if value == 0:
            raise ValueError("Неправильная сумма!")
        try:
            if not settings.real_work:
                return
            coin_pare = coin_name.upper() + pair.upper()
            coin_info = self.client.futures_symbol_ticker()
            coin_price = self.show_coin_price(coin_pare)
            if not coin_info:
                raise ValueError(f"Пары {coin_pare} не существует!")
            self.client.futures_change_leverage(symbol=coin_pare, leverage=self.main_leverage)
            order = self.client.futures_create_order(
                symbol=coin_pare,
                type='MARKET',
                side=route,
                quantity=coin_price if 10 <= coin_price <= 100 else value * self.main_leverage
            )
            order_info = self.client.futures_get_order(symbol=coin_pare,
                                                       orderId=order[
                                                           'orderId'])
            print(
                f"SUCCESSFULLY BOUGHT - {coin_pare} for price - {order_info['avgPrice']} \n"
                f"Marge - {order_info['cumQuote']}$ Leverage - {self.main_leverage}x")
            return order_info
        except Exception as er:
            log_error.exception(er)

    def show_coin_volume(self, coin_pare: str, start_date: str, end_date: str, interval: str):
        data = pd.DataFrame(self.client.futures_historical_klines(
            symbol=coin_pare,
            interval=interval,
            start_str=start_date,
            end_str=end_date,

        ))
        data = data.iloc[:, :6]
        data.columns = ['date', 'open', 'high', 'low', 'close', 'volume']
        data['date'] = pd.to_datetime(data['date'], unit='ms')
        for col in data.columns[1:]:
            data[col] = pd.to_numeric(data[col])
        candy_types = [int(row['open'] < row['close']) for i, row in data.iterrows()]
        data['candy_type'] = candy_types
        return data

    def show_open_order_data(self, coin_pare):
        res = [i for i in self.client.futures_account()['positions'] if i['symbol'] == coin_pare]
        for el in res:
            if el['entryPrice'] == '0.0':
                return False
            return el
        return False

    def get_proc(self, orders_data, coin_pare, coin_price):
        if orders_data[coin_pare]['route'] == "BUY":
            return (coin_price / orders_data[coin_pare]['open_price'] - 1) * 100 * orders_data[coin_pare]['lev']
        return (orders_data[coin_pare]['open_price'] / coin_price - 1) * 100 * orders_data[coin_pare]['lev']

    def check_coin_pare(self, orders_data, coin_pare, coin_price):
        temp_sl = None
        if not len(orders_data[coin_pare]['tp']):
            return settings.reached_all_targets_text
        if (coin_price <= orders_data[coin_pare]['sl'] and orders_data[coin_pare]['route'] == "BUY") or \
                (coin_price >= orders_data[coin_pare]['sl'] and orders_data[coin_pare]['route'] == "SELL"):
            profit = self.get_proc(orders_data, coin_pare, coin_price)
            add_to_history(orders_data, coin_pare, coin_price, profit)
            return profit
        elif coin_price >= orders_data[coin_pare]['tp'][0] and orders_data[coin_pare]['route'] == 'BUY':
            temp_sl = coin_price - (coin_price * settings.sl_procent / 100 / orders_data[coin_pare]['lev'])
        elif coin_price <= orders_data[coin_pare]['tp'][0] and orders_data[coin_pare]['route'] == 'SELL':
            temp_sl = coin_price + (coin_price * settings.sl_procent / 100 / orders_data[coin_pare]['lev'])
        if temp_sl:
            set_sl(coin_pare, temp_sl)
            return fix_target(coin_pare), temp_sl
        return False

    def check_coin_for_profit(self, coin_pare):
        coin_price = self.show_coin_price(coin_pare)
        open_order_data = json.load(open('./swag logs/active orders.json', 'r'))
        if coin_pare not in open_order_data:
            return False
        if not open_order_data[coin_pare]['tp']:
            return fix_profit(coin_pare)
        answer = self.check_coin_pare(open_order_data, coin_pare, coin_price)
        if answer == settings.reached_all_targets_text:
            return answer
        elif type(answer) == float:
            return False, coin_pare, answer
        elif answer:
            return True, coin_pare, answer[0]
        return False

    def cancel_order_for_profit(self, pare, price, route):
        try:
            if not (answer := self.show_open_order_data(pare)):
                return False
            print(f"REALISED PROFIT - {answer['unrealizedProfit']}")
            close_price = round(price, 3)
            print(route)
            self.client.futures_create_order(symbol=pare, side=settings.help_direction[route], type='STOP_MARKET',
                                             stopPrice=close_price, closePosition='true')
            print(f"CLOSED POSITION {answer['symbol']}")
            with open('swag logs/active orders.json', 'r') as data_file:
                data = json.load(data_file)
            data.pop(pare)
            with open('swag logs/active orders.json', 'w') as data_file:
                json.dump(data, data_file)
            print(answer)
            with open("signals.csv", "w", newline='', encoding='utf-8') as csv_file:
                data = csv.DictWriter(csv_file, fieldnames=['coin_pare', 'open_price', 'volume', 'profit'])
                data.writerow(
                    {"coin_pare": pare, 'open_price': answer['entryPrice'],
                     'volume': answer['initialMargin'], 'profit': answer['unrealizedProfit']})
        except Exception as er:
            print(er)


if __name__ == '__main__':
    print(json.load(open('./swag logs/active orders.json')))
