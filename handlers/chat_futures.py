import logging

from aiogram import types
from aiogram.dispatcher import FSMContext

import keyboards
from data import config, text_util
from data.bot_setup import service_bot
from models import db
from states.service import StatesGroup
from utils import useful_methods


async def connect_to_chat(callback: types.CallbackQuery, state: FSMContext):
    print(callback.data)

    event = useful_methods.get_event(callback)
    user_chat_id = useful_methods.get_id_from_data(callback.data, 2)
    user = db.get_from_db_multiple_filter(db.User, [db.User.chat_id == user_chat_id])
    if isinstance(event, db.Event) and isinstance(user, db.User):
        print(callback.data)
        await state.update_data(sender_chat_id=user_chat_id)
        await state.update_data(event_id=event.id)
        await StatesGroup.in_chat.set()
        logging.info(f'enter in chat , state - {await state.get_state()}')

        db.User.set_in_chat(callback.message.chat.id, True, 'service')
        await callback.message.reply(
            text_util.ENTER_IN_CHAT.format(event.title,
                                           user.user_fullname),
            reply_markup=keyboards.r_snippets.exit_from_chat_or_show_event())
    else:
        await callback.message.reply(text_util.EVENT_DELETED)
        if state:
            await state.finish()


async def leave_chat(message: types.Message, state: FSMContext):
    await state.finish()
    db.User.set_in_chat(message.chat.id, False, 'client')
    logging.info('leave chat, chat state finish')
    await service_bot.send_message(message.chat.id,
                                   text_util.LEFT_CHAT,
                                   reply_markup=keyboards.r_snippets.remove())


async def show_event(callback: types.CallbackQuery):
    print(callback.data)
    event = useful_methods.get_event(callback)
    chat_id = callback.message.chat.id
    if isinstance(event, db.Event):
        with service_bot.with_token(config.CLIENT_BOT_TOKEN) as bot:
            await service_bot.send_photo(chat_id=chat_id,
                                         photo=event.get_media(),
                                         caption=f'{event.stringify()}')
        await service_bot.send_message(chat_id,
                                       text_util.LINKER_TO_CLIENT)
    else:
        await service_bot.send_message(chat_id,
                                       text_util.EVENT_DELETED)
    # todonow send deep link
