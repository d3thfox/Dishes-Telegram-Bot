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
    data = await state.get_data()
    database.save_recipe(data)
    await message.answer('Рецепт добавлен')
    await state.clear()





