import typing
from aiogram.dispatcher.filters import BoundFilter
from bot.config import ADMINS


class AdminFilter(BoundFilter):
    key = 'is_admin'

    def __init__(self, is_admin: typing.Optional[bool] = None):
        self.is_admin = is_admin

    async def check(self, obj):
        if self.is_admin is None:
            return False
        return (obj.from_user.id in ADMINS) == self.is_admin
