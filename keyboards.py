from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils.keyboard import ReplyKeyboardBuilder, InlineKeyboardBuilder


main_menu = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text='📊 Таблица'),
            KeyboardButton(text='👤 Профиль'),
        ],
        [
            KeyboardButton(text='📝 Задания'),
            KeyboardButton(text='📝 Помощь'),
        ],
    ],
    resize_keyboard=True
)

inline_keyboard = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text='Видео', url='https://www.youtube.com/watch?v=m5VXMbWBW6c&list=RDm5VXMbWBW6c&start_radio=1'),
        ],
    ]
)

test = ['кнопка 1', 'кнопка 2', 'кнопка 3', 'кнопка 4']


async def test_keyboard():
    keyboard = ReplyKeyboardBuilder()
    for key in test:
        keyboard.add(KeyboardButton(text=key))
    return keyboard.adjust(2).as_markup()
