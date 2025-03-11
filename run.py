import asyncio
import logging
from aiogram import Bot, Dispatcher

from config import TOKEN
from app.user import user


async def main():
    bot = Bot(token=TOKEN)
    dp = Dispatcher()
    dp.include_router(user)
    await dp.start_polling(bot)


if __name__ == '__main__':
    try:
        logging.basicConfig(level=logging.INFO)
        asyncio.run(main())
    except KeyboardInterrupt:
        logging.info("Bot stopped")