from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

introduction_keyboard = InlineKeyboardMarkup(row_width=1)
introduction_keyboard.add(InlineKeyboardButton(text='Я СОГЛАСЕН', callback_data='wants_activate'))
password_keyboard = InlineKeyboardMarkup(row_width=1)
password_keyboard.add(InlineKeyboardButton(text='ВВЕСТИ КЛЮЧ ДОСТУПА', callback_data='wants_password'))
confirm_keyboard = InlineKeyboardMarkup(row_width=1)
confirm_keyboard.add(InlineKeyboardButton(text='ПОДТВЕРЖДАЮ СВОЕ СОГЛАСИЕ', callback_data='wants_continue'))
