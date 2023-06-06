import os
import logging
from bot.utils.report import setup_logger


coin_list = [
    "1INCH", "ALGO", "AVAX", "AXS", "CHZ", "COMP",
    "CRV", "DASH", "DOGE", "DOT", "EGLD", "ENJ", "EOS", "ETC",
    "FIL", "FTM", "KAVA", "KSM", "LINK", "LTC", "MATIC", "ONE", "SOL",
    "SUSHI", "SXP", "THETA", "TRX", "UNI", "VET", "WAVES", "XLM", "XMR",
    "XRP", "XTZ", "SFP", "DENT", "IOTX", "OCEAN", "C98", "ZIL", "HOT", "DODO", "TRB",
    "AUDIO", "BAND", "OGN", "BAKE"
]
real_work = False
algo_ratio = 5
tp_quantity = 10
MY_CHANNEL = -1001732576576
TOKEN = os.environ['BOT_TOKEN']
log_error = setup_logger('ERROR', f"swag logs/errors.log", logging.ERROR)
log_binance = setup_logger('BINANCE', f'swag logs/binance.log')
log_telegram = setup_logger('TELEGRAM', f'swag logs/tg.log')
currency = 'USDT'
algo_interval = '15m'
help_interval = {
    '15m': 900,
    '5m': 300,
    '1h': 3600,
}
help_direction = {
    0: "SELL",
    1: "BUY",
}

reached_all_targets_text = 'ALL TARGETS DONE!'
schedule = [14, 29, 44, 59]
sl_procent = 15
sl_start_procent = 40
activate_key = "12345"
order_volume = 5
