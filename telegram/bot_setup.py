from aiogram import Bot
from aiogram.dispatcher import Dispatcher
from aiogram.utils import executor
import os
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from data.db.mongo import DbManager
from telegram.handlers.UserCommands import *
from telegram.settings import log_error
import asyncio


def tele_main():
    token = os.getenv('BOT_TOKEN')
    BOT = Bot(token=token)
    storage = MemoryStorage()
    dp = Dispatcher(BOT, storage=storage)
    register_activate_handlers(dp)
    try:
        executor.start_polling(dp)
    except Exception as er:
        log_error.error(er)


if __name__ == '__main__':
    tele_main()
