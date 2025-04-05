from aiogram import F, Router
from aiogram.filters import CommandStart
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, Message

import app.database.requests as request
import app.user.keyboards as keyboard
from app.database.data import sizes
from app.user.states import AddCart

user = Router()


@user.message(CommandStart())
async def start(message: Message):
    try:
        # Set the user in the database (or any data structure you're using)
        await request.set_user(message.from_user.id)

        welcome_message = (
            f"🍕 <b>Welcome {message.from_user.first_name}!</b>\n\n"
            f"Craving pizza? You’re in the right place! 😋\n\n"
            f"<i>Here’s what you can do:</i>\n\n"
            f"✅ <b>Browse the menu</b>\n"
            f"✅ <b>Customize your pizza</b>\n"
            f"✅ <b>Place an order</b> and track it in real-time\n\n"
            f"All of this and more, right here! Let’s get started! 🍕🔥"
        )

        await message.answer(
            welcome_message, parse_mode="HTML", reply_markup=keyboard.menu_kb()
        )

    except Exception as e:
        print(f"Error in start command: {e}")
        await message.answer("Something went wrong! Please try again later. 🙁")


@user.callback_query(F.data == "catalog")
async def catalog(callback: CallbackQuery):
    try:
        await callback.message.delete()
        await callback.answer()

        await callback.message.answer(
            text="🍕 Catalog", reply_markup=await keyboard.catalog_kb()
        )

    except Exception as e:
        print(f"Error in catalog callback: {e}")
        await callback.answer(
            "An error occurred while fetching the catalog. Please try again later."
        )


@user.callback_query(F.data.startswith("pizza_"))
async def pizza_info(callback: CallbackQuery, state: FSMContext):
    try:
        await callback.message.delete()
        await callback.answer()

        # Extract pizza ID from the callback data
        pizza_id = int(callback.data.split("_")[1])
        await state.update_data(pizza_id=pizza_id)

        pizza = await request.get_pizza(pizza_id)
        if pizza:
            on_sale = pizza.onsale
            sale_text = ""
            if on_sale:
                sale_text = "<b>🔥🔥 💸On Sale! 💸 🔥🔥</b>\n"

            caption = (
                f"<b>{pizza.name}</b>\n"
                f"{sale_text}"
                f"<i>{pizza.about}</i>\n"
                f"<b>Price:</b> <u>{pizza.price} RUB</u>\n\n"
                "<i>Click below to add this pizza to your cart!</i>"
            )

            await callback.message.answer_photo(
                photo=pizza.image,
                caption=caption,
                parse_mode="HTML",
                reply_markup=await keyboard.pizza_kb(pizza_id),
            )
        else:
            await callback.message.answer(
                text="Sorry, we couldn't find the pizza details."
            )

    except Exception as e:
        print(f"Error in pizza_info callback: {e}")
        await callback.message.answer(
            "An error occurred while fetching pizza details. Please try again later."
        )


@user.callback_query(F.data == "back_to_pizza")
async def back_to_pizza(callback: CallbackQuery, state: FSMContext):
    try:
        await state.clear()

        await callback.message.edit_text(
            text="🍕 Catalog", reply_markup=await keyboard.catalog_kb()
        )
    except Exception as e:
        print(f"Error in back_to_pizza callback: {e}")
        await callback.message.answer(
            "An error occurred while navigating back to the catalog. Please try again later."
        )


@user.callback_query(F.data.startswith("add_to_cart_"))
async def add_to_cart(callback: CallbackQuery, state: FSMContext):
    try:
        await callback.message.delete()
        await state.set_state(AddCart.size)

        await callback.message.answer(
            text="Choose the size of the pizza",
            reply_markup=await keyboard.add_to_cart_kb(),
        )

    except Exception as e:
        print(f"Error in add_to_cart callback: {e}")
        await callback.message.answer(
            "An error occurred while adding the pizza to your cart. Please try again later."
        )


@user.callback_query(AddCart.size)
async def size(callback: CallbackQuery, state: FSMContext):
    try:
        await state.update_data(size=callback.data.split("_")[1])
        await state.set_state(AddCart.quantity)

        await callback.message.edit_text(
            text="Enter the quantity of the pizza",
            reply_markup=await keyboard.choose_quantity_kb(),
        )

    except Exception as e:
        print(f"Error in size callback: {e}")
        await callback.message.answer(
            "An error occurred while selecting the size. Please try again later."
        )


@user.callback_query(AddCart.quantity)
async def quantity(callback: CallbackQuery, state: FSMContext):
    try:
        await state.update_data(quantity=callback.data.split("_")[1])

        data = await state.get_data()
        pizza_id = data["pizza_id"]
        size = int(data["size"])
        quantity = data["quantity"]

        if await request.add_to_cart(callback.from_user.id, pizza_id, size, quantity):
            # Clear the state and send a success message
            await state.clear()
            await callback.message.edit_text(
                f"""🍕 Pizza added to cart!\nSize: {sizes[size]}\nQuantity: {quantity}""",
                reply_markup=await keyboard.proceed_to_pay(),
            )
        else:
            await callback.message.answer(
                "Error adding to cart. Please try again later."
            )

        await callback.answer()

    except Exception as e:
        print(f"Error in quantity callback: {e}")
        await callback.message.answer(
            "An error occurred while adding the pizza to the cart. Please try again later."
        )
        await callback.answer()


@user.callback_query(F.data == "menu")
async def menu(callback: CallbackQuery):
    try:
        await callback.message.edit_text(
            text="🍕 Menu", reply_markup=keyboard.menu_kb()
        )
        await callback.answer()

    except Exception as e:
        print(f"Error in menu callback: {e}")
        await callback.message.answer(
            "An error occurred while loading the menu. Please try again later."
        )
        await callback.answer()


@user.callback_query(F.data == "cart")
async def cart(callback: CallbackQuery):
    try:
        cart = await request.check_cart(callback.from_user.id)

        if not cart:
            # If the cart is empty, notify the user and show the menu
            await callback.answer("🛒 Cart is empty")
            await callback.message.edit_text(
                text="🍕 Cart is empty, Add something", reply_markup=keyboard.menu_kb()
            )
        else:
            # If the cart has items, show the cart with items
            await callback.message.edit_text(
                text="🛒 Cart",
                reply_markup=await keyboard.cart_kb(callback.from_user.id),
            )

        await callback.answer()

    except Exception as e:
        print(f"Error in cart callback: {e}")
        await callback.message.answer(
            "An error occurred while accessing your cart. Please try again later."
        )
        await callback.answer()


@user.callback_query(F.data.startswith("remove_"))
async def remove_item(callback: CallbackQuery):
    try:
        cart_id = int(callback.data.split("_")[1])
        await request.remove_quantity(cart_id)
        await callback.message.edit_text(
            text="🛒 Cart", reply_markup=await keyboard.cart_kb(callback.from_user.id)
        )
        await callback.answer("Item removed from cart")

    except Exception as e:
        print(f"Error in remove_item callback: {e}")
        await callback.message.answer("An error occurred. Please try again later.")

    await callback.answer()


@user.callback_query(F.data.startswith("add_"))
async def add_item(callback: CallbackQuery):
    try:
        cart_id = int(callback.data.split("_")[1])
        await request.add_quantity(cart_id)
        await callback.answer("Item added to cart")
        await callback.message.edit_text(
            text="🛒 Cart", reply_markup=await keyboard.cart_kb(callback.from_user.id)
        )

    except Exception as e:
        print(f"Error in add_item callback: {e}")
        await callback.message.answer("An error occurred. Please try again later.")

    await callback.answer()


@user.callback_query(F.data.startswith("delete_"))
async def delete_item(callback: CallbackQuery):
    try:
        cart_id = int(callback.data.split("_")[1])
        if await request.delete_cart_item(cart_id):
            await callback.answer("Item deleted")
            if not await request.check_cart(callback.from_user.id):
                await callback.message.edit_text(
                    text="🍕Cart is empty, Add something",
                    reply_markup=keyboard.menu_kb(),
                )
            else:
                await callback.message.edit_text(
                    text="🛒Cart",
                    reply_markup=await keyboard.cart_kb(callback.from_user.id),
                )
        else:
            await callback.message.answer("Error deleting item")

    except Exception as e:
        print(f"Error in delete_item callback: {e}")
        await callback.message.answer("An error occurred. Please try again later.")

    await callback.answer()


@user.callback_query(F.data == "pay")
async def pay(callback: CallbackQuery):
    try:
        await callback.message.edit_text(
            text="💳 Pay", reply_markup=await keyboard.pay_kb()
        )

    except Exception as e:
        print(f"Error in pay callback: {e}")
        await callback.message.answer("An error occurred. Please try again later.")

    await callback.answer()


@user.callback_query(F.data.startswith("about_pizza"))
async def reviews(callback: CallbackQuery):
    try:
        await callback.message.delete()
        pizza_id = int(callback.data.split("_")[2])

        reviews = await request.get_reviews(pizza_id)
        total_reviews = await request.count_reviews(pizza_id)

        average_rating = (
            round(sum([review.rating for review in reviews]) / total_reviews, 2)
            if total_reviews > 0
            else 0
        )
        pizza = await request.get_pizza(pizza_id)

        review_text = f"🍕 <b>{pizza.name}</b> - Customer Reviews:\n\n"
        review_text += f"🌟 <b>Average Rating:</b> {average_rating}/5\n"
        review_text += f"👥 <b>Total Reviewers:</b> {total_reviews}\n\n"

        if reviews:
            for review in reviews:
                user_name = review.user_name if review.user_name else "Anonymous"
                text = review.text if review.text else "No comment provided."
                review_text += f"⭐ <b>{user_name}</b> - Rating: {review.rating}/5\n"
                review_text += f"💬 {text}\n\n"

            review_text += "────────────────────\n"
            review_text += "Leave your review! 📝"
        else:
            review_text += """
                🍕 <b>No reviews yet for this pizza.</b>\n
                Be the first to leave a review and share your thoughts! 📝"""

        await callback.message.answer(
            text=review_text,
            parse_mode="HTML",
            reply_markup=await keyboard.reviews_kb(pizza_id),
        )

    except Exception as e:
        print(f"Error in reviews callback: {e}")
        await callback.message.answer(
            "An error occurred while fetching reviews. Please try again later."
        )

    await callback.answer()


@user.callback_query(F.data == "all_reviews")
async def all_reviews(callback: CallbackQuery):
    try:
        reviews = await request.get_all_reviews()

        if not reviews:
            await callback.message.answer("No reviews available yet.")
            return

        pizza_reviews = {}

        for review in reviews:
            pizza_id = review.pizza_id
            if pizza_id not in pizza_reviews:
                pizza = await request.get_pizza(pizza_id)
                pizza_reviews[pizza_id] = {
                    "name": pizza.name,
                    "ratings": [],
                    "comments": [],
                }

            pizza_reviews[pizza_id]["ratings"].append(review.rating)
            pizza_reviews[pizza_id]["comments"].append(
                f"⭐ <b>{review.user_name}</b> - {review.rating}/5\n💬 {review.text}"
            )

        review_text = "<b>📢 All Customer Reviews:</b>\n\n"

        for pizza_id, data in pizza_reviews.items():
            avg_rating = round(sum(data["ratings"]) / len(data["ratings"]), 2)
            total_reviews = len(data["ratings"])

            review_text += f"🍕 <b>{data['name']}</b>\n"
            review_text += f"🌟 <b>Average Rating:</b> {avg_rating}/5\n"
            review_text += f"👥 <b>Total Reviews:</b> {total_reviews}\n\n"

            for comment in data["comments"]:
                review_text += f"{comment}\n\n"

            review_text += "────────────────────\n\n"

        await callback.message.edit_text(
            text=review_text,
            parse_mode="HTML",
            reply_markup=await keyboard.all_reviews_kb(),
        )

    except Exception as e:
        print(f"Error in all_reviews callback: {e}")
        await callback.message.answer(
            "An error occurred while fetching all reviews. Please try again later."
        )

    await callback.answer()


@user.message(F.photo)
async def handle_photo(message: Message):
    await message.answer(message.photo[-1].file_id)
