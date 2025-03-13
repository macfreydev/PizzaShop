from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.filters import CommandStart
from app.database.requests import set_user
import app.keyboards as kb
import app.database.requests as db


user = Router()

@user.message(CommandStart())
async def start(message: Message):
    await set_user(message.from_user.id) # register new user in db - add try catch later on for all db requests
    await message.answer(
        f"""🍕 Welcome {message.from_user.first_name}!
Craving pizza? You’re in the right place!  
✅ Browse the menu  
✅ Customize your pizza  
✅ Place an order and track it in real-time  
All right here. Let's get started! 🍕🔥"""
,reply_markup=kb.menu)
    
@user.callback_query(F.data == "catalog")
async def catalog(callback: CallbackQuery):
    await callback.message.delete()
    await callback.answer()
    await callback.message.answer(
        text="🍕Catalog",
        reply_markup= await kb.catalog_kb() 
        )



@user.callback_query(F.data.startswith("pizza_"))
async def pizza_info(callback: CallbackQuery):
    await callback.message.delete()
    await callback.answer()
    pizza_id = int(callback.data.split("_")[1])
    pizza = await db.get_pizza(pizza_id)
    await callback.message.answer_photo(
        photo=pizza.image,
        caption=f"{pizza.name}\n{pizza.about}\n{pizza.price} RUB",
        parse_mode='HTML',
        reply_markup= await kb.pizza_kb(pizza_id)
        )

@user.message(F.photo)
async def handle_photo(message: Message):
    await message.answer(message.photo[-1].file_id)