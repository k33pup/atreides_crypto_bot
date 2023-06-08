from bot.database.base import __init__models
from aiogram import Bot
from aiogram.dispatcher import Dispatcher
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from bot.config import BOT_TOKEN, NEED_TO_INIT_MODELS
from .filters import register_all_filters
from .handlers import setup_all_handlers


async def run_telegram():

    bot = Bot(BOT_TOKEN)
    storage = MemoryStorage()
    dp = Dispatcher(bot, storage=storage)

    if NEED_TO_INIT_MODELS:
        await __init__models()

    register_all_filters(dp)
    setup_all_handlers(dp)

    try:
        await dp.start_polling()
    finally:
        await dp.storage.close()
        await dp.storage.wait_closed()
        await bot.session.close()
