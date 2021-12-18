import pandas as pd
from extra.callbacks import *
from extra import settings


class Analyser:
    def __init__(self):
        self.route_help = {1: "buy", 0: "sell"}
        self.ratio = settings.algo_ratio

    def solve(self, data):
        last_volume = data.iloc[-1]['volume']
        mean_volume = data.iloc[-10:-1]["volume"].mean()
        if mean_volume == 0:
            raise BadHistoryData("Недопустимые исторические данные!")
        concern = last_volume / mean_volume
        if concern >= self.ratio:
            signal_type = self.route_help[data.iloc[-1]['candy_type']]
            return signal_type
        return False
