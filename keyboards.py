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

inline_keyboard_test = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text='Каталог', callback_data='catalog')],
        [
            InlineKeyboardButton(text='Новости', callback_data='news')],
        [
            InlineKeyboardButton(text='Профиль', callback_data='profile')]
    ])

test = ['chatgpt', 'кнопка 2', 'кнопка 3', 'кнопка 4']


async def test_keyboard():
    keyboard = InlineKeyboardBuilder()
    for key in test:
        keyboard.add(InlineKeyboardButton(text=key, url='https://chatgpt.com/'))
    return keyboard.adjust(2).as_markup()

# Задание 1: Reply-меню с кнопками "Привет" и "Пока"
hello_bye_menu = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="Привет"), KeyboardButton(text="Пока")],
    ],
    resize_keyboard=True
)

# Задание 2: Инлайн-кнопки с URL-ссылками
links_inline = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text="Новости", url="https://tengrinews.kz/")],
        [InlineKeyboardButton(text="Музыка", url="https://music.yandex.ru")],
        [InlineKeyboardButton(text="Видео", url="https://www.youtube.com")],
    ]
)

# Задание 3: Динамическая инлайн-клавиатура
show_more_inline = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text="Показать больше", callback_data="show_more")],
    ]
)

options_inline = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text="Опция 1", callback_data="option_1"),
            InlineKeyboardButton(text="Опция 2", callback_data="option_2"),
        ]
    ]
)
