
from aiogram import Router, types,F
from aiogram.fsm.state import StatesGroup, State
from aiogram.fsm.context import FSMContext
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery

review_router = Router()

class RestourantReview(StatesGroup):
    name = State()
    phone_number = State()
    food_rating = State()
    cleanliness_rating = State()
    extra_comments = State()

user_id = set()

@review_router.callback_query(F == 'start_review')
async def start_review(callback_query: CallbackQuery, state: FSMContext):
    if callback_query.from_user.id in user_id:
        await callback_query.message.answer('Вы уже оставляли отзыв')
        await state.clear()
        return
    await callback_query.message.answer('Введите ваше имя')
    await state.set_state(RestourantReview.name)

    user_id.add(callback_query.from_user.id)

@review_router.message(RestourantReview.name)
async def get_name(message: types.Message, state: FSMContext):
    await state.update_data(name=message.text)
    await message.answer('Введите ваш номер телефона (используйте код страны).\nПример: 996555111222')
    await state.set_state(RestourantReview.phone_number)

@review_router.message(RestourantReview.phone_number)
async def get_phone_number(message: types.Message, state: FSMContext):
    phone_number = message.text
    if not phone_number.isdigit():
        await message.answer('К вводу допускаются только числа. Попробуйте еще раз.')
        return
    if len(phone_number) != 12:
        await message.answer("Номер телефона должен состоять из 12 цифр. Попробуйте еще раз.")
        return
    await state.update_data(phone_number=phone_number)

    kb = InlineKeyboardMarkup(
        inline_keyboard=[[InlineKeyboardButton(text=str(i), callback_data=str(i)) for i in range(1, 6)]]
    )
    await message.answer('Выберите оценку (1-5)', reply_markup=kb)
    await state.set_state(RestourantReview.food_rating)

@review_router.callback_query(RestourantReview.food_rating)
async def get_food_rating(callback: CallbackQuery, state: FSMContext):
    food_rating = callback.data
    if not food_rating.isdigit() or int(food_rating) < 1 or int(food_rating) > 5:
        await callback.answer("Пожалуйста, выберите оценку от 1 до 5.")
        return
    await state.update_data(food_rating=food_rating)

    kb = InlineKeyboardMarkup(
        inline_keyboard=[[InlineKeyboardButton(text=str(i), callback_data=str(i)) for i in range(1, 6)]]
    )
    await callback.message.answer("Выберите оценку чистоты заведения (1-5)", reply_markup=kb)
    await state.set_state(RestourantReview.cleanliness_rating)
    await callback.answer()

@review_router.callback_query(RestourantReview.cleanliness_rating)
async def get_cleanliness_rating(callback: CallbackQuery, state: FSMContext):
    cleanliness_rating = callback.data
    if not cleanliness_rating.isdigit() or int(cleanliness_rating) < 1 or int(cleanliness_rating) > 5:
        await callback.answer("Пожалуйста, выберите оценку от 1 до 5.")
        return
    await state.update_data(cleanliness_rating=cleanliness_rating)
    await callback.message.answer("Можете ввести дополнительные комментарии/жалобы:")
    await state.set_state(RestourantReview.extra_comments)
    await callback.answer()


@review_router.message(RestourantReview.extra_comments)
async def get_extra_comments(message: types.Message, state: FSMContext):
    await state.update_data(extra_comments=message.text)

    data = await state.get_data()
    await message.answer(
        "Спасибо за пройденный опрос!\n\n"
        f"Ваше имя : {data['name']}\n"
        f"Ваш номер телефона: {data['phone_number']}\n"
        f"Оценка еды: {data['food_rating']}\n"
        f"Оценка чистоты: {data['cleanliness_rating']}\n"
        f"Комментарии: {data['extra_comments']}"
    )
    await state.clear()
