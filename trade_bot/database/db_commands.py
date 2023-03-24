import asyncpg
from psycopg2 import Error
import os
from datetime import datetime


class DbManager:
    def __init__(self):
        self.host = "localhost"
        self.port = 5432
        self.user = "postgres"
        self.password = os.getenv("dbPass")
        self.db_name = "trade bot"

    async def add_user(self, tg_user_id, api_key, secret_api__key, licence_type):
        try:
            async with asyncpg.connect(
                    host=self.host,
                    port=self.port,
                    user=self.user,
                    password=self.password,
                    database=self.db_name,
            ) as connection:
                async with connection.cursor() as cursor:
                    current_time = datetime.utcnow().strftime('%d-%m-%Y %H:%M:%S')
                    await cursor.execute(UserData_query,
                                         (tg_user_id, licence_type, api_key, secret_api__key, current_time))
                    await connection.commit()
                    user_table_id = self.get_user_db_id(tg_user_id)
                    await cursor.execute(GeneralSettings_query,
                                         (user_table_id, start_coins, start_condition, start_currency))
                    await connection.commit()
                    for coin in start_coins:
                        await cursor.execute(OrdersSettings_query, (user_table_id, coin, start_leverage, False,
                                                                    start_sl, start_tp, start_tp_number,
                                                                    start_tp_only_one, start_sl_stage_percent))
                    await connection.commit()
                    print(f"SUCCESSFULLY ADDED USER {tg_user_id} TO DATABASE")
        except (Exception, Error) as er:
            print("FAILED TO ADD USER")
            print(er)

    async def get_user_db_id(self, tg_user_id):
        try:
            async with asyncpg.connect(
                    host=self.host,
                    port=self.port,
                    user=self.user,
                    password=self.password,
                    database=self.db_name,
            ) as connection:
                async with connection.cursor() as cursor:
                    cursor.execute(f"""SELECT id FROM "UsersData" WHERE tg_id = %s""", (tg_user_id,))
                    result = cursor.fetchone()
                    return result
        except (Exception, Error) as er:
            print("FAILED TO SEARCH USER ID")
            print(er)

    async def get_user_keys(self, tg_user_id):
        try:
            connection = await asyncpg.connect(
                host=self.host,
                port=self.port,
                user=self.user,
                password=self.password,
                database=self.db_name,
            )
            result = await connection.fetch(GetUserKeys_query, tg_user_id)
            if result:
                result = (result[0]['binance_api_key'], result[0]['binance_secret_api_key'])
            await connection.close()
            return result
        except (Exception, Error) as er:
            print("FAILED TO SEARCH USER BINANCE API KEYS")
            print(er)

    async def get_user_currency(self, user_id):
        try:
            async with asyncpg.connect(
                    host=self.host,
                    port=self.port,
                    user=self.user,
                    password=self.password,
                    database=self.db_name,
            ) as connection:
                async with connection.cursor() as cursor:
                    cursor.execute(f"""SELECT currency FROM "GeneralSettings" WHERE id = %s""", (user_id,))
                    result = cursor.fetchone()
                    return result
        except (Exception, Error) as er:
            print("FAILED TO FIND USER BINANCE FUTURES CURRENCY BALANCE")
            print(er)


if __name__ == '__main__':
    db = DbManager()
