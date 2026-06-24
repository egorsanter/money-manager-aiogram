from aiogram import F, Router
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery

from app.keyboards import accounts_keyboard
from app.logger import setup_logger
from app.messages import ACCOUNT_SELECTION_TEXT
from app.services.navigation.service import set_step
from app.services.navigation.steps import NavigationStep


router = Router()
logger = setup_logger(__name__)


@router.callback_query(F.data.startswith('category_'))
async def category_selected(
    callback: CallbackQuery,
    state: FSMContext,
    user_id: int,
) -> None:
    data = await state.get_data()
    category_id = int(callback.data.split("_")[1])
    message_id = data['message_id']

    await set_step(
        state=state,
        current_step=NavigationStep.ACCOUNT_SELECTION,
        user_id=user_id,
        category_id=category_id,
        message_id=message_id
    )

    await callback.message.edit_text(
        ACCOUNT_SELECTION_TEXT,
        reply_markup=await accounts_keyboard(user_id),
    )
    await callback.answer()

    logger.info(
        'Category selected',
        extra={
            'user_id': user_id,
            'category_id': category_id,
            'message_id': message_id,
        },
    )
