from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.filters import CommandStart, Filter
from app.admin.keyboards import get_menu_keyboard, get_pizzas_kb, get_pizza_detail_kb
from app.database.requests import add_pizza, get_pizza


admin = Router()

ADMIN_IDS = [5129759335]  # List of admin Telegram IDs change to db later on


class Admin(Filter):
    async def __call__(self, message: Message):
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
async def add_admin_handler(callback: CallbackQuery):
    pass # to be implemented 


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
        # Create a decorative border
        border_top = "┏━━━━━━━━━━━━━━━━━━━━┓"
        border_bottom = "┗━━━━━━━━━━━━━━━━━━━━┛"
        
        status_icon = "🟢🟢🟢 ON SALE" if pizza.onsale else "⭕️"
        price_display = f"${pizza.price:,.2f}"
        
        caption = (
            f"{border_top}\n"
            f"     🍕 <b>{pizza.name.upper()}</b>\n"
            f"━━━━━━━━━━━━━━━━━━━━\n\n"
            f"📝 <b>Details</b>\n"
            f"• Size: {pizza.size}\n"
            f"• Price: {price_display}\n"
            f"• Status: {status_icon} \n\n"
            f"📋 <b>Description</b>\n"
            f"{pizza.about}\n\n"
            f"{border_bottom}"
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

