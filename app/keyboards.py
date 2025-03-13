from aiogram.types import (ReplyKeyboardMarkup, KeyboardButton,
                           InlineKeyboardMarkup, InlineKeyboardButton)
from aiogram.utils.keyboard import ReplyKeyboardBuilder, InlineKeyboardBuilder
from app.database.requests import get_all_pizzas,add_pizzas, get_pizza


menu = InlineKeyboardMarkup(inline_keyboard=[
    [
        InlineKeyboardButton(text="🍕Catalog", callback_data="catalog")
    ],
    [
        InlineKeyboardButton(text="🛒Cart", callback_data="cart")
    ],
    [
        InlineKeyboardButton(text="🎉Sales", callback_data="sales")
    ], 
    [
        InlineKeyboardButton(text="📞Contact", callback_data="contact")
    ], 
    [
        InlineKeyboardButton(text="🔍Reviews", callback_data="reviews")
    ]
], row_width=2)


async def catalog_kb():
    all_pizzas = await get_all_pizzas()
    if not all_pizzas:
        await add_pizzas()
        all_pizzas = await get_all_pizzas()

    keyboard = InlineKeyboardBuilder()
    for pizza in all_pizzas:
        keyboard.add(InlineKeyboardButton(text=pizza.name, 
                                          callback_data=f'pizza_{pizza.id}'))
    return keyboard.adjust(3).as_markup()

async def pizza_kb(pizza_id):
    if not pizza_id:
         return None
    
    keyboard = InlineKeyboardBuilder()
    keyboard.add(InlineKeyboardButton(text="⬅️Back",callback_data="catalog"),
                 InlineKeyboardButton(text="➕Add to Cart", callback_data=f"add_{pizza_id}"))
    return keyboard.adjust(2).as_markup()
