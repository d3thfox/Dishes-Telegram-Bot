from aiogram import Router, types,F
from aiogram.filters import  Command
from aiogram.types import FSInputFile

from bot_config import database

catalog_router = Router()

@catalog_router.callback_query(F.data == 'call_catalog')
async def call_catalog_callback_query(callback_query: types.CallbackQuery):
    catalog = database.select_catalog()
    for i in catalog:
        photo = FSInputFile(i['image'])
        name = i['name']
        price = i['price']
        await callback_query.message.answer_photo(photo=photo,caption=f'Название: {name}\n'
                                                                      f'Цена: {price}')
        await callback_query.answer()