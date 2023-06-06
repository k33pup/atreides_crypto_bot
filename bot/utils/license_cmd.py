from random import choice
from string import ascii_uppercase
from bot.database.base import async_session
from bot.database.models.license_key_md import LicenseKey
from sqlalchemy import select


def create_license_key(length: int) -> str:
    alph = ascii_uppercase + "0123456789"
    return "".join([choice(alph) for i in range(length)])


async def check_license_key(key: str) -> bool:
    with async_session() as db_sess:
        check_query = select(LicenseKey.id).where(
            LicenseKey.key == key)
        return (await db_sess.execute(check_query)).first() is not None
