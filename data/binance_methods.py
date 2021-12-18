import os
import pandas as pd
from binance.client import Client
from pprint import pprint
from datetime import date, timedelta
from data.indicators import Analyser


class Manager:
    def __init__(self, leverage):
        __api_key = os.environ["BINANCE_API_KEY"]
        __api_secret = os.environ["BINANCE_SECRET_API_KEY"]
        self.main_leverage = leverage
        self.client = Client(__api_key, __api_secret)

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
            print(f"[ERROR] {er}")

    def show_coin_price(self, coin_pare):
        price = " ".join(
            [i['price'] for i in self.client.futures_symbol_ticker() if i['symbol'] == coin_pare])
        return price

    def make_futures_order(self, coin_name, pair, route, value):
        if value == 0:
            raise ValueError("Неправильная сумма!")
        if float(self.show_coin_balance(pair)) < value:
            raise ValueError(f"Недостаточно {pair.upper()} на балансе!")
        try:
            coin_pare = coin_name.upper() + pair.upper()
            coin_info = self.client.futures_symbol_ticker()
            if not coin_info:
                raise ValueError(f"Пары {coin_pare} не существует!")
            self.client.futures_change_leverage(symbol=coin_pare, leverage=self.main_leverage)
            order = self.client.futures_create_order(
                symbol=coin_pare,
                type='MARKET',
                side=route,
                quantity=value,

            )
            order_info = self.client.futures_get_order(symbol=coin_pare,
                                                       orderId=order[
                                                           'orderId'])
            print(
                f"SUCCESSFULLY BOUGHT - {coin_pare} for price - {order_info['avgPrice']} \n"
                f"Marge - {order_info['cumQuote']}$ Leverage - {self.main_leverage}x")
        except Exception as er:
            print(f"[ERROR] {er}")

    def show_coin_volume(self, coin_pare: str, start_date: str, end_date: str, interval: str):
        data = pd.DataFrame(self.client.futures_historical_klines(
            symbol=coin_pare,
            interval=interval,
            start_str=start_date,
            end_str=end_date
        ))
        data = data.iloc[:, :6]
        data.columns = ['date', 'open', 'high', 'low', 'close', 'volume']
        data['date'] = pd.to_datetime(data['date'], unit='ms')
        for col in data.columns[1:]:
            data[col] = pd.to_numeric(data[col])
        candy_types = [int(1 * row['open'] < row['close']) for i, row in data.iterrows()]
        data['candy_type'] = candy_types
        return data


if __name__ == '__main__':
    ex = Manager(10)
    a = Analyser()
