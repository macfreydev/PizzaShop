import asyncio
from aiogram import Bot, Dispatcher, types

from config import TOKEN

from app.user import user


async def main():
    bot = Bot(token=TOKEN)
    dp = Dispatcher()
    dp.include_router(user)
    await dp.start_polling(bot)

if __name__ == '__main__':
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("Bot stopped")