import configparser
import os
import re
from pathlib import Path

from icecream import ic

base_dir = Path(__file__).resolve().parent
media_path = Path(__file__).resolve().parent.parent.joinpath('media')
config = configparser.ConfigParser()
print(base_dir)
config.read(os.path.join(base_dir, "config.ini"))


def database_link():
    pre_database_url = os.environ.get('DATABASE_URL') or config['DataBase']['url']
    if pre_database_url is None:
        return None
    print('database: ', pre_database_url)
    arr = re.split(pattern=r'[:|@|/]', string=pre_database_url)
    while '' in arr:
        arr.remove('')

    name = arr[5]
    print(name)
    print('info from arr ', len(arr))
    user = arr[1]
    password = arr[2]
    host_db = arr[3]
    port = arr[4]
    db_path = 'postgresql+psycopg2://{}:{}@{}/{}'.format(user, password, host_db, name)
    return db_path


BOT_TOKEN = os.environ.get('bot_token') or config['Bot']['bot_token']
PORT = os.environ.get('port') or config['Server']['port']
ALCHEMY_DB_PATH = database_link()
ic(ALCHEMY_DB_PATH)
CLIENT_BOT_LINK = os.environ.get('client_bot_link') or config['Bot']['client_bot_link']
CLIENT_BOT_TOKEN = os.environ.get('client_bot_token') or config['Bot']['client_bot_token']
# region commands
EXIT_FROM_CHAT = 'Выйти из чата'
SHOW_EVENT_IN_CHAT = 'Посмотреть событие'
EVENT_ANSWER = 'Ответить'

# Sure check

# endregion
# validations
date_format = '%Y-%m-%d'
date_format_human = 'Год-месяц-день'

# callback data markers
ADD_EVENTS_PAGINATOR = 'add'
DELETE_EVENT = 'delete'
CONNECT_TO_CHAT = 'connect'

SHOW_EVENT_MARKER = 'show_event'