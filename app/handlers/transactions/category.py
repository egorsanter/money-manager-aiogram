from aiogram import F, Router
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery

from app.exceptions import InvalidStateDataError
from app.keyboards import accounts_keyboard, main_menu_button_keyboard
from app.logger import setup_logger
from app.messages import ACCOUNT_SELECTION_TEXT, INVALID_STATE_TEXT
from app.services.navigation.service import (
    get_required_state_data,
    set_navigation_step,
)
from app.services.navigation.steps import NavigationStep
from app.services.telegram import safe_edit_text

router = Router()
logger = setup_logger(__name__)


@router.callback_query(F.data.startswith('category_'))
async def category_selected(
    callback: CallbackQuery,
    state: FSMContext,
    user_id: int,
) -> None:
    try:
        data = await get_required_state_data(state, 'message_id')
    except InvalidStateDataError as error:
        await state.clear()
        await safe_edit_text(
            callback.message,
            INVALID_STATE_TEXT,
            reply_markup=main_menu_button_keyboard(),
        )
        await callback.answer()

        logger.warning(
            'Category selected with invalid state data',
            extra={
                'user_id': user_id,
                'error': str(error),
            },
        )

        return

    category_id = int(callback.data.split("_")[1])
    message_id = data['message_id']

    await set_navigation_step(
        state=state,
        current_step=NavigationStep.ACCOUNT_SELECTION,
        user_id=user_id,
        category_id=category_id,
        message_id=message_id,
    )

    await safe_edit_text(
        callback.message,
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
