
from aiogram import Router, types,F
from aiogram.fsm.state import StatesGroup, State
from aiogram.fsm.context import FSMContext
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery
from bot_config import database

review_router = Router()

class RestourantReview(StatesGroup):
    confirm = State()
    name = State()
    phone_number = State()
    food_rating = State()
    cleanliness_rating = State()
    extra_comments = State()
    time_data = State()

@review_router.callback_query(F.data == "start_review")
async def new_recipe(callback_query : CallbackQuery, state: FSMContext):
    user_id = callback_query.from_user.id
    user =  database.check_user_id(user_id)
    if user:
        await callback_query.message.answer('Вы уже оставляли отзыв')
        await callback_query.answer()
        await state.clear()
        return

    kb = types.InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text='Да',callback_data= 'yes'),
                InlineKeyboardButton(text='Не',callback_data= 'no'),
            ]
        ]
    )
    await callback_query.message.answer('Вы действительно хотите оставить отзыв?', reply_markup=kb)
    await callback_query.answer()
    await state.set_state(RestourantReview.confirm)

@review_router.callback_query(RestourantReview.confirm, F.data == 'no')
async def cancel(callback_query : CallbackQuery, state: FSMContext):
    await callback_query.message.answer('Отмена')
    await callback_query.answer()
    await state.clear()

@review_router.callback_query(RestourantReview.confirm,F.data == 'yes')
async def handler_confirm(callback : CallbackQuery, state: FSMContext):
    await callback.message.answer('Введите ваше имя')
    await callback.answer()
    await state.set_state(RestourantReview.name)


@review_router.callback_query(RestourantReview.name)
async def start_review(callback_query: CallbackQuery, state: FSMContext):
    await callback_query.message.answer('Введите ваше имя')
    await callback_query.answer()
    await state.set_state(RestourantReview.name)




@review_router.message(RestourantReview.name)
async def get_name(message: types.Message, state: FSMContext):
    name = message.text
    if not name.isalpha():
        await message.answer('Введите имя прописными буквами')
        return
    if len(name) < 3 or len(name) > 8:
        await message.answer('Имя не должно быть меньше 3 символов и не должно привышать 8')
        return
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
    await message.answer('Введите дату посещения\n'
                         'Пример(19.12.2024)')
    await state.set_state(RestourantReview.time_data)


@review_router.message(RestourantReview.time_data)
async def get_extra_comments(message: types.Message, state: FSMContext):
    if len(message.text) != 10:
        await message.answer('Превышенно допустмое колличество символов')
        return
    await state.update_data(time_data=message.text)
    await state.update_data(user_id=message.from_user.id)

    data = await state.get_data()
    database.save_survey(data)
    await message.answer(
        "Спасибо за пройденный опрос!\n\n"
        f"Ваше имя : {data['name']}\n"
        f"Ваш номер телефона: {data['phone_number']}\n"
        f"Оценка еды: {data['food_rating']}\n"
        f"Оценка чистоты: {data['cleanliness_rating']}\n"
        f"Комментарии: {data['extra_comments']}\n"
        f"Дата посещения : {data['time_data']}\n"
    )
    await state.clear()



