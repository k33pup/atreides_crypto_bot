from aiogram.dispatcher import Dispatcher
from aiogram import types
from bot.telegram.templates.telegram_texts import *
from bot.settings.config import licenses, key_length
from bot.database.db_commands import DbManager
from bot.utils.license_cmd import create_license_key


async def create_license(message: types.Message):
    message_data = message.text.split()[1:]
    if len(message_data) != 2:
        await message.answer(bad_license_cmd, parse_mode="Markdown")
        return
    if message[0] not in licenses:
        await message.answer(bad_license_type)
        return
    if not message[1].isdigit():
        await message.answer(bad_days_license)
        return
    license_type, duration = message_data[0], int(message_data[1])
    license_key = create_license_key(key_length)
    await DbManager.add_license_key(license_key, license_type, duration)
    await message.answer(accept_license_create.format(license_key, duration),
                         parse_mode="Markdown")


async def answer_password(message: types.Message):
    pass


def setup_license_handlers(dp: Dispatcher):
    dp.register_message_handler(create_license, commands='new_license', is_admin=True)
    dp.register_message_handler(answer_password)
