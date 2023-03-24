UserData_query = """INSERT INTO "UsersData" 
(tg_id, license, binance_api_key, binance_secret_api_key, join_date) 
VALUES (%s, %s, %s, %s, %s)
"""
GeneralSettings_query = """INSERT INTO "GeneralSettings" (id, coins, work_condition, currency) VALUES (%s, %s, %s, %s)"""
OrdersSettings_query = """INSERT INTO "OrdersSettings" (id, symbol, leverage, stage_condition, sl_start_percent, 
                            tp_first, tp_number, tp_only_one, sl_stage_percent) 
                            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)"""
GetUserKeys_query = """SELECT binance_api_key, binance_secret_api_key 
                                FROM "UsersData" WHERE tg_id = $1"""
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
