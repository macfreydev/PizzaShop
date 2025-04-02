from aiogram.fsm.state import State, StatesGroup


class AddCart(StatesGroup):
    pizza_id = State()
    size = State()
    quantity = State()
