from aiogram import Router
from aiogram.filters import CommandStart
from aiogram.fsm.context import FSMContext
from aiogram.types import Message

from app.logger import setup_logger
from app.messages import START_TEXT
from app.services.navigation.ui import show_main_menu

router = Router()
logger = setup_logger(__name__)


@router.message(CommandStart())
async def cmd_start(
    message: Message,
    state: FSMContext,
    user_id: int,
) -> None:
    await message.answer(START_TEXT)
    await show_main_menu(
        message=message,
        state=state,
        user_id=user_id,
    )

    logger.info(
        'Start command handled',
        extra={'user_id': user_id},
    )
