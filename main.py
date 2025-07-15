import asyncio
from aiogram import Bot, Dispatcher, F
from aiogram.filters import CommandStart, Command
from aiogram.types import Message, FSInputFile

from config import TOKEN

import random
import aiohttp

from gtts import gTTS
import os
from googletrans import Translator

bot = Bot(token=TOKEN)
dp = Dispatcher()

translator = Translator()

@dp.message(Command('voice'))
async def send_voice(message: Message):
    voice = FSInputFile('sample.ogg')
    await message.answer_voice(voice)

@dp.message(Command('doc'))
async def doc(message: Message):
    doc = FSInputFile('TG02.pdf')
    await bot.send_document(message.chat.id, doc)

@dp.message(Command('video'))
async def video(message: Message):
    await bot.send_chat_action(message.chat.id, 'upload_video')
    video = FSInputFile('video.mp4')
    await bot.send_video(message.chat.id, video)

@dp.message(Command('audio'))
async def audio(message: Message):
    audio = FSInputFile('audio.mp3')
    await bot.send_audio(message.chat.id, audio)

@dp.message(Command('training'))
async def training(message: Message):
    training_list = [
        "Тренировка 1:\n1. Скручивания: 3 подхода по 15 повторений\n2. Велосипед: 3 подхода по 20 повторений (каждая сторона)\n3. Планка: 3 подхода по 30 секунд",
        "Тренировка 2:\n1. Подъемы ног: 3 подхода по 15 повторений\n2. Русский твист: 3 подхода по 20 повторений (каждая сторона)\n3. Планка с поднятой ногой: 3 подхода по 20 секунд (каждая нога)",
        "Тренировка 3:\n1. Скручивания с поднятыми ногами: 3 подхода по 15 повторений\n2. Горизонтальные ножницы: 3 подхода по 20 повторений\n3. Боковая планка: 3 подхода по 20 секунд (каждая сторона)"
    ]
    rand_tr = random.choice(training_list)
    await message.answer(f"Это ваша мини-тренировка на сегодня {rand_tr}")

    tts = gTTS(text=rand_tr, lang='ru')
    tts.save("training.ogg")
    audio = FSInputFile('training.ogg')
    await bot.send_voice(message.chat.id, audio)
    os.remove("training.ogg")

@dp.message(Command('photo', prefix='&'))
async def photo(message: Message):
    list = ['https://i.pinimg.com/736x/60/74/03/6074038a30411cb9860094fbfd7cf1ec.jpg', 'https://i.pinimg.com/736x/f5/33/f5/f533f5c1adff152ba5c6fadff9e062a3.jpg', 'https://png.pngtree.com/png-vector/20240708/ourlarge/pngtree-skull-clipart-vector-png-image_13021653.png']
    rand_photo = random.choice(list)
    await message.answer_photo(photo=rand_photo, caption="Это супер крутая картинка!")

@dp.message(F.photo)
async def save_photo(message: Message):
    os.makedirs("img", exist_ok=True)
    photo = message.photo[-1]
    file_path = f"img/{photo.file_id}.jpg"
    await bot.download(photo, destination=file_path)
    await message.answer("Фото сохранено!")

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
    await message.answer(f'Привет, {message.from_user.first_name} !')

# Удаляю оба универсальных обработчика @dp.message() и заменяю на один универсальный
@dp.message()
async def universal_handler(message: Message):
    if message.text == 'Привет':
        await message.answer('Привет, чем я могу тебе помочь?')
    else:
        try:
            result = translator.translate(message.text, src='ru', dest='en')
            await message.answer(f"Перевод на английский:\n{result.text}")
        except Exception as e:
            await message.answer(f"Ошибка перевода: {e}")


async def main():
    await dp.start_polling(bot)


if __name__ == '__main__':
    asyncio.run(main())