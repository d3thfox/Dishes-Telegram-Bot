import asyncio

from handlers.start import start_router
from handlers.random_recipe import random_recipe_router
from handlers.my_info import my_info_router
from bot_config import bot,dp



async def main():
   dp.include_routers(start_router,random_recipe_router,my_info_router)
   await dp.start_polling(bot)


if __name__ == '__main__':
    asyncio.run(main())



