from aiogram import Router, F, types
from aiogram.filters import Command
from aiogram.fsm.state import StatesGroup, State
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, InlineKeyboardButton, Message
from bot_config import database
from bot_config import admin_id



new_recipe_router = Router()
new_recipe_router.message.filter(F.from_user.id == 1787320714)
new_recipe_router.callback_query.filter(F.from_user.id == 1787320714)

class NewRecipe(StatesGroup):
    confirm = State()
    recipe = State()
    image = State()
    price = State()
    category = State()

@new_recipe_router.callback_query(F.data == "new_recipe")
async def new_recipe(callback_query : CallbackQuery, state: FSMContext):
    kb = types.InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text='Да',callback_data= 'yes'),
                InlineKeyboardButton(text='Не',callback_data= 'no'),
            ]
        ]
    )
    await callback_query.message.answer('Вы уверены?', reply_markup=kb)
    await state.set_state(NewRecipe.confirm)

@new_recipe_router.callback_query(F.data == 'no')
async def cancel(callback_query : CallbackQuery, state: FSMContext):
    await callback_query.message.answer('Отмена')
    await state.clear()

@new_recipe_router.callback_query(F.data == 'yes')
async def handler_confirm(callback : CallbackQuery, state: FSMContext):
    await callback.message.answer('Введите рецепт')
    await state.set_state(NewRecipe.recipe)

@new_recipe_router.message(NewRecipe.recipe)
async def handler_recipe(message : Message, state: FSMContext):
    await state.update_data(recipe=message.text)
    await message.answer('Введите ссылку на файл\n'
                         'Пример:image/cool_meat')
    await state.set_state(NewRecipe.image)

@new_recipe_router.message(NewRecipe.image)
async def handler_image(message : Message, state: FSMContext):
    await state.update_data(image=message.text)
    await message.answer('Введите цену')
    await state.set_state(NewRecipe.price)

@new_recipe_router.message(NewRecipe.price)
async def handler_price(message : Message, state: FSMContext):
    price = message.text
    if not price.isdigit():
        await message.answer('Вводите числа')
        return
    await message.answer('Введите категорию')
    await state.update_data(price=price)
    await state.set_state(NewRecipe.category)

@new_recipe_router.message(NewRecipe.category)
async def handler_category(message : Message, state: FSMContext):
    await state.update_data(category=message.text)
    data = await state.get_data()
    database.save_recipe(data)
    await message.answer('Рецепт добавлен')
    await state.clear()





