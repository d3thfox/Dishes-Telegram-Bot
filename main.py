import asyncio


from handlers.new_recipe import new_recipe_router
from handlers.start import start_router
from handlers.random_recipe import random_recipe_router
from handlers.my_info import my_info_router
from bot_config import bot,dp
from handlers.review_dialog import review_router
from  bot_config import database


async def on_startup(bot):
    database.create_table()
    database.create_table_new_recipe()


async def main():
   dp.include_routers(start_router,random_recipe_router,my_info_router,review_router,new_recipe_router)
   dp.startup.register(on_startup)
   await dp.start_polling(bot)




if __name__ == '__main__':
    asyncio.run(main())



