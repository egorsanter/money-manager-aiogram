from aiogram import F, Router
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery

from app.exceptions import InvalidStateDataError
from app.keyboards import description_keyboard, main_menu_button_keyboard
from app.logger import setup_logger
from app.messages import DESCRIPTION_INPUT_TEXT, INVALID_STATE_TEXT
from app.services.navigation.service import (
    get_required_state_data,
    set_navigation_step,
)
from app.services.navigation.steps import NavigationStep
from app.services.telegram import safe_edit_text
from app.states import AddDescription

router = Router()
logger = setup_logger(__name__)


@router.callback_query(F.data.startswith('account_'))
async def account_selected(
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
            'Account selected with invalid state data',
            extra={
                'user_id': user_id,
                'error': str(error),
            },
        )

        return

    account_id = int(callback.data.split('_')[1])
    message_id = data['message_id']

    await set_navigation_step(
        state=state,
        current_step=NavigationStep.DESCRIPTION_INPUT,
        user_id=user_id,
        account_id=account_id,
        message_id=message_id,
    )
    await state.set_state(AddDescription.description_input)

    await safe_edit_text(
        callback.message,
        DESCRIPTION_INPUT_TEXT,
        reply_markup=description_keyboard(),
    )
    await callback.answer()

    logger.info(
        'Account selected',
        extra={
            'user_id': user_id,
            'account_id': account_id,
            'message_id': message_id,
        },
    )
