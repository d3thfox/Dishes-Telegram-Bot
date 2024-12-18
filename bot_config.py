from aiogram import Bot,Dispatcher
from dotenv import  dotenv_values

from database import Database

token = dotenv_values(".env")['BOT_TOKEN']
admin_id = dotenv_values(".env")['ADMIN_ID']

bot = Bot(token=token)
dp = Dispatcher()
database = Database('db.sqlite3')
