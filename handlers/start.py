from aiogram import Router, F,types
from aiogram.filters import Command
from handlers.review_dialog import start_review
from aiogram.fsm.context import FSMContext



start_router = Router()


user_id = set()

@start_router.message(Command("start"))
async def start(message: types.message):
    global user_id
    name = message.from_user.first_name
    if message.from_user.id not in user_id:
        user_id.add(message.from_user.id)
    users = len(user_id)
    kb = types.InlineKeyboardMarkup(
        inline_keyboard=[
            [
                types.InlineKeyboardButton(text = 'Оставить отзыв', callback_data = 'start_review'),
            ]
        ]
    )
    await message.answer(f'Привет!{name},\n'
                         f'Мы обслужили уже {users} пользователей\n'
                         f'Мои комманды:\n'
                         f'/start - начало работы с ботом\n'
                         f'/my_info - показывает всю информацию о вас\n'
                         f'/random_recipe - выбирает рандомный рецепт и отправляет вам', reply_markup=kb)



@start_router.callback_query(lambda callback: callback.data == "start_review")
async def start_review_callback(callback: types.CallbackQuery, state: FSMContext):
    await callback.message.answer("Вы начали оставлять отзыв!")
    await callback.answer()
    await start_review(callback, state)

