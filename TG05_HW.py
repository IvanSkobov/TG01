import asyncio
from aiogram import Bot, Dispatcher, F
from aiogram.filters import Command
from aiogram.types import Message
import requests
from config import TOKEN, NASA_API_KEY, WEATHER_API_KEY, DADATA_API_KEY, RAPIDAPI_KEY, POLYGON_API_KEY

bot = Bot(token=TOKEN)
dp = Dispatcher()

# 1. Факт о котах
@dp.message(Command("catfact"))
async def cat_fact(message: Message):
    url = "https://catfact.ninja/fact"
    fact = requests.get(url).json().get("fact", "Факт не найден.")
    await message.answer(f"Факт о котах: {fact}")

# 2. NASA APOD
@dp.message(Command("nasa"))
async def nasa_apod(message: Message):
    url = f"https://api.nasa.gov/planetary/apod?api_key={NASA_API_KEY}"
    data = requests.get(url).json()
    photo_url = data.get("url")
    title = data.get("title", "Без названия")
    explanation = data.get("explanation", "Нет описания")
    await message.answer_photo(photo=photo_url, caption=f"{title}\n\n{explanation}")

# 3. Шутка
@dp.message(Command("joke"))
async def joke(message: Message):
    url = "https://v2.jokeapi.dev/joke/Any?lang=ru"
    data = requests.get(url).json()
    if data["type"] == "single":
        await message.answer(data["joke"])
    else:
        await message.answer(f"{data['setup']}\n\n{data['delivery']}")

# 4. Погода
@dp.message(Command("weather"))
async def weather(message: Message):
    args = message.text.split(maxsplit=1)
    if len(args) < 2:
        await message.answer("Укажите город: /weather Москва")
        return
    city = args[1]
    url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={WEATHER_API_KEY}&units=metric&lang=ru"
    data = requests.get(url).json()
    if data.get("cod") != 200:
        await message.answer("Город не найден.")
        return
    temp = data["main"]["temp"]
    desc = data["weather"][0]["description"]
    await message.answer(f"Погода в {city}:\n{desc.capitalize()}, {temp}°C")

# 5. SpaceX — последние 3 запуска
@dp.message(Command("spacex"))
async def spacex_launches(message: Message):
    url = "https://api.spacexdata.com/v3/launches?limit=3"
    launches = requests.get(url).json()
    for launch in launches:
        name = launch.get("mission_name", "Без названия")
        date = launch.get("launch_date_utc", "Нет даты")
        links = launch.get("links", {})
        photos = links.get("flickr_images") or []
        photo_url = photos[0] if photos else links.get("mission_patch")
        caption = f"🚀 {name}\nДата: {date}"
        if photo_url:
            await message.answer_photo(photo=photo_url, caption=caption)
        else:
            await message.answer(caption)

# 6. Dadata — поиск марки авто
@dp.message(Command("car"))
async def car_brand(message: Message):
    args = message.text.split(maxsplit=1)
    if len(args) < 2:
        await message.answer("Укажите марку: /car форд")
        return
    query = args[1]
    url = "https://suggestions.dadata.ru/suggestions/api/4_1/rs/suggest/car_brand"
    headers = {
        "Content-Type": "application/json",
        "Accept": "application/json",
        "Authorization": f"Token {DADATA_API_KEY}"
    }
    data = {"query": query}
    resp = requests.post(url, headers=headers, json=data).json()
    if resp.get("suggestions"):
        result = []
        for s in resp["suggestions"]:
            info = s["data"]
            name = s["value"]
            country = info.get("country", None)
            code = info.get("code", None)
            name_en = info.get("name", None)
            info_lines = [f"Марка: {name}"]
            if country:
                info_lines.append(f"Страна: {country}")
            if code:
                info_lines.append(f"Код: {code}")
            if name_en:
                info_lines.append(f"Англ: {name_en}")
            result.append("\n".join(info_lines))
        await message.answer("\n\n".join(result))
    else:
        await message.answer("Марка не найдена.")

# 7. Polygon.io Stocks API — цена акции по тикеру
@dp.message(Command("stock"))
async def stock_info(message: Message):
    args = message.text.split(maxsplit=1)
    if len(args) < 2:
        await message.answer("Укажите тикер: /stock AAPL")
        return
    ticker = args[1].upper()
    url = f"https://api.polygon.io/v2/aggs/ticker/{ticker}/prev?adjusted=true&apiKey={POLYGON_API_KEY}"
    resp = requests.get(url).json()
    results = resp.get("results")
    if results and len(results) > 0:
        price = results[0].get("c")
        open_price = results[0].get("o")
        high = results[0].get("h")
        low = results[0].get("l")
        volume = results[0].get("v")
        await message.answer(
            f"Тикер: {ticker}\nЦена закрытия: {price}\nОткрытие: {open_price}\nМакс: {high}\nМин: {low}\nОбъем: {volume}"
        )
    else:
        await message.answer("Нет данных по тикеру.")

async def main():
    await dp.start_polling(bot)

if __name__ == '__main__':
    asyncio.run(main())
