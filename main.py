from aiogram import Bot,Dispatcher,types
from dotenv import dotenv_values
from aiogram.filters import  Command
from random import choice
import asyncio


token = dotenv_values(".env")['BOT_TOKEN']

bot = Bot(token=token)
dp = Dispatcher()

user_id = set()

@dp.message(Command("start"))
async def start(message: types.Message):
    global user_id
    name = message.from_user.first_name
    if message.from_user.id not in user_id:
        user_id.add(message.from_user.id)
    users = len(user_id)
    await message.answer(f'Привет!{name}, мы обслужили уже {users} пользователей ')


@dp.message(Command("my_info"))
async def my_info(message: types.Message):
    id = message.from_user.id
    username = message.from_user.username
    name = message.from_user.first_name
    await message.answer(f'Вот вся информация о вас :'
                         f'ID - {id}, Username - {username} , Name - {name}')

names = ['Alex','Dante','Vergil','Raiden','Sam']


@dp.message(Command("random"))
async def random_name(message: types.Message):
    await message.answer(f"{choice(names)}")

async def main():
   await dp.start_polling(bot)


if __name__ == '__main__':
    asyncio.run(main())



