AddUser_query = """INSERT INTO "users" (tg_id, license, join_date) VALUES (%s, %s, %s)"""
UsedDbId_query = """SELECT id FROM "UsersData" WHERE tg_id = %s"""
GeneralSettings_query = """INSERT INTO "GeneralSettings" (id, coins, work_condition, currency) VALUES (%s, %s, %s, %s)"""
start_coins = ["1INCH", "ALGO", "AVAX", "AXS", "CHZ", "COMP",
               "CRV", "DASH", "DOGE", "DOT", "EGLD", "ENJ", "EOS", "ETC",
               "FIL", "FTM", "KAVA", "KSM", "LINK", "LTC", "MATIC", "ONE", "SOL",
               "SUSHI", "SXP", "THETA", "TRX", "UNI", "VET", "WAVES", "XLM", "XMR",
               "XRP", "XTZ", "SFP", "DENT", "IOTX", "OCEAN", "C98", "ZIL", "HOT", "DODO", "TRB",
               "AUDIO", "BAND", "OGN", "BAKE"]
