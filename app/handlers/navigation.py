from aiogram import F, Router
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery

from app.exceptions import InvalidStateDataError
from app.keyboards import (
    accounts_keyboard,
    back_keyboard,
    categories_keyboard,
    main_menu_keyboard,
)
from app.logger import setup_logger
from app.messages import (
    ACCOUNT_SELECTION_TEXT,
    AMOUNT_INPUT_TEXT,
    CATEGORY_SELECTION_TEXT,
    DESCRIPTION_INPUT_TEXT,
    MAIN_MENU_TEXT,
    NAVIGATION_RESET_TEXT,
)
from app.services.navigation.service import (
    get_required_state_data,
    set_navigation_step,
)
from app.services.navigation.steps import NavigationStep
from app.services.telegram import safe_edit_text
from app.states import AddDescription, AddTransaction

router = Router()
logger = setup_logger(__name__)


async def _show_main_menu(
    callback: CallbackQuery,
    state: FSMContext,
    user_id: int,
    text: str = MAIN_MENU_TEXT,
) -> None:
    await state.clear()
    await set_navigation_step(
        state=state,
        current_step=NavigationStep.MAIN_MENU,
        previous_step=None,
        user_id=user_id,
    )
    await safe_edit_text(
        callback.message,
        text,
        reply_markup=main_menu_keyboard(),
    )


@router.callback_query(F.data == 'back')
async def back_selected(
    callback: CallbackQuery,
    state: FSMContext,
    user_id: int,
) -> None:
    message_id = callback.message.message_id
    data = await state.get_data()
    previous_step = data.get('previous_step')

    try:
        match previous_step:
            case NavigationStep.MAIN_MENU:
                await _show_main_menu(callback, state, user_id)

            case NavigationStep.AMOUNT_INPUT:
                data = await get_required_state_data(state, 'category_type')
                await set_navigation_step(
                    state=state,
                    current_step=NavigationStep.AMOUNT_INPUT,
                    previous_step=NavigationStep.MAIN_MENU,
                    user_id=user_id,
                    category_type=data['category_type'],
                    message_id=message_id,
                )
                await state.set_state(AddTransaction.amount_input)
                await safe_edit_text(
                    callback.message,
                    AMOUNT_INPUT_TEXT,
                    reply_markup=back_keyboard(),
                )

            case NavigationStep.CATEGORY_SELECTION:
                data = await get_required_state_data(
                    state,
                    'category_type',
                    'amount',
                )
                await set_navigation_step(
                    state=state,
                    current_step=NavigationStep.CATEGORY_SELECTION,
                    previous_step=NavigationStep.AMOUNT_INPUT,
                    user_id=user_id,
                    category_type=data['category_type'],
                    amount=data['amount'],
                    message_id=message_id,
                )
                await state.set_state(None)
                await safe_edit_text(
                    callback.message,
                    CATEGORY_SELECTION_TEXT,
                    reply_markup=await categories_keyboard(
                        user_id=user_id,
                        category_type=data['category_type'],
                    ),
                )

            case NavigationStep.ACCOUNT_SELECTION:
                data = await get_required_state_data(state, 'category_id')
                await set_navigation_step(
                    state=state,
                    current_step=NavigationStep.ACCOUNT_SELECTION,
                    previous_step=NavigationStep.CATEGORY_SELECTION,
                    user_id=user_id,
                    category_id=data['category_id'],
                    message_id=message_id,
                )
                await state.set_state(None)
                await safe_edit_text(
                    callback.message,
                    ACCOUNT_SELECTION_TEXT,
                    reply_markup=await accounts_keyboard(user_id),
                )

            case NavigationStep.DESCRIPTION_INPUT:
                data = await get_required_state_data(state, 'account_id')
                await set_navigation_step(
                    state=state,
                    current_step=NavigationStep.DESCRIPTION_INPUT,
                    previous_step=NavigationStep.ACCOUNT_SELECTION,
                    user_id=user_id,
                    account_id=data['account_id'],
                    message_id=message_id,
                )
                await state.set_state(AddDescription.description_input)
                await safe_edit_text(
                    callback.message,
                    DESCRIPTION_INPUT_TEXT,
                    reply_markup=back_keyboard(),
                )

            case _:
                await _show_main_menu(callback, state, user_id)

    except InvalidStateDataError as error:
        logger.warning(
            'Back button clicked with invalid state data',
            extra={
                'user_id': user_id,
                'previous_step': previous_step,
                'message_id': message_id,
                'error': str(error),
            },
        )
        await _show_main_menu(
            callback,
            state,
            user_id,
            text=NAVIGATION_RESET_TEXT,
        )

    logger.info(
        'Back button clicked',
        extra={
            'user_id': user_id,
            'previous_step': previous_step,
            'message_id': message_id,
        },
    )

    await callback.answer()
