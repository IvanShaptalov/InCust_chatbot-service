from aiogram import types
from utils import useful_methods


async def send_text_message(message: types.Message):
    await message.reply('.')


async def connect_to_chat(callback: types.CallbackQuery):
    print(callback.data)
    event = useful_methods.get_event(callback)
    # with client_bot.with_token(config.BOT_TOKEN) as bot:
    #     await bot.send_photo(chat_id=callback.message.chat.id,
    #                          photo=event.get_media(),
    #                          caption=f'{event.stringify()}')


async def show_event(callback: types.CallbackQuery):
    print(callback.data)
    event = useful_methods.get_event(callback)
    # todonow send deep link
