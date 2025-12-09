import asyncio
import logging

from aiogram import Bot
from bot.config import TOKEN

from bot import setup_dp

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


async def main():
    logger.info("🚀 Бот запускается...")
    bot = Bot(token=TOKEN)
    dp = setup_dp()

    try:
        await dp.start_polling(bot)
    finally:
        await bot.session.close()
        logger.info("🛑 Бот остановлен")


if __name__ == "__main__":
    asyncio.run(main())
