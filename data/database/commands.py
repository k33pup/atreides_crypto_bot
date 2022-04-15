import psycopg2
from psycopg2 import Error
import os
from data.database.templates import *
from datetime import datetime
from data import report


class DbManager:
    def __init__(self):
        self.host = "localhost"
        self.port = 5432
        self.user = "postgres"
        self.password = os.getenv("dbPass")
        self.db_name = "trade bot"

    def add_user(self, tg_user_id, api_key, secret_api__key, licence_type):
        try:
            connection = psycopg2.connect(
                host=self.host,
                port=self.port,
                user=self.user,
                password=self.password,
                database=self.db_name,
            )
            cursor = connection.cursor()
            current_time = datetime.utcnow().strftime('%d-%m-%Y %H:%M:%S')
            cursor.execute(UserData_query, (tg_user_id, licence_type, api_key, secret_api__key, current_time))
            connection.commit()
            user_table_id = self.get_user_db_id(tg_user_id)
            cursor.execute(GeneralSettings_query, (user_table_id, start_coins, start_condition, start_currency))
            connection.commit()
            for coin in start_coins:
                cursor.execute(OrdersSettings_query, (user_table_id, coin, start_leverage, False,
                                                      start_sl, start_tp, start_tp_number,
                                                      start_tp_only_one, start_sl_stage_percent))
            connection.commit()
            print(f"SUCCESSFULLY ADDED USER {tg_user_id} TO DATABASE")
            connection.close()
            cursor.close()
        except (Exception, Error) as er:
            print("FAILED TO ADD USER")
            print(er)

    def get_user_db_id(self, tg_user_id):
        try:
            connection = psycopg2.connect(
                host=self.host,
                port=self.port,
                user=self.user,
                password=self.password,
                database=self.db_name,
            )

            cursor = connection.cursor()
            cursor.execute(f"""SELECT id FROM "UsersData" WHERE tg_id = %s""", (tg_user_id,))
            result = cursor.fetchone()
            connection.close()
            cursor.close()
            return result

        except (Exception, Error) as er:
            print("FAILED TO SEARCH USER ID")
            print(er)

    def get_user_keys(self, user_id):
        try:
            connection = psycopg2.connect(
                host=self.host,
                port=self.port,
                user=self.user,
                password=self.password,
                database=self.db_name,
            )

            cursor = connection.cursor()
            cursor.execute(f"""SELECT binance_api_key, binance_secret_api_key 
                                FROM "UsersData" WHERE id = %s""", (user_id,))
            result = cursor.fetchone()
            connection.close()
            cursor.close()
            return result
        except (Exception, Error) as er:
            print("FAILED TO SEARCH USER BINANCE API KEYS")
            print(er)

    def get_user_currency(self, user_id):
        try:
            connection = psycopg2.connect(
                host=self.host,
                port=self.port,
                user=self.user,
                password=self.password,
                database=self.db_name,
            )

            cursor = connection.cursor()
            cursor.execute(f"""SELECT currency FROM "GeneralSettings" WHERE id = %s""", (user_id,))
            result = cursor.fetchone()
            connection.close()
            cursor.close()
            return result
        except (Exception, Error) as er:
            print("FAILED TO FIND USER BINANCE FUTURES CURRENCY BALANCE")
            print(er)


if __name__ == '__main__':
    db = DbManager()
