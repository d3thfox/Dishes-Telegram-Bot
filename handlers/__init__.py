from aiogram import Router,F

from .start import start_router
from .random_recipe import random_recipe_router
from .my_info import my_info_router
from .review_dialog import review_router
from .new_recipe import new_recipe_router
from .catalog import catalog_router

private_router = Router()

private_router.include_routers(start_router, random_recipe_router, my_info_router, review_router, new_recipe_router, catalog_router)

private_router.message.filter(F.chat.type == 'private')
private_router.callback_query.filter(F.chat.type == 'private')