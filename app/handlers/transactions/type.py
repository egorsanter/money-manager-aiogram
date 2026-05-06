from aiogram import F, Router
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery

from app.database.repositories.users import get_user_by_telegram_id
from app.keyboards import back_keyboard
from app.logger import setup_logger
from app.messages import AMOUNT_INPUT_TEXT
from app.services.navigation.service import set_step
from app.services.navigation.steps import NavigationStep
from app.states import AddTransaction


router = Router()
logger = setup_logger(__name__)


@router.callback_query(F.data.in_({'expense', 'income'}))
async def transaction_selected(
    callback: CallbackQuery,
    state: FSMContext,
) -> None:
    user = await get_user_by_telegram_id(callback.from_user.id)
    user_id = user.user_id

    message_id = callback.message.message_id

    await set_step(
        state,
        current_step=NavigationStep.AMOUNT_INPUT,
        user_id=user_id,
        transaction_type=callback.data,
        message_id=message_id,
    )
    await state.set_state(AddTransaction.amount_input)

    await callback.message.edit_text(
        AMOUNT_INPUT_TEXT,
        reply_markup=await back_keyboard(),
    )
    await callback.answer()

    logger.info(
        'Transaction type selected',
        extra={
            'user_id': user_id,
            'transaction_type': callback.data,
            'message_id': message_id,
        },
    )