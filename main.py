import asyncio

from aiogram import Bot, Dispatcher

from app.config import BOT_TOKEN
from app.handlers import router
from app.logger import setup_logger
from app.middlewares import UserMiddleware

logger = setup_logger(__name__)


def _create_dispatcher() -> Dispatcher:
    dispatcher = Dispatcher()
    dispatcher.update.outer_middleware(UserMiddleware())
    dispatcher.include_router(router)
    return dispatcher


async def run_bot() -> None:
    logger.info('Bot startup started')

    dispatcher = _create_dispatcher()

    async with Bot(token=BOT_TOKEN) as bot:
        logger.info('Starting polling')
        await dispatcher.start_polling(bot)


def main() -> None:
    try:
        asyncio.run(run_bot())
    except KeyboardInterrupt:
        logger.info('Bot stopped manually')
    except Exception:
        logger.exception('Bot stopped with an unexpected error')
        raise
    finally:
        logger.info('Bot shutdown complete')


if __name__ == '__main__':
    main()
