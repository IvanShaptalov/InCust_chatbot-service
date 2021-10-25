from aiogram import types

import filters
from data import config, text_util
from keyboards.inline import inline_button


def in_chat_inline_keyboard(event_id: int, chat_id: str) -> types.InlineKeyboardButton:
    """
    send inline keyboard if user not in chat
    :param event_id: event id
    :param chat_id: telegram user chat id
    :return: types.InlineKeyboardButton
    """
    if not filters.filters.user_in_chat(chat_id, 'client'):
        return types.InlineKeyboardMarkup(). \
            add(
            inline_button(config.EVENT_ANSWER, f'{config.CONNECT_TO_CHAT}:{event_id}:{chat_id}'),
            inline_button(config.SHOW_EVENT_IN_CHAT, f'{config.SHOW_EVENT_MARKER}:{event_id}')
        )
