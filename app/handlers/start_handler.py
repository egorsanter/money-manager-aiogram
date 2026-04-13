from aiogram import Router
from aiogram.types import Message
from aiogram.filters import CommandStart

from app.services.start_service import get_start_text
from app.logger import setup_logger


logger = setup_logger(__name__)
router = Router()

@router.message(CommandStart())
async def cmd_start(message: Message) -> None:
    await message.answer(get_start_text())

    logger.info(
        'Start command handled: user_id=%s',
        message.from_user.id
    )