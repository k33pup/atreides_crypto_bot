import time
from extra import settings
from data.binance_methods import Manager
from data.indicators import Analyser
from datetime import date, timedelta, datetime
import logging

logging.basicConfig(filename="example.log", level=logging.INFO)
log_error = logging.getLogger("RUNBOT")
log_signal = logging.getLogger("SIGNAL")


def main():
    BinanceManager = Manager(1)
    DataAnalyser = Analyser()
    used_coins = []
    while True:
        print("Looking for signal...")
        for coin in settings.coin_list:
            coin_pare = coin + settings.currency
            first_date = str(date.today() - timedelta(days=1))
            second_date = str(date.today() + timedelta(days=1))
            temp_data = BinanceManager.show_coin_volume(coin_pare, first_date, second_date, settings.interval)
            answer = DataAnalyser.solve(temp_data)
            if answer:
                if coin not in used_coins:
                    log_signal.info(f"COIN - {coin}, DO - {answer}. TIME - {datetime.now()}")
                    print(
                        f"!!SIGNAL!!  COIN - {coin}, DO - {answer}. TIME - {datetime.now()}. "
                        f"PRICE - {BinanceManager.show_coin_price(coin_pare)}")
                    used_coins.append(coin)
            time.sleep(0.01)
        print(f"Waiting for another {settings.interval} interval...")
        time.sleep(settings.help_interval[settings.interval])


if __name__ == '__main__':
    try:
        main()
    except Exception as er:
        log_error.exception(er)
