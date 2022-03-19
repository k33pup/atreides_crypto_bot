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
        self.password = os.getenv('dbPass')
        self.db_name = "trade bot"

    def add_user(self, user_id, chat_id, licence):
        try:
            connection = psycopg2.connect(
                host=self.host,
                port=self.port,
                user=self.user,
                password=self.password,
                database=self.db_name,
            )
            cursor = connection.cursor()
            current_time = str(datetime.utcnow())
            cursor.execute(UserData_query, (user_id, chat_id, licence, current_time, current_time))
            connection.commit()
            user_table_id = self.get_user_db_id(user_id)
            cursor.execute(GeneralSettings_query, (user_table_id, start_coins, start_condition, start_currency))
            connection.commit()
            for coin in start_coins:
                cursor.execute(OrdersSettings_query, (user_table_id, coin, start_leverage, False,
                                                      start_sl, start_tp, start_tp_number,
                                                      start_tp_only_one, start_sl_stage_percent))
            connection.commit()
            print(f"SUCCESSFULLY ADDED USER {user_id} TO DATABASE")
        except (Exception, Error) as er:
            print("FAILED TO ADD USER")
            print(er)
        finally:
            if connection:
                connection.close()
                cursor.close()

    def get_user_db_id(self, user_id):
        try:
            connection = psycopg2.connect(
                host=self.host,
                port=self.port,
                user=self.user,
                password=self.password,
                database=self.db_name,
            )

            cursor = connection.cursor()
            cursor.execute(f"""SELECT id FROM "UsersData" WHERE tg_id = %s""", (user_id,))
            result = cursor.fetchone()
            return result

        except (Exception, Error) as er:
            print("FAILED TO SEARCH USER ID")
        finally:
            if connection:
                connection.close()
                cursor.close()


if __name__ == '__main__':
    db = DbManager()
