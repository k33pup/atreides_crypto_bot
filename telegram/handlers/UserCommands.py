from aiogram.dispatcher import FSMContext, Dispatcher
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram import types
from telegram.keyboards import *
from telegram.settings import *
from extra.settings import activate_key
from data.db.mongo import DbManager


class UserStates(StatesGroup):
    introduction = State()
    password = State()


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
    await state.finish()
    database = DbManager()
    database.add_user(message.from_user.id, 'simple', message.chat.id)
    await message.answer(accept_license)


def register_activate_handlers(dp: Dispatcher):
    dp.register_message_handler(start_activation, commands='start', state="*")
    dp.register_message_handler(answer_intro, commands='yes', state=UserStates.introduction)
    dp.register_message_handler(answer_password, state=UserStates.password)
