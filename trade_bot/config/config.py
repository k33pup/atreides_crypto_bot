import os
from dotenv import load_dotenv, find_dotenv

load_dotenv(find_dotenv())

BOT_TOKEN = os.getenv('BOT_TOKEN')
PG_PASSWORD = os.getenv('dbPass')
DATABASE_NAME = os.getenv('db_name')
IP = os.getenv('ip')
PORT = os.getenv('port')

PG_URL = f'postgresql+asyncpg://postgres:{PG_PASSWORD}@{IP}/{DATABASE_NAME}'

start_coins = ["1INCH", "ALGO", "AVAX", "AXS", "CHZ", "COMP",
               "CRV", "DASH", "DOGE", "DOT", "EGLD", "ENJ", "EOS", "ETC",
               "FIL", "FTM", "KAVA", "KSM", "LINK", "LTC", "MATIC", "ONE", "SOL",
               "SUSHI", "SXP", "THETA", "TRX", "UNI", "VET", "WAVES", "XLM", "XMR",
               "XRP", "XTZ", "SFP", "DENT", "IOTX", "OCEAN", "C98", "ZIL", "HOT", "DODO", "TRB",
               "AUDIO", "BAND", "OGN", "BAKE"]
start_condition = False
start_currency = "USDT"
start_leverage = 20
start_sl = 30
start_tp = 15
start_tp_number = 10
start_tp_only_one = 15
start_sl_stage_percent = 10
