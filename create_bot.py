from config import *
import mysql_python

from aiogram import Bot
from aiogram.dispatcher import Dispatcher
from aiogram.contrib.fsm_storage.memory import MemoryStorage


bot = Bot(token = token)
dp = Dispatcher(bot, storage=MemoryStorage())
Dispatcher.set_current(dp)
db = mysql_python.DataBase(
	user = db_user,
	password = db_password,
	database = db_database,
	host = db_host
)