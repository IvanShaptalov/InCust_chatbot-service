import handlers
from aiogram import executor
from data.bot_setup import dispatcher


if __name__ == '__main__':
    handlers.setup(dispatcher)
    executor.start_polling(dispatcher, skip_updates=True)
