from aiogram import F, Router
from aiogram.filters import Command, Filter
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, Message
from app.admin.keyboards import (
    confirmation_kb,
    get_edit_pizza_kb,
    get_menu_keyboard,
    get_pizza_detail_kb,
    get_pizzas_kb,
    get_size_kb,
    get_yes_no_kb,
)
from app.admin.states import AdminStates, EditPizzaStates, PizzaStates
from app.database.requests import (
    add_admin,
    add_pizza,
    add_pizzas,
    delete_pizza,
    get_all_admins,
    get_pizza,
    update_pizza_property,
)

admin = Router()


class Admin(Filter):
    async def __call__(self, message: Message):
        ADMIN_IDS = await get_all_admins()
        return message.from_user.id in ADMIN_IDS


@admin.message(Admin(), Command("admin"))
async def start(message: Message):
    await add_pizzas()
    await message.answer(
        f"""🍕 Welcome {message.from_user.first_name} to the admin panel""",
        reply_markup=await get_menu_keyboard(),
    )


@admin.callback_query(F.data == "admin_catalog")
async def admin_catalog_handler(callback: CallbackQuery):
    try:

        await callback.message.edit_text(
            text="🍕 Pizza Catalog", reply_markup=await get_pizzas_kb()
        )
        await callback.answer()
    except Exception:
        await callback.message.delete()
        await callback.message.answer(
            text="🍕 Pizza Catalog", reply_markup=await get_pizzas_kb()
        )


@admin.callback_query(F.data == "add_admin")
async def add_admin_handler(callback: CallbackQuery, state: FSMContext):
    await state.set_state(AdminStates.waiting_for_admin_id)
    await callback.message.answer("Enter the user id to add as admin:")
    await callback.answer()


@admin.message(AdminStates.waiting_for_admin_id, F.text.isdigit())
async def add_admin_message(message: Message, state: FSMContext):
    await add_admin(int(message.text))
    await message.answer(
        "Admin added successfully!", reply_markup=await get_menu_keyboard()
    )  # beautify later on - it should be a pop up
    await state.clear()


@admin.message(AdminStates.waiting_for_admin_id)
async def invalid_admin_id(message: Message):
    await message.answer("Please enter a valid numeric user ID")


@admin.callback_query(F.data == "back_to_menu")
async def back_to_menu(callback: CallbackQuery):
    await callback.message.edit_text(
        "🍕 Admin Menu", reply_markup=await get_menu_keyboard()
    )
    await callback.answer()


@admin.callback_query(F.data.startswith("admin_pizza_"))
async def show_pizza_detail(callback: CallbackQuery):
    pizza_id = int(callback.data.split("_")[2])
    pizza = await get_pizza(pizza_id)

    if pizza:
        status_icon = "🟢🟢🟢 ON SALE" if pizza.onsale else "⭕️"
        price_display = f"${pizza.price:,.2f}"

        caption = (
            f"     🍕 <b>{pizza.name.upper()}</b>\n\n"
            f"📝 <b>Details</b>\n"
            f"• Size: {pizza.size}\n"
            f"• Price: {price_display}\n"
            f"• Status: {status_icon} \n\n"
            f"📋 <b>Description</b>\n"
            f"{pizza.about}\n\n"
        )

        await callback.message.delete()

        await callback.message.answer_photo(
            photo=pizza.image,
            caption=caption,
            reply_markup=await get_pizza_detail_kb(pizza_id),
            parse_mode="HTML",
        )
    else:
        await callback.answer("Pizza not found!", show_alert=True)

    await callback.answer("")


@admin.callback_query(F.data.startswith("delete_pizza_"))
async def delete_pizza_handler(callback: CallbackQuery):
    pizza_id = int(callback.data.split("_")[-1])
    await delete_pizza(pizza_id)
    await callback.message.answer(
        "🍕 Pizza Catalog", reply_markup=await get_pizzas_kb()
    )
    await callback.answer()


@admin.callback_query(F.data == "add_pizza")
async def add_pizza_handler(callback: CallbackQuery, state: FSMContext):
    await state.set_state(PizzaStates.waiting_for_pizza_name)
    await callback.message.answer("Enter the pizza name:")
    await callback.answer()


@admin.message(PizzaStates.waiting_for_pizza_name)
async def add_pizza_name(message: Message, state: FSMContext):
    await state.update_data(pizza_name=message.text)
    await state.set_state(PizzaStates.waiting_for_pizza_price)
    await message.answer("Enter the pizza price:")


@admin.message(PizzaStates.waiting_for_pizza_price)
async def add_pizza_price(message: Message, state: FSMContext):
    await state.update_data(pizza_price=message.text)
    await state.set_state(PizzaStates.waiting_for_pizza_description)
    await message.answer("Enter the pizza description:")


@admin.message(PizzaStates.waiting_for_pizza_description)
async def add_pizza_description(message: Message, state: FSMContext):
    await state.update_data(pizza_description=message.text)
    await state.set_state(PizzaStates.waiting_for_pizza_image)
    await message.answer("Enter the pizza image:")


@admin.message(PizzaStates.waiting_for_pizza_image)
async def add_pizza_image(message: Message, state: FSMContext):
    await state.update_data(pizza_image=message.photo[-1].file_id)
    await state.set_state(PizzaStates.waiting_for_pizza_sale)
    await message.answer("Is this pizza on sale?", reply_markup=get_yes_no_kb())


@admin.message(PizzaStates.waiting_for_pizza_sale)
async def add_pizza_sale(message: Message, state: FSMContext):
    await state.update_data(pizza_sale=message.text)
    await state.set_state(PizzaStates.waiting_for_pizza_size)
    await message.answer("Enter the pizza size:")


@admin.message(PizzaStates.waiting_for_pizza_size)
async def add_pizza_size(message: Message, state: FSMContext):
    await state.update_data(pizza_size=message.text)
    await state.set_state(PizzaStates.waiting_for_pizza_confirm)
    await message.answer("Confirm the pizza details:")


@admin.message(PizzaStates.waiting_for_pizza_confirm)
async def add_pizza_confirm(message: Message, state: FSMContext):
    data = await state.get_data()
    await add_pizza(data)
    await message.answer(
        "Pizza added successfully!", reply_markup=await get_pizzas_kb()
    )
    await state.clear()


@admin.callback_query(PizzaStates.waiting_for_pizza_sale, F.data == "sale_yes")
async def set_pizza_sale_yes(callback: CallbackQuery, state: FSMContext):
    await state.update_data(pizza_sale=True)
    await state.set_state(PizzaStates.waiting_for_pizza_size)
    await callback.message.answer("Select the pizza size:", reply_markup=get_size_kb())
    await callback.answer()


@admin.callback_query(PizzaStates.waiting_for_pizza_sale, F.data == "sale_no")
async def set_pizza_sale_no(callback: CallbackQuery, state: FSMContext):
    await state.update_data(pizza_sale=False)
    await state.set_state(PizzaStates.waiting_for_pizza_size)
    await callback.message.answer("Select the pizza size:", reply_markup=get_size_kb())
    await callback.answer()


@admin.callback_query(PizzaStates.waiting_for_pizza_size, F.data.startswith("size_"))
async def set_pizza_size(callback: CallbackQuery, state: FSMContext):
    size = callback.data.split("_")[1]  # Get S, M, or L
    await state.update_data(pizza_size=size)

    data = await state.get_data()

    summary = (
        f"📝 <b>Pizza Summary:</b>\n\n"
        f"• Name: {data['pizza_name']}\n"
        f"• Price: ${data['pizza_price']}\n"
        f"• Size: {data['pizza_size']}\n"
        f"• On Sale: {'Yes' if data['pizza_sale'] else 'No'}\n\n"
        f"<b>Description:</b>\n{data['pizza_description']}\n\n"
        f"Confirm to add this pizza? (yes/no)"
    )

    await callback.message.answer(
        summary, reply_markup=confirmation_kb(), parse_mode="HTML"
    )
    await state.set_state(PizzaStates.waiting_for_pizza_confirm)
    await callback.answer()


@admin.callback_query(PizzaStates.waiting_for_pizza_confirm, F.data == "confirm_pizza")
async def confirm_pizza_handler(callback: CallbackQuery, state: FSMContext):

    data = await state.get_data()

    from app.database.requests import add_new_pizza

    # Call function to add the pizza
    await add_new_pizza(
        name=data["pizza_name"],
        price=float(data["pizza_price"]),
        about=data["pizza_description"],
        image=data["pizza_image"],
        size=data["pizza_size"],
        onsale=data["pizza_sale"],
    )

    await state.clear()

    await callback.message.answer("✅ Pizza added successfully!")
    await callback.message.answer(
        "🍕 Pizza Catalog", reply_markup=await get_pizzas_kb()
    )
    await callback.answer()


@admin.callback_query(PizzaStates.waiting_for_pizza_confirm, F.data == "cancel_pizza")
async def cancel_pizza_handler(callback: CallbackQuery, state: FSMContext):
    await state.clear()

    await callback.message.answer("❌ Pizza creation cancelled.")
    await callback.message.answer(
        "🍕 Pizza Catalog", reply_markup=await get_pizzas_kb()
    )
    await callback.answer()


@admin.callback_query(F.data.startswith("edit_pizza_"))
async def edit_pizza_menu(callback: CallbackQuery):
    pizza_id = int(callback.data.split("_")[2])
    pizza = await get_pizza(pizza_id)

    if pizza:
        await callback.message.edit_caption(
            caption=f"Select which property to edit for {pizza.name}:",
            reply_markup=get_edit_pizza_kb(pizza_id),
        )
    await callback.answer()


# Handler for each property edit selection
@admin.callback_query(F.data.startswith("edit_"))
async def edit_property_handler(callback: CallbackQuery, state: FSMContext):

    parts = callback.data.split("_")
    property_name = parts[1]  # name, price, desc, etc.
    pizza_id = int(parts[2])

    await state.update_data(edit_pizza_id=pizza_id, edit_property=property_name)

    if property_name == "name":
        prompt = "Enter the new name for the pizza:"
    elif property_name == "price":
        prompt = "Enter the new price for the pizza:"
    elif property_name == "desc":
        prompt = "Enter the new description for the pizza:"
    elif property_name == "size":
        await callback.message.edit_caption(
            caption="Select the new size for the pizza:",
            reply_markup=get_size_kb(f"size_edit_{pizza_id}"),
        )
        await callback.answer()
        return
    elif property_name == "sale":
        # For sale status, show yes/no buttons
        await callback.message.edit_caption(
            caption="Should this pizza be on sale?",
            reply_markup=get_yes_no_kb(f"sale_edit_{pizza_id}"),
        )
        await callback.answer()
        return
    elif property_name == "image":
        prompt = "Send a new image for the pizza:"

    await state.set_state(EditPizzaStates.waiting_for_value)
    await callback.message.answer(prompt)
    await callback.answer()


# Handle text responses for edits
@admin.message(EditPizzaStates.waiting_for_value)
async def process_edit_value(message: Message, state: FSMContext):
    data = await state.get_data()
    pizza_id = data["edit_pizza_id"]
    property_name = data["edit_property"]

    if property_name == "name":
        await update_pizza_property(pizza_id, "name", message.text)
    elif property_name == "price":
        # Validate price
        if message.text.isdigit():
            await update_pizza_property(pizza_id, "price", int(message.text))
        else:
            await message.answer("Please enter a valid number for price.")
            return
    elif property_name == "desc":
        await update_pizza_property(pizza_id, "about", message.text)
    elif property_name == "image":
        if not message.photo:
            await message.answer("Please send an image.")
            return
        photo_id = message.photo[-1].file_id
        await update_pizza_property(pizza_id, "image", photo_id)

    await state.clear()
    pizza = await get_pizza(pizza_id)
    await message.answer("✅ Pizza updated successfully!")

    await show_updated_pizza(message, pizza)


async def show_updated_pizza(message: Message, pizza):
    """Show the updated pizza after editing"""
    if pizza:
        status_icon = "🟢" if pizza.onsale else "⭕️"
        price_display = f"${pizza.price:,.2f}"

        caption = (
            f"     🍕 <b>{pizza.name.upper()}</b>\n\n"
            f"📝 <b>Details</b>\n"
            f"• Size: {pizza.size}\n"
            f"• Price: {price_display}\n"
            f"• Status: {status_icon} \n\n"
            f"📋 <b>Description</b>\n"
            f"{pizza.about}\n\n"
        )

        await message.answer_photo(
            photo=pizza.image,
            caption=caption,
            reply_markup=await get_pizza_detail_kb(pizza.id),
            parse_mode="HTML",
        )
    else:
        await message.answer("Pizza not found!")
