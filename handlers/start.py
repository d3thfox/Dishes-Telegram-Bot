from aiogram import Router, F,types
from aiogram.filters import Command
from handlers.review_dialog import start_review
from aiogram.fsm.context import FSMContext



start_router = Router()


user_id = set()

@start_router.message(Command("start"))
async def start(message: types.message):
    name = message.from_user.first_name
    users = len(user_id)
    kb = types.InlineKeyboardMarkup(
        inline_keyboard=[
            [
                types.InlineKeyboardButton(text = 'Оставить отзыв', callback_data = 'start_review'),
                types.InlineKeyboardButton(text='Добавить новый рецепт', callback_data='new_recipe'),
                types.InlineKeyboardButton(text='Отоброзить каталог', callback_data='call_catalog'),
            ]
        ]
    )
    kb_1 = types.ReplyKeyboardMarkup(
        keyboard=[
            [
                types.KeyboardButton(text='/my_info'),
                types.KeyboardButton(text='/random_recipe'),
                types.KeyboardButton(text='/start'),
            ]
        ],
        resize_keyboard = True
    )

    await message.answer(f'Привет!{name},\n'
                         f'Мы обслужили уже {users} пользователей\n'
                         f'Мои комманды:\n'
                         f'/start - начало работы с ботом\n'
                         f'/my_info - показывает всю информацию о вас\n'
                         f'/random_recipe - выбирает рандомный рецепт и отправляет вам', reply_markup=kb,)
    await message.answer('Можете выбрать команду',reply_markup=kb_1)




