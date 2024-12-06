from aiogram import Router,types
from aiogram.filters import Command

my_info_router = Router()


@my_info_router.message(Command("my_info"))
async def my_info(message: types.Message):
    id = message.from_user.id
    username = message.from_user.username
    name = message.from_user.first_name
    if username is None:
        await message.answer(f'Вот вся информация о вас:\n'
                         f'ID - {id}\n'
                         f'Ваше имя - {name}\n'
                         'У вас нет никнейма')
    else:
        await message.answer(f'Вот вся информация о вас:\n'
                             f'ID - {id}\n'
                             f'Ваше имя - {name}\n'
                             f'Ваш никнейм - @{username}')
