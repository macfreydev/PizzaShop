from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup

class AddCart(StatesGroup):
   pizza_id = State()
   size = State()
   quantity = State() #Should be added later on or not