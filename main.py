import asyncio
from aiogram import Bot, Dispatcher, F
from aiogram.filters import CommandStart, Command
from aiogram.types import Message

from config import TOKEN

import random
import aiohttp

bot = Bot(token=TOKEN)
dp = Dispatcher()

@dp.message(Command('photo'))
async def photo(message: Message):
    list = ['https://i.pinimg.com/736x/60/74/03/6074038a30411cb9860094fbfd7cf1ec.jpg', 'https://i.pinimg.com/736x/f5/33/f5/f533f5c1adff152ba5c6fadff9e062a3.jpg', 'https://png.pngtree.com/png-vector/20240708/ourlarge/pngtree-skull-clipart-vector-png-image_13021653.png']
    rand_photo = random.choice(list)
    await message.answer_photo(photo=rand_photo, caption="Это супер крутая картинка!")

@dp.message(F.photo)
async def aitext(message: Message):
    list = ["Ого какое фото!!!", "Не отправляй мне такое больше", "Не понял что это такое?"]
    rand_answ = random.choice(list)
    await message.answer(rand_answ)

@dp.message(F.text == "Что такое ИИ?")
async def aitext(message: Message):
    await message.answer('Искусственный интеллект (ИИ) – это область компьютерных наук, занимающаяся разработкой систем, которые могут выполнять задачи, требующие человеческого интеллекта. Проще говоря, это технологии, позволяющие машинам «думать» и «учиться» подобно людям, обрабатывая данные и принимая решения. ')

@dp.message(Command('weather'))
async def weather(message: Message):
    city = 'Samara'
    api_key = 'c1569892fe7c201402fd0bb2547cb09c'
    url = f'http://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric&lang=ru'
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as resp:
            data = await resp.json()
            if resp.status == 200:
                temp = data['main']['temp']
                description = data['weather'][0]['description']
                await message.answer(f'Погода в Самаре: {temp}°C, {description}')
            else:
                error_message = data.get('message', 'Неизвестная ошибка')
                await message.answer(f'Ошибка: {error_message}')


@dp.message(Command('help'))
async def help(message: Message):
    await message.answer('Этот бот умеет выполнять команды: \n /start \n /help')


@dp.message(CommandStart())
async def start(message: Message):
    await message.answer('Привет!')



async def main():
    await dp.start_polling(bot)


if __name__ == '__main__':
    asyncio.run(main())