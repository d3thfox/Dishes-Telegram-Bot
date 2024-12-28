import asyncio

from bot_config import bot,dp
from  bot_config import database
from handlers import private_router
from handlers.group_menegment import group_router


async def on_startup(bot):
    database.create_table()
    database.create_table_new_recipe()


async def main():

   dp.include_routers(private_router,group_router)
   dp.startup.register(on_startup)
   await dp.start_polling(bot)






if __name__ == '__main__':
    asyncio.run(main())



