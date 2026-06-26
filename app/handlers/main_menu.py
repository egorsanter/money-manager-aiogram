from aiogram import F, Router
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery

from app.logger import setup_logger
from app.services.navigation.ui import show_main_menu

router = Router()
logger = setup_logger(__name__)


@router.callback_query(F.data == 'main_menu')
async def main_menu_selected(
    callback: CallbackQuery,
    state: FSMContext,
    user_id: int,
) -> None:
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
