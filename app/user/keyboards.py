from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder

from app.database.data import sizes
from app.database.requests import add_pizzas, get_all_pizzas, get_cart, get_pizza


def menu_kb():
    try:
        return InlineKeyboardMarkup(
            inline_keyboard=[
                [
                    InlineKeyboardButton(text="🍕 Catalog", callback_data="catalog"),
                    InlineKeyboardButton(text="🛒 Cart", callback_data="cart"),
                ],
                [
                    InlineKeyboardButton(text="🎉 Sales", callback_data="sales"),
                    InlineKeyboardButton(
                        text="🔍 Reviews", callback_data="all_reviews"
                    ),
                ],
                [InlineKeyboardButton(text="📞 Contact", callback_data="contact")],
            ]
        )
    except Exception as e:
        print(f"Error in get_menu_kb: {e}")
        return None  # Return None to signal failure


async def catalog_kb():
    try:
        all_pizzas = await get_all_pizzas()
        if not all_pizzas:
            try:
                await add_pizzas()
                all_pizzas = await get_all_pizzas()
            except Exception as e:
                print(f"Error adding pizzas: {e}")
                return None  # Return None if pizza addition fails

        keyboard = InlineKeyboardBuilder()
        for pizza in all_pizzas:
            keyboard.add(
                InlineKeyboardButton(text=pizza.name, callback_data=f"pizza_{pizza.id}")
            )
        keyboard.add(InlineKeyboardButton(text="🏠Menu", callback_data="menu"))
        return keyboard.adjust(3).as_markup()

    except Exception as e:
        print(f"Error fetching pizzas: {e}")
        return None  # Return None if fetching pizzas fails


async def pizza_kb(pizza_id):
    try:
        if not pizza_id:
            raise ValueError("Invalid pizza_id")  # Explicit error for invalid ID

        keyboard = InlineKeyboardBuilder()
        keyboard.add(
            InlineKeyboardButton(text="⬅️Back", callback_data="catalog"),
            InlineKeyboardButton(
                text="🔍Reviews", callback_data=f"about_pizza_{pizza_id}"
            ),
            InlineKeyboardButton(
                text="➕Add to Cart", callback_data=f"add_to_cart_{pizza_id}"
            ),
        )
        return keyboard.adjust(2).as_markup()

    except Exception as e:
        print(f"Error in pizza_kb: {e}")
        return None  # Return None to signal failure


async def add_to_cart_kb():
    try:
        keyboard = InlineKeyboardBuilder()
        keyboard.row(
            InlineKeyboardButton(text="Small", callback_data="size_1"),
            InlineKeyboardButton(text="Medium", callback_data="size_2"),
            InlineKeyboardButton(text="Large", callback_data="size_3"),
        )
        keyboard.row(InlineKeyboardButton(text="⬅️Back", callback_data="back_to_pizza"))

        return keyboard.adjust(3).as_markup()

    except Exception as e:
        print(f"Error in add_to_cart_kb: {e}")
        return None  # Return None to indicate failure


async def choose_quantity_kb():
    try:
        keyboard = InlineKeyboardBuilder()
        for i in range(1, 21):
            keyboard.add(
                InlineKeyboardButton(text=str(i), callback_data=f"quantity_{i}")
            )
        return keyboard.adjust(5).as_markup()

    except Exception as e:
        print(f"Error in choose_quantity_kb: {e}")
        return None  # Return None to indicate failure


async def proceed_to_pay():
    try:
        keyboard = InlineKeyboardBuilder()
        keyboard.add(
            InlineKeyboardButton(text="🍕Add pizza", callback_data="catalog"),
            InlineKeyboardButton(text="🛒Cart", callback_data="cart"),
            InlineKeyboardButton(text="💳Pay", callback_data="pay"),
        )
        return keyboard.adjust(3).as_markup()

    except Exception as e:
        print(f"Error in proceed_to_pay: {e}")
        return None  # Return None to indicate failure


async def cart_kb(user_id):
    try:
        cart = await get_cart(user_id)
        if not cart:
            return None  # Return None if the cart is empty

        keyboard = InlineKeyboardBuilder()

        for item in cart:
            try:
                pizza = await get_pizza(
                    item.pizza_id
                )  # Fixed potential issue (was using item.user_id)

                if not pizza:
                    continue  # Skip this item if pizza details aren't found

                # First row: Pizza name & size
                keyboard.row(
                    InlineKeyboardButton(
                        text=f"{pizza.name} | {sizes.get(item.size, 'Unknown Size')}",
                        callback_data=f"cart_{item.id}",
                    )
                )

                # Second row: +, quantity, - buttons
                keyboard.row(
                    InlineKeyboardButton(text="➕", callback_data=f"add_{item.id}"),
                    InlineKeyboardButton(
                        text=str(item.quantity), callback_data=f"quantity_{item.id}"
                    ),
                    InlineKeyboardButton(text="➖", callback_data=f"remove_{item.id}"),
                    InlineKeyboardButton(text="❌", callback_data=f"delete_{item.id}"),
                )

            except Exception as e:
                print(f"Error processing cart item {item.id}: {e}")
                continue  # Skip the problematic item but continue processing others

        # Add navigation buttons
        keyboard.row(
            InlineKeyboardButton(text="🏠 Menu", callback_data="menu"),
            InlineKeyboardButton(text="💳 Pay", callback_data="pay"),
            InlineKeyboardButton(text="🍕Add pizza", callback_data="catalog"),
        )

        return keyboard.as_markup()

    except Exception as e:
        print(f"Error in cart_kb: {e}")
        return None  # Return None to signal failure


async def reviews_kb(pizza_id: int):
    try:
        if not isinstance(pizza_id, int) or pizza_id <= 0:
            raise ValueError("Invalid pizza_id provided")

        keyboard = InlineKeyboardBuilder()
        keyboard.add(
            InlineKeyboardButton(
                text="📝 Leave a Review", callback_data=f"review_add_{pizza_id}"
            ),
            InlineKeyboardButton(
                text="🔙 Back to Pizzas", callback_data="back_to_pizza"
            ),
        )
        return keyboard.adjust(2).as_markup()

    except Exception as e:
        print(f"Error in reviews_kb: {e}")
        return None  # Return None to indicate failure


async def all_reviews_kb():
    try:
        keyboard = InlineKeyboardBuilder()
        keyboard.add(
            InlineKeyboardButton(text="🏠Go to Menu", callback_data="menu"),
            InlineKeyboardButton(text="🔙 Back to Catalog", callback_data="catalog"),
        )
        return keyboard.adjust(2).as_markup()

    except Exception as e:
        print(f"Error in all_reviews_kb: {e}")
        return None  # Return None to indicate failure


async def pay_kb():
    try:
        keyboard = InlineKeyboardBuilder()
        keyboard.add(
            InlineKeyboardButton(text="💳 Pay", callback_data="pay"),
            InlineKeyboardButton(text="🛒 Cart", callback_data="cart"),
        )
        return keyboard.as_markup()

    except Exception as e:
        print(f"Error in pay_kb: {e}")
        return None  # Return None to signal failure
