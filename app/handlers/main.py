from aiogram import F, Router
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery

from app.database.repositories.users import get_user_by_telegram_id
from app.logger import setup_logger
from app.services.navigation.ui import show_main_menu


router = Router()
logger = setup_logger(__name__)


@router.callback_query(F.data == 'main')
async def main_page(
    callback: CallbackQuery,
    state: FSMContext,
) -> None:
    user = await get_user_by_telegram_id(callback.from_user.id)
    user_id = user.user_id

    await show_main_menu(
        message=callback.message,
        state=state,
        user_id=user_id,
    )

    await callback.answer()

    logger.info(
        'Main menu opened',
        extra={'user_id': user_id},
    )