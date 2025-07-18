import asyncio
from aiogram import Bot, Dispatcher, F
from aiogram.filters import CommandStart, Command
from aiogram.types import Message, CallbackQuery, ReplyKeyboardRemove
from config import TOKEN
import keyboards as kb

bot = Bot(token=TOKEN)
dp = Dispatcher()

# Задание 1: Reply-меню с кнопками "Привет" и "Пока"
@dp.message(CommandStart())
async def start(message: Message):
    await message.answer(
        f"Привет, {message.from_user.first_name}! Выберите действие:",
        reply_markup=ReplyKeyboardRemove()
    )
    await message.answer(
        "Меню:",
        reply_markup=kb.hello_bye_menu
    )

@dp.message(F.text == "Привет")
async def say_hello(message: Message):
    await message.answer(f"Привет, {message.from_user.first_name}!")

@dp.message(F.text == "Пока")
async def say_bye(message: Message):
    await message.answer(f"До свидания, {message.from_user.first_name}!")

# Задание 2: Инлайн-кнопки с URL-ссылками
@dp.message(Command('links'))
async def show_links(message: Message):
    await message.answer("Выберите ссылку:", reply_markup=kb.links_inline)

# Задание 3: Динамическая инлайн-клавиатура
@dp.message(Command('dynamic'))
async def dynamic_menu(message: Message):
    await message.answer("Динамическое меню:", reply_markup=kb.show_more_inline)

@dp.callback_query(F.data == 'show_more')
async def show_more_options(callback: CallbackQuery):
    await callback.message.edit_text(
        "Выберите опцию:",
        reply_markup=kb.options_inline
    )
    await callback.answer()

@dp.callback_query(F.data.in_(['option_1', 'option_2']))
async def option_selected(callback: CallbackQuery):
    text = "Вы выбрали Опция 1" if callback.data == 'option_1' else "Вы выбрали Опция 2"
    await callback.answer()
    await callback.message.answer(text)

async def main():
    await dp.start_polling(bot)

if __name__ == '__main__':
    asyncio.run(main())
