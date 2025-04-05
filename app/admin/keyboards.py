import logging

from aiogram.types import InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder

from app.database.exceptions import DatabaseError
from app.database.requests import get_all_pizzas

logger = logging.getLogger(__name__)


async def get_menu_keyboard():
    kb = InlineKeyboardBuilder()
    kb.button(text="🍕 Pizza Catalog", callback_data="admin_catalog")
    kb.button(text="➕ Add Admin", callback_data="admin_add_admin")
    # Add other admin menu buttons
    kb.adjust(2)
    return kb.as_markup()


async def get_pizzas_kb():
    kb = InlineKeyboardBuilder()

    try:
        pizzas = await get_all_pizzas()

        for pizza in pizzas:
            kb.button(text=pizza.name, callback_data=f"admin_pizza_{pizza.id}")

        if pizzas:
            kb.adjust(2)
    except DatabaseError as e:
        logger.error(f"Error getting pizzas for keyboard: {e}")
        # Continue with the keyboard but without pizza buttons

    kb.row(InlineKeyboardButton(text="➕ Add Pizza", callback_data="admin_add_pizza"))
    kb.row(InlineKeyboardButton(text="⬅️ Back", callback_data="back_to_menu"))

    return kb.as_markup()


async def get_pizza_detail_kb(pizza_id: int):
    kb = InlineKeyboardBuilder()
    kb.button(text="✏️ Edit", callback_data=f"edit_pizza_{pizza_id}")
    kb.button(text="🗑️ Delete", callback_data=f"delete_pizza_{pizza_id}")
    kb.button(text="⬅️ Back", callback_data="admin_catalog")
    kb.adjust(2, 1)
    return kb.as_markup()


def get_size_kb(callback_prefix="size"):
    """Get a keyboard with pizza size options"""
    kb = InlineKeyboardBuilder()

    # If this is for editing, use a different callback format
    if callback_prefix.startswith("size_edit_"):
        pizza_id = callback_prefix.split("_")[2]
        kb.button(text="Small", callback_data=f"size_edit_{pizza_id}_S")
        kb.button(text="Medium", callback_data=f"size_edit_{pizza_id}_M")
        kb.button(text="Large", callback_data=f"size_edit_{pizza_id}_L")
    else:
        kb.button(text="Small", callback_data="size_S")
        kb.button(text="Medium", callback_data="size_M")
        kb.button(text="Large", callback_data="size_L")

    kb.adjust(3)  # 3 buttons per row
    return kb.as_markup()


def get_yes_no_kb(callback_prefix="sale"):
    """Get a yes/no keyboard for sale status"""
    kb = InlineKeyboardBuilder()

    # If this is for editing, use a different callback format
    if callback_prefix.startswith("sale_edit_"):
        pizza_id = callback_prefix.split("_")[2]
        kb.button(text="Yes", callback_data=f"sale_yes_edit_{pizza_id}")
        kb.button(text="No", callback_data=f"sale_no_edit_{pizza_id}")
    else:
        kb.button(text="Yes", callback_data="sale_yes")
        kb.button(text="No", callback_data="sale_no")

    kb.adjust(2)  # 2 buttons per row
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
