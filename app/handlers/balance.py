from aiogram import F, Router
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery

from app.keyboards import back_keyboard
from app.logger import setup_logger
from app.messages import Buttons
from app.services.balance import get_balance_text
from app.services.navigation.service import set_navigation_step
from app.services.navigation.steps import NavigationStep
from app.services.telegram import safe_edit_text

router = Router()
logger = setup_logger(__name__)


@router.callback_query(F.data == Buttons.BALANCE.callback_data)
async def balance_selected(
    callback: CallbackQuery,
    state: FSMContext,
    user_id: int,
) -> None:
    message_id = callback.message.message_id
    text = await get_balance_text(user_id)

    await set_navigation_step(
        state=state,
        current_step=NavigationStep.BALANCE,
        previous_step=NavigationStep.MAIN_MENU,
        user_id=user_id,
        message_id=message_id,
    )

    await safe_edit_text(
        callback.message,
        text,
        reply_markup=back_keyboard(),
    )

    await callback.answer()

    logger.info(
        'Balance opened',
        extra={
            'user_id': user_id,
            'message_id': message_id,
        },
    )
