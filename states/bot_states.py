from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.dispatcher.storage import FSMContext

class Creation(StatesGroup):
    get_cat_name = State()
    get_good_name = State()
