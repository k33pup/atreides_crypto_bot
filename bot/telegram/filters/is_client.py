import typing
from aiogram.dispatcher.filters import BoundFilter
from bot.database.db_commands import DbManager
from bot.config import ADMINS


class ClientFilter(BoundFilter):
    key = 'is_client'

    def __init__(self, is_client: typing.Optional[bool] = None):
        self.is_client = is_client

    async def check(self, obj):
        if self.is_client is None:
            return False
        return (await DbManager.get_user_db_id(obj.from_user.id) is not None) or obj.from_user.id in ADMINS

