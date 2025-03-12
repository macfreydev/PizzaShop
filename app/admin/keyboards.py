from aiogram.utils.keyboard import InlineKeyboardBuilder
from app.database.requests import get_all_pizzas, get_pizza


async def get_menu_keyboard():
    menu_kb = InlineKeyboardBuilder()

    menu_kb.button(text="🏷️ Catalog", callback_data="catalog")
    menu_kb.button(text="➕ Add Admin", callback_data="add_admin")

    return menu_kb.as_markup()


async def get_pizzas_kb():
    kb = InlineKeyboardBuilder()
    
    # Get pizzas from database
    pizzas = await get_all_pizzas()
    
    for pizza in pizzas:
        kb.button(text=pizza.name, callback_data=f"pizza_{pizza.id}")
    
    kb.button(text="➕ Add Pizza", callback_data="add_pizza")
    kb.button(text="⬅️ Back", callback_data="back_to_menu")
    
    kb.adjust(2, 2) 
    
    return kb.as_markup()


async def get_pizza_detail_kb(pizza_id: int):
    kb = InlineKeyboardBuilder()
    
    # Add action buttons
    kb.button(text="✏️ Edit", callback_data=f"edit_pizza_{pizza_id}")
    kb.button(text="❌ Delete", callback_data=f"delete_pizza_{pizza_id}")
    kb.button(text="⬅️ Back to Catalog", callback_data="catalog")
    
    # Arrange buttons in one row
    kb.adjust(3)
    
    return kb.as_markup()
