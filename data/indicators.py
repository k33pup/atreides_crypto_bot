from datetime import timedelta, datetime

import pandas as pd
from extra.callbacks import *
from extra import settings


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

    def look_for_patterns(self, data):
        huge_red = []
        huge_green = []
        greenData = data[data['candy_type'] == 1]
        redData = data[data['candy_type'] == 0]
        greenData = greenData[greenData['volume'] >= greenData['volume'].mean() * 2]
        redData = redData[redData['volume'] >= redData['volume'].mean() * 2]
        for i in range(1, len(greenData)):
            huge_green.append((greenData.iloc[i]['date'] -
                               greenData.iloc[i - 1]['date']).seconds)
        for i in range(1, len(redData)):
            huge_red.append((redData.iloc[i]['date'] -
                             redData.iloc[i - 1]['date']).seconds)
        print(huge_green)
        print(huge_red)
        return
