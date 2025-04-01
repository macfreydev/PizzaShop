from aiogram.fsm.state import State, StatesGroup


class AdminStates(StatesGroup):
    waiting_for_admin_id = State()


class PizzaStates(StatesGroup):
    waiting_for_pizza_name = State()
    waiting_for_pizza_price = State()
    waiting_for_pizza_description = State()
    waiting_for_pizza_image = State()
    waiting_for_pizza_sale = State()
    waiting_for_pizza_size = State()
    waiting_for_pizza_confirm = State()


class EditPizzaStates(StatesGroup):
    waiting_for_value = State()
