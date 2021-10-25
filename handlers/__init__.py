from states.service import ServiceStates
from data import config
from . import chat
from aiogram import Dispatcher


def setup(dp: Dispatcher):
    dp.register_message_handler(chat.send_text_message, content_types=['text'], state=ServiceStates.in_chat)
    dp.register_callback_query_handler(chat.show_event, lambda callback: config.SHOW_EVENT in callback.data)
    dp.register_callback_query_handler(chat.connect_to_chat, lambda callback: config.ANSWER in callback.data,
                                       state='*')
