import asyncio
from aiogram import Bot, Dispatcher, F
from aiogram.filters import CommandStart
from aiogram.types import Message
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.storage.memory import MemoryStorage
import sqlite3
import logging
from config import TOKEN

# Инициализация бота и диспетчера
bot = Bot(token=TOKEN)
dp = Dispatcher()
logging.basicConfig(level=logging.INFO)

# Определение состояний
class StudentForm(StatesGroup):
    name = State()
    age = State()
    grade = State()

def init_db():
    conn = sqlite3.connect('school_data.db')
    cur = conn.cursor()
    cur.execute('''
        CREATE TABLE IF NOT EXISTS students (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            age INTEGER NOT NULL,
            grade TEXT NOT NULL
        )
    ''')
    conn.commit()
    conn.close()

init_db()

@dp.message(CommandStart())
async def start(message: Message, state: FSMContext):
    await message.answer("Привет! Как тебя зовут?")
    await state.set_state(StudentForm.name)

@dp.message(StudentForm.name)
async def get_name(message: Message, state: FSMContext):
    await state.update_data(name=message.text)
    await message.answer("Сколько тебе лет?")
    await state.set_state(StudentForm.age)

@dp.message(StudentForm.age)
async def get_age(message: Message, state: FSMContext):
    await state.update_data(age=message.text)
    await message.answer("В каком классе ты учишься?")
    await state.set_state(StudentForm.grade)

@dp.message(StudentForm.grade)
async def get_grade(message: Message, state: FSMContext):
    await state.update_data(grade=message.text)
    data = await state.get_data()
    # Сохраняем данные в базу данных
    conn = sqlite3.connect('school_data.db')
    cur = conn.cursor()
    cur.execute('INSERT INTO students (name, age, grade) VALUES (?, ?, ?)', (data['name'], data['age'], data['grade']))
    conn.commit()
    conn.close()
    await message.answer(f"Данные сохранены!\nИмя: {data['name']}\nВозраст: {data['age']}\nКласс: {data['grade']}")
    await state.clear()

async def main():
    await dp.start_polling(bot)

if __name__ == '__main__':
    asyncio.run(main())
