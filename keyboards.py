from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

start_board = InlineKeyboardButton(text='Start', callback_data='start')
start = InlineKeyboardMarkup(resize_keyboard=True).row(start_board)

finish_board = InlineKeyboardButton(text='Show me', callback_data='finish')
finish = InlineKeyboardMarkup(resize_keyboard=True).row(finish_board)
