from aiogram.dispatcher.filters import Text

from states.service import StatesGroup
from data import config
from . import chat
from . import chat_futures
from aiogram import Dispatcher


def setup(dp: Dispatcher):
    # in-chat futures
    dp.register_callback_query_handler(chat_futures.show_event, lambda callback: config.SHOW_EVENT_MARKER in callback.data, state='*')

    dp.register_callback_query_handler(chat_futures.connect_to_chat, lambda callback: config.CONNECT_TO_CHAT in callback.data,
                                       state='*')

    # exit from chat
    dp.register_message_handler(chat_futures.leave_chat, Text(equals=config.EXIT_FROM_CHAT), state='*')

    # chat
    # chat content sending
    dp.register_message_handler(chat.send_text_message, content_types=['text'], state=StatesGroup.in_chat)
    dp.register_message_handler(chat.send_location, content_types=['location'], state=StatesGroup.in_chat)
    dp.register_message_handler(chat.send_sticker, content_types=['sticker'], state=StatesGroup.in_chat)
    dp.register_message_handler(chat.send_photo, content_types=['photo'], state=StatesGroup.in_chat)
    dp.register_message_handler(chat.send_animation, content_types=['animation'], state=StatesGroup.in_chat)
    dp.register_message_handler(chat.send_audio, content_types=['audio'], state=StatesGroup.in_chat)
    dp.register_message_handler(chat.send_video, content_types=['video'], state=StatesGroup.in_chat)
    dp.register_message_handler(chat.send_voice, content_types=['voice'], state=StatesGroup.in_chat)
    # service_bot

