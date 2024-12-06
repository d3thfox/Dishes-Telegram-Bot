from aiogram import Router,types
from aiogram.filters import Command

start_router = Router()


user_id = set()

@start_router.message(Command("start"))
async def start(message: types.Message):
    global user_id
    name = message.from_user.first_name
    if message.from_user.id not in user_id:
        user_id.add(message.from_user.id)
    users = len(user_id)
    await message.answer(f'Привет!{name},\n'
                         f'Мы обслужили уже {users} пользователей\n'
                         f'Мои комманды:\n'
                         f'/start - начало работы с ботом\n'
                         f'/my_info - показывает всю информацию о вас\n'
                         f'/random_recipe - выбирает рандомный рецепт и отправляет вам')