import asyncio
import logging
from aiogram import Bot, Dispatcher

from config import TOKEN
from app.user import user
from app.admin.admin import admin
from app.database.db import init_db

async def main():
    await init_db()
    bot = Bot(token=TOKEN)
    dp = Dispatcher()
    dp.include_router(admin)
    dp.include_router(user)
    await dp.start_polling(bot)


if __name__ == '__main__':
    try:
        logging.basicConfig(level=logging.INFO)
        asyncio.run(main())
    except KeyboardInterrupt:
        logging.info("Bot stopped")