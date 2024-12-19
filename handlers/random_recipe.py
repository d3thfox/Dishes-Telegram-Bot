from aiogram import Router, types
from aiogram.filters import  Command
from bot_config import database

random_recipe_router = Router()


@random_recipe_router.message(Command("random_recipe"))
async def random_name(message: types.Message):
    random_recipe = database.random_rec()
    photo = types.FSInputFile(random_recipe[1])
    title = random_recipe[0]
    await message.answer_photo(photo=photo, caption=title)