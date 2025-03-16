from aiogram.types import (ReplyKeyboardMarkup, KeyboardButton,
                           InlineKeyboardMarkup, InlineKeyboardButton)
from aiogram.utils.keyboard import ReplyKeyboardBuilder, InlineKeyboardBuilder
from app.database.requests import get_all_pizzas,add_pizzas, get_pizza, add_to_cart, get_cart, delete_cart_item


menu = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text="🍕 Catalog", callback_data="catalog"),
            InlineKeyboardButton(text="🛒 Cart", callback_data="cart")
        ],
        [
            InlineKeyboardButton(text="🎉 Sales", callback_data="sales"),
            InlineKeyboardButton(text="🔍 Reviews", callback_data="reviews")
        ],
        [
            InlineKeyboardButton(text="📞 Contact", callback_data="contact")
        ]
    ],
    row_width=2
)


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
                 InlineKeyboardButton(text="🔍Reviews", callback_data="reviews"),
                 InlineKeyboardButton(text="➕Add to Cart", callback_data=f"add_to_cart_{pizza_id}"))
    return keyboard.adjust(2).as_markup()

async def add_to_cart_kb():
    keyboard = InlineKeyboardBuilder()
    keyboard.add(InlineKeyboardButton(text="Small", callback_data="size_1"),
                 InlineKeyboardButton(text="Medium", callback_data="size_2"),
                 InlineKeyboardButton(text="Large", callback_data="size_3"))

    return keyboard.adjust(3).as_markup()   

async def choose_quantity_kb():
    keyboard = InlineKeyboardBuilder()
    for i in range(1, 21):
        keyboard.add(InlineKeyboardButton(text=str(i), callback_data=f"quantity_{i}"))
    return keyboard.adjust(5).as_markup()

async def proceed_to_pay():
    keyboard = InlineKeyboardBuilder()
    keyboard.add(InlineKeyboardButton(text="🏠Menu", callback_data="menu"),
                InlineKeyboardButton(text="🛒Cart", callback_data="cart"),
                InlineKeyboardButton(text="💳Pay", callback_data="pay")
                 )
    return keyboard.adjust(3).as_markup()

async def cart_kb(user_id):
    cart = await get_cart(user_id)  
    if not cart:
        return None 
    keyboard = InlineKeyboardBuilder()
    for item in cart:
        pizza = await get_pizza(item.pizza_id)
        keyboard.add(
                InlineKeyboardButton(
                    text=f"{pizza.name} {item.size}",
                    callback_data=f"cart_{item.id}"
                ),
                InlineKeyboardButton(
                    text="➕", 
                    callback_data=f"add_{item.id}"
                ),
                InlineKeyboardButton(
                    text=str(item.quantity),
                    callback_data=f"quantity_{item.id}"
                ),
                InlineKeyboardButton(
                    text="➖", 
                    callback_data=f"remove_{item.id}"
                )
            )
        keyboard.row()
        keyboard.add(InlineKeyboardButton(text="🏠Menu", callback_data="menu"),
                 InlineKeyboardButton(text="💳Pay", callback_data="pay")).adjust(2)
        
    return keyboard.as_markup()

async def pay_kb():
    keyboard = InlineKeyboardBuilder()  
    keyboard.add(InlineKeyboardButton(text="💳Pay", callback_data="pay"),
                 InlineKeyboardButton(text="🛒Cart", callback_data="cart"))
    return keyboard.as_markup()