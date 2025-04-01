from aiogram.types import InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder

from app.database.requests import get_all_pizzas


async def get_menu_keyboard():
    menu_kb = InlineKeyboardBuilder()

    menu_kb.button(text="🏷️ Catalog", callback_data="admin_catalog")
    menu_kb.button(text="➕ Add Admin", callback_data="add_admin")

    return menu_kb.as_markup()


async def get_pizzas_kb():
    kb = InlineKeyboardBuilder()

    pizzas = await get_all_pizzas()

    for pizza in pizzas:
        kb.button(text=pizza.name, callback_data=f"pizza_{pizza.id}")

    if pizzas:
        kb.adjust(2)

    kb.row(InlineKeyboardButton(text=" Add Pizza", callback_data="add_pizza"))
    kb.row(InlineKeyboardButton(text="⬅️ Back", callback_data="back_to_menu"))

    return kb.as_markup()


async def get_pizza_detail_kb(pizza_id: int):
    kb = InlineKeyboardBuilder()

    kb.button(text="✏️ Edit", callback_data=f"edit_pizza_{pizza_id}")
    kb.button(text="❌ Delete", callback_data=f"delete_pizza_{pizza_id}")
    kb.button(text="⬅️ Back", callback_data="catalog")

    kb.adjust(3)

    return kb.as_markup()


def get_yes_no_kb():
    kb = InlineKeyboardBuilder()
    kb.button(text="✅ Yes", callback_data="sale_yes")
    kb.button(text="❌ No", callback_data="sale_no")
    kb.adjust(2)
    return kb.as_markup()


def get_size_kb():
    kb = InlineKeyboardBuilder()
    kb.button(text="S - Small", callback_data="size_S")
    kb.button(text="M - Medium", callback_data="size_M")
    kb.button(text="L - Large", callback_data="size_L")
    kb.adjust(3)
    return kb.as_markup()


def confirmation_kb():
    kb = InlineKeyboardBuilder()
    kb.button(text="✅ Confirm", callback_data="confirm_pizza")
    kb.button(text="❌ Cancel", callback_data="cancel_pizza")
    kb.adjust(2)
    return kb.as_markup()


def get_edit_pizza_kb(pizza_id: int):
    kb = InlineKeyboardBuilder()

    kb.button(text="📝 Name", callback_data=f"edit_name_{pizza_id}")
    kb.button(text="💰 Price", callback_data=f"edit_price_{pizza_id}")
    kb.button(text="📋 Description", callback_data=f"edit_desc_{pizza_id}")
    kb.button(text="📏 Size", callback_data=f"edit_size_{pizza_id}")
    kb.button(text="🏷️ Sale Status", callback_data=f"edit_sale_{pizza_id}")
    kb.button(text="🖼️ Image", callback_data=f"edit_image_{pizza_id}")
    kb.button(text="⬅️ Back", callback_data=f"pizza_{pizza_id}")

    kb.adjust(2)

    return kb.as_markup()
