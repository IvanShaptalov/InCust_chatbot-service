import logging
import os
from abc import abstractmethod
from copy import copy

from aiogram import types

import keyboards.reply.r_snippets
from data import text_util, config
from data.bot_setup import client_bot, service_bot
from models import db


class BaseSender:

    def __init__(self, event_id, sender_id):
        self.event_id = event_id
        self.sender_id = sender_id
        self.event, self._owner = self._get_event()
        self.sender = self._get_sender()

    def get_answer_markup(self):
        return keyboards.i_snippets.in_chat_inline_keyboard(event_id=self.event_id,
                                                            receiver_chat_id=self.get_owner().chat_id,
                                                            sender_chat_id=self.sender_id)

    def check_that_event_exists(self):
        return False if self.event is None else True

    def get_owner(self) -> db.User:
        return self._owner

    def _get_event(self):
        session = db.session
        with session:
            event = db.get_from_db_multiple_filter(table_class=db.Event,
                                                   identifier_to_value=[db.Event.id == self.event_id],
                                                   open_session=session)
            if isinstance(event, db.Event):
                owner = copy(event.event_owner)
                return event, owner
            else:
                return None

    def _get_sender(self) -> db.User:
        sender = db.get_from_db_multiple_filter(db.User, [db.User.chat_id == self.sender_id])
        assert isinstance(sender, db.User)
        return sender

    def prepare_to_send(self):
        text = text_util.NOTIFICATION.format(self.event.title, self.sender.user_fullname)
        return text

    @abstractmethod
    def forward_data(self, data):
        pass


class TextSender(BaseSender):
    async def forward_data(self, data: types.Message):
        user_in_service_bot = False
        with service_bot.with_token(config.CLIENT_BOT_TOKEN):
            chat_id = self.sender_id

            text = "{} {}".format(self.prepare_to_send(), data.text)
            try:
                await service_bot.send_message(chat_id=chat_id,
                                               text=text,
                                               reply_markup=self.get_answer_markup())
                user_in_service_bot = True
            except Exception as e:
                logging.warning(e, 'not register in bot')
        if not user_in_service_bot:
            await service_bot.send_message(chat_id=self.sender_id,
                                           text=text_util.LINKER_TO_CLIENT)


class LocationSender(BaseSender):
    async def forward_data(self, data: types.Message):
        user_in_service_bot = False
        with service_bot.with_token(config.CLIENT_BOT_TOKEN):
            chat_id = self.sender_id

            text = "{}".format(self.prepare_to_send())
            try:
                await service_bot.send_message(chat_id=chat_id,
                                               text=text,
                                               reply_markup=self.get_answer_markup())
                await service_bot.send_location(chat_id=chat_id,
                                                latitude=data.location.latitude,
                                                longitude=data.location.longitude)
                user_in_service_bot = True
            except Exception as e:
                logging.warning(e, 'not register in bot')
        if not user_in_service_bot:
            await service_bot.send_message(chat_id=self.sender_id,
                                           text=text_util.LINKER_TO_CLIENT)


class StickerSender(BaseSender):
    async def forward_data(self, data: types.Message):
        user_in_service_bot = False
        with service_bot.with_token(config.CLIENT_BOT_TOKEN):
            chat_id = self.sender_id

            text = "{}".format(self.prepare_to_send())
            try:
                await service_bot.send_message(chat_id=chat_id,
                                               text=text,
                                               reply_markup=self.get_answer_markup())
                await service_bot.send_sticker(chat_id=chat_id,
                                               sticker=data.sticker.file_id)
                user_in_service_bot = True
            except Exception as e:
                logging.warning(e, 'not register in bot')
        if not user_in_service_bot:
            await service_bot.send_message(chat_id=self.sender_id,
                                           text=text_util.LINKER_TO_CLIENT)


class PhotoSender(BaseSender):
    async def forward_data(self, data: types.Message):
        user_in_service_bot = False
        path = os.path.join(config.media_path, 'tmp_photo')
        photo = await data.photo[0].download(destination_file=path)
        with client_bot.with_token(config.CLIENT_BOT_TOKEN):
            chat_id = self.sender_id

            text = "{}".format(self.prepare_to_send())
            try:
                await service_bot.send_message(chat_id=chat_id,
                                               text=text,
                                               reply_markup=self.get_answer_markup())
                await service_bot.send_photo(chat_id=chat_id,
                                             photo=open(path, 'rb'))
                user_in_service_bot = True
            except Exception as e:
                logging.warning(e, 'not register in bot')
        if not user_in_service_bot:
            await service_bot.send_message(chat_id=self.sender_id,
                                           text=text_util.LINKER_TO_CLIENT)


class AnimationSender(BaseSender):
    async def forward_data(self, data: types.Message):
        user_in_service_bot = False
        path = os.path.join(config.media_path, 'animation.gif')
        photo = await data.animation.download(destination_file=path)
        with service_bot.with_token(config.CLIENT_BOT_TOKEN):
            chat_id = self.sender_id

            text = "{}".format(self.prepare_to_send())
            try:
                await service_bot.send_message(chat_id=chat_id,
                                               text=text,
                                               reply_markup=self.get_answer_markup())
                await service_bot.send_animation(chat_id=chat_id,
                                                 animation=open(path, 'rb'))
                user_in_service_bot = True
            except Exception as e:
                logging.warning(e, 'not register in bot')
        if not user_in_service_bot:
            await service_bot.send_message(chat_id=self.sender_id,
                                           text=text_util.LINKER_TO_CLIENT)


class VideoSender(BaseSender):
    async def forward_data(self, data):
        user_in_service_bot = False
        path = os.path.join(config.media_path, 'video.mp4')
        photo = await data.video.download(destination_file=path)
        with service_bot.with_token(config.CLIENT_BOT_TOKEN):
            chat_id = self.sender_id

            text = "{}".format(self.prepare_to_send())
            try:
                await service_bot.send_message(chat_id=chat_id,
                                               text=text,
                                               reply_markup=self.get_answer_markup())
                await service_bot.send_video(chat_id=chat_id,
                                             video=open(path, 'rb'))
                user_in_service_bot = True
            except Exception as e:
                logging.warning(e, 'not register in bot')
        if not user_in_service_bot:
            await service_bot.send_message(chat_id=self.sender_id,
                                           text=text_util.LINKER_TO_CLIENT)


class AudioSender(BaseSender):
    async def forward_data(self, data):
        user_in_service_bot = False
        path = os.path.join(config.media_path, 'audio.mp3')
        photo = await data.audio.download(destination_file=path)
        with service_bot.with_token(config.CLIENT_BOT_TOKEN):
            chat_id = self.sender_id

            text = "{}".format(self.prepare_to_send())
            try:
                await service_bot.send_message(chat_id=chat_id,
                                               text=text,
                                               reply_markup=self.get_answer_markup())
                await service_bot.send_audio(chat_id=chat_id,
                                             audio=open(path, 'rb'))
                user_in_service_bot = True
            except Exception as e:
                logging.warning(e, 'not register in bot')
        if not user_in_service_bot:
            await service_bot.send_message(chat_id=self.sender_id,
                                           text=text_util.LINKER_TO_CLIENT)


class VoiceSender(BaseSender):
    async def forward_data(self, data):
        user_in_service_bot = False
        path = os.path.join(config.media_path, 'voice.ogg')
        photo = await data.voice.download(destination_file=path)
        with service_bot.with_token(config.CLIENT_BOT_TOKEN):
            chat_id = self.sender_id
            text = "{}".format(self.prepare_to_send())
            try:
                await service_bot.send_message(chat_id=chat_id,
                                               text=text,
                                               reply_markup=self.get_answer_markup())
                await service_bot.send_voice(chat_id=chat_id,
                                             voice=open(path, 'rb'))
                user_in_service_bot = True
            except Exception as e:
                logging.warning(e, 'not register in bot')
        if not user_in_service_bot:
            await service_bot.send_message(chat_id=self.sender_id,
                                           text=text_util.LINKER_TO_CLIENT)
