from aiogram import Bot, Dispatcher
from aiogram.contrib.fsm_storage.memory import MemoryStorage

from data.config import BOT_TOKEN, CLIENT_BOT_TOKEN


client_bot = Bot(token=CLIENT_BOT_TOKEN)
service_bot = Bot(token=BOT_TOKEN)
dispatcher = Dispatcher(service_bot, storage=MemoryStorage())
