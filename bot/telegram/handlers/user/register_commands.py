from aiogram.dispatcher import Dispatcher
from aiogram import types
from bot.telegram.templates.telegram_texts import *
from bot.utils.license_cmd import check_license_key
from bot.database.db_commands import DbManager
from datetime import datetime, timedelta

async def start(message: types.Message):
    await message.answer(intro_text)


async def activate_license(message: types.Message):
    if len(message.text.split()) != 2:
        await message.answer(bad_pass_text)
        return
    license_key_text = message.text.split()[1]
    if not check_license_key(license_key_text):
        await message.answer(bad_pass_text)
        return
    license_key = await DbManager.get_license_key(license_key_text)
    expire_date = datetime.utcnow() + timedelta(days=license_key.duration)
    await DbManager.add_user_license(message.from_user.id, license_key.type,
                                     expire_date)
    await DbManager.delete_license_key(license_key_text)
    await message.answer(accept_license)


def setup_register_handlers(dp: Dispatcher):
    dp.register_message_handler(start, commands='start', state="*")
    dp.register_message_handler(activate_license, commands='activate')
