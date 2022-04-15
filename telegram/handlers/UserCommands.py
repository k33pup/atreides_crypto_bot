from aiogram.dispatcher import FSMContext, Dispatcher
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram import types
from telegram.telegram_texts import *
from data.database.commands import DbManager

activate_key = '12345'


class UserStates(StatesGroup):
    introduction = State()
    password = State()
    api_key = State()
    secret_api_key = State()


async def start_activation(message: types.Message):
    await UserStates.introduction.set()
    await message.answer(intro_text)


async def answer_intro(message: types.Message, state: FSMContext):
    await UserStates.next()
    await message.answer(password_text)


async def answer_password(message: types.Message, state: FSMContext):
    if message.text != activate_key:
        await message.answer(bad_pass_text)
        return
    await UserStates.next()
    await message.answer(instruction_api_key)


async def answer_api_key(message: types.Message, state: FSMContext):
    await state.update_data(api_key=message.text)
    await UserStates.next()
    await message.answer(api_key_answer)
    await message.answer(instruction_secret_api_key)


async def answer_secret_api_key(message: types.Message, state: FSMContext):
    storage_data = await state.get_data()
    tg_user_id, api_key, secret_api_key, license_type = message.from_user.id, storage_data['api_key'], message.text, 'simple'
    db_manager = DbManager()
    # db_manager.add_user(tg_user_id, api_key, secret_api_key, license_type)
    await state.finish()
    await message.answer(accept_license)


def register_activate_handlers(dp: Dispatcher):
    dp.register_message_handler(start_activation, commands='start', state="*")
    dp.register_message_handler(answer_intro, commands='yes', state=UserStates.introduction)
    dp.register_message_handler(answer_password, state=UserStates.password)
    dp.register_message_handler(answer_api_key, state=UserStates.api_key)
    dp.register_message_handler(answer_secret_api_key, state=UserStates.secret_api_key)
