from aiogram import Router, F,types
from aiogram.filters import Command
from handlers.review_dialog import start_review
from aiogram.fsm.context import FSMContext



start_router = Router()


user_id = set()

@start_router.message(Command("start"))
async def start(message: types.message):
    name = message.from_user.first_name
    if message.from_user.id not in user_id:
        user_id.add(message.from_user.id)
    users = len(user_id)
    kb = types.InlineKeyboardMarkup(
        inline_keyboard=[
            [
                types.InlineKeyboardButton(text = 'Оставить отзыв', callback_data = 'start_review'),
                types.InlineKeyboardButton(text='Добавить новый рецепт', callback_data='new_recipe'),
            ]
        ]

    )
    await message.answer(f'Привет!{name},\n'
                         f'Мы обслужили уже {users} пользователей\n'
                         f'Мои комманды:\n'
                         f'/start - начало работы с ботом\n'
                         f'/my_info - показывает всю информацию о вас\n'
                         f'/random_recipe - выбирает рандомный рецепт и отправляет вам', reply_markup=kb)




