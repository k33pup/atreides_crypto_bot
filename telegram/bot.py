from aiogram import Bot, types
from aiogram.dispatcher import Dispatcher
from aiogram.utils import executor
import os

token = os.getenv('BOT_TOKEN')
BOT = Bot(token)
dp = Dispatcher(BOT)


@dp.message_handler()
async def echo_send(message: types.Message):
    await BOT.send_message(message.from_user.id, message.text)

executor.start_polling(dp, skip_updates=True)
