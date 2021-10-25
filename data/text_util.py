from data import config

# event creating
LINKER_TO_CLIENT = f'Для того, чтобы посмотреть событие перейдите в \n{config.CLIENT_BOT_LINK}'

# chat features
EVENT_DELETED = 'Событие удалено'
LEFT_CHAT = 'Вы вышли из чата'

# chat

ENTER_IN_CHAT = 'Вы вошли в чат "{}" с пользователем {}'
"""1{} - event_title 2{} - user_fullname(sender)"""
# service bot

NOTIFICATION = 'Сообщение "{}"\n{}: '
""" 1{} event title 2{} user_fullname(sender)"""
