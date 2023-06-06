from asyncpg import PostgresError
from sqlalchemy import select, delete
from .base import async_session
from .models.user_md import User
from .models.license_key_md import LicenseKey
from .models.user_license_md import License
from datetime import datetime
from typing import NoReturn


class DbManager:
    def __init__(self):
        pass

    @staticmethod
    async def add_user(tg_id: int) -> NoReturn:
        try:
            new_user = User()
            new_user.tg_id = tg_id
            new_user.join_date = datetime.utcnow()
            async with async_session() as db_sess:
                async with db_sess.begin():
                    db_sess.add(new_user)
                await db_sess.commit()
        except PostgresError as er:
            print("FAILED TO ADD USER")
            print(er)

    @staticmethod
    async def get_user_db_id(tg_user_id: int) -> int:
        try:
            async with async_session() as db_sess:
                id_query = select(User.id).where(User.tg_id == tg_user_id)
                return (await db_sess.execute(id_query)).first()
        except PostgresError as er:
            print("FAILED TO FIND USER DB ID")
            print(er)

    @staticmethod
    async def add_license_key(license_key_text: str, license_type: str,
                              duration: int) -> NoReturn:
        try:
            new_key = LicenseKey()
            new_key.key = license_key_text
            new_key.type = license_type
            new_key.duration = duration
            async with async_session() as db_sess:
                async with db_sess.begin():
                    db_sess.add(new_key)
                await db_sess.commit()
        except PostgresError as er:
            print("FAILED TO ADD LICENSE KEY")
            print(er)

    @staticmethod
    async def get_license_key(license_key_text: str) -> LicenseKey:
        try:
            async with async_session() as db_sess:
                id_query = select(LicenseKey).where(
                    LicenseKey.key == license_key_text)
                return (await db_sess.execute(id_query)).first()
        except PostgresError as er:
            print("FAILED TO FIND USER DB ID")
            print(er)

    @staticmethod
    async def delete_license_key(license_key_text: str) -> NoReturn:
        try:
            query = delete(LicenseKey).where(LicenseKey.key == license_key_text)
            async with async_session() as db_sess:
                async with db_sess.begin():
                    db_sess.execute(query)
                await db_sess.commit()
        except PostgresError as er:
            print("FAILED TO DELETE LI")
            print(er)

    @staticmethod
    async def add_user_license(user_id: int, license_type: str,
                               expire_date: datetime) -> NoReturn:
        try:
            new_license = License()
            new_license.user_id = user_id
            new_license.type = license_type
            new_license.expire_date = expire_date
            async with async_session() as db_sess:
                async with db_sess.begin():
                    db_sess.add(new_license)
                await db_sess.commit()
        except PostgresError as er:
            print("FAILED TO ADD USER LICENSE")
            print(er)


if __name__ == '__main__':
    db = DbManager()
