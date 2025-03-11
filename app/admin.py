from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.filters import Command, CommandStart

admin = Router()

@admin.message(CommandStart())
async def start(message: Message):
    await message.answer(
        f"""🍕 Welcome {message.from_user.first_name} to the admin panel""")