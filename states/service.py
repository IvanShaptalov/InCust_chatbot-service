from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher.filters.state import StatesGroup, State

storage = MemoryStorage()


class ServiceStates(StatesGroup):
    main_menu = State()
    in_chat = State()