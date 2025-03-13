from aiogram import Router, F
from aiogram.types import Message
from aiogram.filters import CommandStart
from app.database.requests import set_user

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
    )

@user.message(F.photo)
async def photo(message: Message):
    await message.answer(message.photo[-1].file_id)
