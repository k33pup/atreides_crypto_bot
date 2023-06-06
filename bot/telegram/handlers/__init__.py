from .user import register_all_user_handlers
from .admin import register_all_admin_handlers
from aiogram import Dispatcher


def setup_all_handlers(dp: Dispatcher):
    register_all_user_handlers(dp)
    register_all_admin_handlers(dp)


__all__ = ['register_all_user_handlers', 'register_all_admin_handlers', 'setup_all_handlers']
