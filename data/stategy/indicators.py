from extra.callbacks import *
import settings
import pandas
import matplotlib.pyplot as plt


class Analyser:
    def __init__(self):
        self.route_help = {1: "BUY", 0: "SELL"}
        self.ratio = settings.algo_ratio

    def solve_for_last_candies(self, data):
        last_volume = data.iloc[-1]['volume']
        mean_volume = data.iloc[-10:-1]["volume"].mean()
        if mean_volume == 0:
            raise BadHistoryData("Недопустимые исторические данные!")
        concern = last_volume / mean_volume
        if concern >= self.ratio:
            signal_type = self.route_help[data.iloc[-1]['candy_type']]
            return signal_type
        return False

    def look_for_patterns(self, data, period):
        interval = 240
        best_procent = 0
        best_start = 0
        general_chain = data.iloc[-interval:]
        for i in range(len(data) - interval):
            temp_proc = 0
            wrong_candles = 0
            for j in range(interval):
                first, second = general_chain.iloc[j], data.iloc[i + j]
                if (first['open'] < first['close'] and second['open'] < second['close']) or \
                        (first['open'] > first['close'] and second['open'] > second['close']):
                    if first['open'] < first['close']:
                        candles = sorted((first['close'] - first['open'], second['close'] - second['open']))
                        shadows = sorted((first['high'] - first['low'], second['high'] - second['low']))
                    else:
                        candles = sorted((first['open'] - first['close'], second['open'] - second['close']))
                        shadows = sorted((first['high'] - first['low'], second['high'] - second['low']))
                    block_proc = (candles[0] / candles[1] + shadows[0] / shadows[1]) / 2
                    temp_proc += block_proc
                else:
                    wrong_candles += 1
            temp_proc -= (wrong_candles / 100)
            temp_proc /= interval
            if temp_proc > best_procent:
                best_procent = temp_proc
                best_start = i
            print(temp_proc)
        return best_start, best_procent, interval

    def get_ema_lines(self, candles_data, number, base_type='open') -> pandas.DataFrame:
        clear_data = candles_data[base_type]
        ema = clear_data.ewm(com=number).mean()
        return ema

    def get_last_ema_cross(self, candles_data):
        ema_1 = self.get_ema_lines(candles_data, 50)
        ema_2 = self.get_ema_lines(candles_data, 200)
        corridor = 25
        last_cross = -corridor
        result = []
        for i in range(corridor // 2, len(ema_1) - corridor // 2):
            first_element, second_element = ema_1.iloc[i], ema_2.iloc[i]
            first_start, second_start = ema_1.iloc[i - corridor // 2], ema_2.iloc[i - corridor // 2]
            first_end, second_end = ema_1.iloc[i + corridor // 2], ema_2.iloc[i + corridor // 2]
            if max(first_element, second_element) / min(first_element, second_element) - 1 <= 0.0025:
                if max(first_start, second_start) / min(first_start, second_start) - 1 >= 0.004 or \
                        max(first_end, second_end) / min(first_end, second_end) - 1 >= 0.004:
                    if i - last_cross >= corridor:
                        route = 'BUY' if first_start < second_start and first_end > second_end else "SELL"
                        result.append((candles_data.iloc[i]['date'], route))
                        last_cross = i
        return result
