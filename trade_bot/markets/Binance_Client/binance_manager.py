import asyncio

import pandas as pd
from binance.client import AsyncClient
from trade_bot.database.db_commands import DbManager
import aiohttp
import calendar
from datetime import datetime


class BinanceManager:
    def __init__(self, tg_user_id):
        self.__db = DbManager()
        self.tg_user_id = tg_user_id
        self.api_url = 'https://api.binance.com/api/v3/klines'
        self.candle_data_limit = 1000

    async def show_coin_price(self, coin_pare):
        auth_data = await self.__db.get_user_keys(self.tg_user_id)
        client = await AsyncClient.create(*auth_data)
        response = await client.futures_mark_price(symbol=coin_pare)
        price = round(float(response['markPrice']), 3)
        await client.close_connection()
        return price

    async def get_historical_data(self, coin_pare, interval, start_date: str, end_date: str) -> pd.DataFrame:
        start = calendar.timegm(datetime.fromisoformat(start_date).timetuple()) * 1000
        end = calendar.timegm(datetime.fromisoformat(end_date).timetuple()) * 1000
        url = f'{self.api_url}?symbol={coin_pare}&interval={interval}&limit={self.candle_data_limit}&startTime={start}&endTime={end}'
        async with aiohttp.ClientSession() as session:
            response = await session.get(url)
            response_data = await response.json()
        data = pd.DataFrame(response_data)
        if data.empty:
            return data
        data = data.drop(range(6, 12), axis=1)
        data.columns = ['date', 'open', 'high', 'low', 'close', 'volume']
        data['date'] = pd.to_datetime(data['date'], unit='ms')
        for col in data.columns[1:]:
            data[col] = pd.to_numeric(data[col])
        return data

    def make_futures_order(self, coin_name, pair, route, value):
        try:
            if not settings.real_work:
                return
            if value > self.show_futures_currency_balance():
                return
            coin_pare = coin_name.upper() + pair.upper()
            order_marge = value * self.main_leverage
            self.client.futures_change_leverage(symbol=coin_pare, leverage=self.main_leverage)
            order = self.client.futures_create_order(
                symbol=coin_pare,
                type='MARKET',
                side=route,
                quantity=order_marge
            )
            order_info = self.client.futures_get_order(symbol=coin_pare, orderId=order['orderId'])
            print(
                f"SUCCESSFULLY BOUGHT - {coin_pare} for price - {order_info['avgPrice']} \n"
                f"Marge - {order_info['cumQuote']}$ Leverage - {self.main_leverage}x")
            return order_info
        except Exception as er:
            settings.log_error.error(er)

    def show_coin_volume(self, coin_pare: str, start_date: str, end_date: str, interval: str) -> pd.DataFrame:
        data = self.get_historical_data(coin_pare, interval, start_date, end_date)
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
            return profit, False
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
        # open_order_data = json.load(open('./swag logs/active orders.json', 'r'))
        if coin_pare not in open_order_data:
            return False
        if not open_order_data[coin_pare]['tp']:
            return fix_profit(coin_pare)
        answer = self.check_coin_pare(open_order_data, coin_pare, coin_price)
        if answer == settings.reached_all_targets_text:
            return answer
        elif not answer:
            return False
        elif not answer[1]:
            return False, coin_pare, answer[0]
        return True, coin_pare, answer[0]

    async def show_futures_currency_balance(self):
        client = await AsyncClient.create(*(await self.__db.get_user_keys(self.user_id)))
        all_balances = await client.futures_account_balance()
        for coin in all_balances:
            if coin['asset'] == self.currency:
                return coin['withdrawAvailable']
        await client.close_connection()
        return None


async def main():
    ex = BinanceManager(595905860)
    # first_date = (datetime.now() - timedelta(hours=5)).timestamp()
    # second_date = datetime.now().timestamp()
    # print(first_date, second_date)
    # res = await ex.get_historical_data('BTCUSDT', '5m', first_date, second_date)
    # print(res)
    # print(res.info())
    # for i in res.columns:
    #     print(i)
    res = await ex.show_coin_price("BTCUSDT")
    print(res)


if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
