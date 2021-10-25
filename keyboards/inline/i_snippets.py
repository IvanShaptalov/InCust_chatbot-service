from aiogram import types

from data import config, text_util
from keyboards.inline import inline_button


def sure_inline_keyboard(event_id: int) -> types.InlineKeyboardButton:
    return types.InlineKeyboardMarkup(). \
        add(
        inline_button(config.YES, f'{config.YES}:{event_id}'),
        inline_button(config.NO, f'{config.NO}:')
    )


def notification_inline_keyboard(event_id: int) -> types.InlineKeyboardButton:
    return types.InlineKeyboardMarkup().\
        add(
        inline_button(text_util.N_BUTTON_ANSWER, f'{config.ANSWER}:{event_id}'),
        inline_button(config.SHOW_EVENT_IN_CHAT, f'{config.SHOW_EVENT}:{event_id}')
    )

