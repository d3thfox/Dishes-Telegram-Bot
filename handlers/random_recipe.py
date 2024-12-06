from aiogram import Router, types
from aiogram.filters import  Command
from random import choice
from recipes import rec

random_recipe_router = Router()


@random_recipe_router.message(Command("random_recipe"))
async def random_name(message: types.Message):
    random_recipe = choice(rec)
    photo = types.FSInputFile(random_recipe[0])
    await message.answer_photo(photo=photo, caption=random_recipe[1])