import time
from datetime import date, timedelta

import requests
import settings
from bot.utils import Manager
from bot.trade.stategy import Analyser


def send_signal(coin, signal, coin_price):
    ids = DbManager().get_all_chats_id('simple')
    text = f"✨ OH, NEW HUGE SIGNAL! \nCOIN is {coin}, DIRECTION is {signal}. \nOPEN PRICE is {coin_price}"
    print(f"Coin - {coin}, route - {signal}, price - {coin_price}")
    for chat_id in ids:
        requests.post(
            url=f'https://api.telegram.org/bot{settings.TOKEN}/sendMessage',
            data={'chat_id': chat_id, 'text': text}
        ).json()


def send_reached_target(is_open, coin_pare, profit):
    ids = DbManager().get_all_chats_id('simple')
    if not is_open:
        text = f"CLOSED BY STOP-LOSS on {coin_pare}. PROFIT {round(profit, 2)}%"
    else:
        text = f"ALREADY REACHED {round(profit, 2)}% on {coin_pare}"
    print(text.lower())
    settings.log_binance.info(text)
    for chat_id in ids:
        requests.post(
            url=f'https://api.telegram.org/bot{settings.TOKEN}/sendMessage',
            data={'chat_id': chat_id, 'text': text}
        ).json()


def look_for_signal(BinanceManager, DataAnalyser):
    with open('bot/logs/active orders.json', 'r') as myfile:
        data = json.loads(myfile.read())
    used_coins = []
    print(f"Looking for signal... at {datetime.now()}")
    for coin in settings.coin_list:
        coin_pare = coin + settings.currency
        first_date = str(date.today() - timedelta(days=1))
        second_date = str(date.today() + timedelta(days=1))
        temp_data = BinanceManager.show_coin_volume(coin_pare, first_date, second_date, settings.algo_interval)
        signal_answer = DataAnalyser.solve_for_last_candies(temp_data)
        if signal_answer:
            if coin_pare not in data.keys():
                coin_price = BinanceManager.show_coin_price(coin_pare)
                BinanceManager.make_futures_order(coin, settings.currency, signal_answer.upper(), 5)
                settings.log_binance.info(f"Coin - {coin}, route - {signal_answer}, price - {coin_price}")
                send_signal(coin_pare, signal_answer, coin_price)
                direction = 1 if signal_answer == "BUY" else -1
                tp_prices = [coin_price * (1 + 0.15 / BinanceManager.main_leverage * i * direction) for i in
                             range(1, settings.tp_quantity + 1)]
                sl_price = coin_price - coin_price * (
                        settings.sl_start_procent / 100 / BinanceManager.main_leverage) * direction
                add_signal(coin_pare, signal_answer, coin_price,
                           str(datetime.now()), tp_prices,
                           sl_price, BinanceManager.main_leverage)
                used_coins.append(coin)
        time.sleep(0.1)
    print(f"Waiting for another {settings.algo_interval} interval...")


def check_exist_signals(BinanceManager):
    data = json.load(open('bot/logs/active orders.json', 'r'))
    for coin in data:
        if answer := BinanceManager.check_coin_for_profit(coin):
            if answer is not False:
                is_opened, coin_pare, profit = answer
                send_reached_target(is_opened, coin_pare, profit)
        time.sleep(0.1)


def binance_main():
    try:
        BinanceManager = Manager(25)
        DataAnalyser = Analyser()
        previous = None
        print(f"STARTED! TIME - {datetime.now()}")
        while True:
            check_exist_signals(BinanceManager)
            current_minute = datetime.now().minute
            if current_minute in settings.schedule and previous != current_minute:
                previous = current_minute
                look_for_signal(BinanceManager, DataAnalyser)
    except Exception as er:
        settings.log_error.error(er)


def test():
    s = time.time()
    BinanceManager = Manager(25)
    DataAnalyser = Analyser()
    while True:
        for coin in settings.coin_list:
            temp_data = BinanceManager.get_historical_data(coin + settings.currency, '5m',
                                                           str(datetime.now() - timedelta(hours=6)), str(datetime.now()))
            answer = DataAnalyser.get_last_ema_cross(temp_data)
            if answer:
                print(f'{coin} - {answer[-1][-1]} {answer[-1][0]}')
            time.sleep(1)
        time.sleep(1)


if __name__ == '__main__':
    # p1 = Process(target=binance_main)
    # p1.start()
    # p2 = Process(target=tele_main)
    # p2.start()
    # p1.join()
    # p2.join()
    test()
