import asyncio

from aiogram import Bot, Dispatcher

from app.config import BOT_TOKEN
from app.logger import setup_logger
from app.handlers import router


logger = setup_logger(__name__)


async def main() -> None:
    logger.info('Starting bot...')
    dp = Dispatcher()

    dp.include_router(router)

    async with Bot(token=BOT_TOKEN) as bot:
        logger.info('Starting polling...')
        await dp.start_polling(bot)

        logger.info('Polling stopped')


if __name__ == '__main__':
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        logger.info('Bot stopped manually')
    finally:
        logger.info('Bot shutdown complete')