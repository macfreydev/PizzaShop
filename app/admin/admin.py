from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.filters import Command, Filter, CommandStart
from app.admin.keyboards import get_menu_keyboard, get_pizzas_kb, get_pizza_detail_kb
from app.database.requests import add_pizza, get_pizza, add_admin, get_all_admins
from app.admin.states import AdminStates
from aiogram.fsm.context import FSMContext

admin = Router()


class Admin(Filter):
    async def __call__(self, message: Message):
        ADMIN_IDS = await get_all_admins()
        return message.from_user.id in ADMIN_IDS


@admin.message(Admin(), CommandStart())
async def start(message: Message):
    await add_pizza()
    await message.answer(
        f"""🍕 Welcome {message.from_user.first_name} to the admin panel""",
          reply_markup= await get_menu_keyboard()
        )


@admin.callback_query(F.data == "catalog")
async def admin_catalog_handler(callback: CallbackQuery):
    await callback.message.edit_text(
        text="🍕 Pizza Catalog",
        reply_markup=await get_pizzas_kb()
    )
    await callback.answer()

@admin.callback_query(F.data == "add_admin")
async def add_admin_handler(callback: CallbackQuery, state: FSMContext):
    await state.set_state(AdminStates.waiting_for_admin_id)
    await callback.message.answer("Enter the user id to add as admin:")
    await callback.answer()

@admin.message(AdminStates.waiting_for_admin_id, F.text.isdigit())
async def add_admin_message(message: Message, state: FSMContext):
    await add_admin(int(message.text))
    await message.answer("Admin added successfully!")
    await state.clear()

@admin.message(AdminStates.waiting_for_admin_id)
async def invalid_admin_id(message: Message):
    await message.answer("Please enter a valid numeric user ID")

@admin.callback_query(F.data == 'back_to_menu')
async def back_to_menu(callback: CallbackQuery):
    await callback.message.edit_text(
        "🍕 Admin Menu",
          reply_markup= await get_menu_keyboard()
        )
    await callback.answer()

@admin.callback_query(F.data.startswith("pizza_"))
async def show_pizza_detail(callback: CallbackQuery):
    pizza_id = int(callback.data.split("_")[1])
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
            parse_mode="HTML"
        )
    else:
        await callback.answer("Pizza not found!", show_alert=True)
    
    await callback.answer()

