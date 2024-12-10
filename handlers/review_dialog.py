import uuid

from aiogram import Router, F, types
from aiogram.filters import Command, state
from aiogram.fsm.state import StatesGroup,State
from aiogram.fsm.context import FSMContext
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery

review_router = Router()

class RestourantReview(StatesGroup):
    phone_number = State()
    food_rating = State()
    cleanliness_rating = State()
    extra_comments = State()

user_id = set()


@review_router.message(Command('start_review'))
async def start_review(message: types.Message, state: FSMContext):
    if message.from_user.id in user_id:
        await message.answer("Вы уже оставляли отзыв.")
        await state.clear()
        return
    await message.answer('Введите ваш номер телефона (используйте код страны).\n'
                         'Пример: 996555111222')
    await state.set_state(RestourantReview.phone_number)

    user_id.add(message.from_user.id)


@review_router.message(RestourantReview.phone_number)
async def get_phone_number(message: types.Message, state: FSMContext):
    phone_number = message.text
    if not phone_number.isdigit():
       await message.answer('К вводу допускаются только числа. Попробуйте еще раз.')
    if len(phone_number) != 12:
        await message.answer("Номер телефона должен состоять из 12 цифр. Попробуйте еще раз.")
        return
    await state.update_data(phone_number=phone_number)
    kb = types.InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text=str(i), callback_data=str(i)) for i in range(1, 6)]
        ]
    )
    await message.answer('Выберите оценку (1-5)',reply_markup=kb)
    await state.set_state(RestourantReview.food_rating)

@review_router.callback_query(RestourantReview.food_rating)
async def get_food_rating(callback: types.CallbackQuery, state: FSMContext):
    food_rating = callback.data
    if not food_rating.isdigit() or int(food_rating) < 1 or int(food_rating) > 5:
        await callback.answer("Пожалуйста, выберите оценку от 1 до 5.")
        return
    await state.update_data(food_rating=food_rating)

    kb = types.InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text=str(i), callback_data=str(i)) for i in range(1, 6)]
        ]
    )
    await callback.message.answer("Выберите оценку чистоты заведеня (1-5)",reply_markup=kb)
    await state.set_state(RestourantReview.cleanliness_rating)
    await callback.answer()

@review_router.callback_query(RestourantReview.cleanliness_rating)
async def get_cleanliness_rating(callback: types.CallbackQuery, state: FSMContext):
    cleanliness_rating = callback.data
    if not cleanliness_rating.isdigit() or int(cleanliness_rating) < 1 or int(cleanliness_rating) > 5:
        await callback.answer("Пожалуйста, выберите оценку от 1 до 5.")
        return
    await state.update_data(cleanliness_rating=cleanliness_rating)
    await callback.message.answer("Можете ввести дополнительные комментарии/жалобы:")
    await state.set_state(RestourantReview.extra_comments)
    await callback.answer()

@review_router.message(RestourantReview.extra_comments)
async def get_extra_comments(message : types.message, state: FSMContext):
    await state.update_data(extra_comments=message.text)

    data = await state.get_data()
    await message.answer(
        "Спасибо за пройденный опрос!\n\n"
        f"Ваш номер телефона: {data['phone_number']}\n"
        f"Оценка еды: {data['food_rating']}\n"
        f"Оценка чистоты: {data['cleanliness_rating']}\n"
        f"Комментарии: {data['extra_comments']}"
    )
    await state.clear()









