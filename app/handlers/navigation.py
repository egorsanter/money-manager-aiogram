from aiogram import F, Router
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery

from app.database.repositories.users import get_user_by_telegram_id
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
)
from app.services.navigation.steps import NavigationStep
from app.states import AddDescription, AddTransaction


router = Router()
logger = setup_logger(__name__)


@router.callback_query(F.data == 'back')
async def back_selected(
    callback: CallbackQuery,
    state: FSMContext,
) -> None:
    user = await get_user_by_telegram_id(callback.from_user.id)
    user_id = user.user_id
    message_id = callback.message.message_id

    data = await state.get_data()
    previous_step = data.get('previous_step')

    if previous_step == NavigationStep.MAIN:
        await state.clear()
        await state.update_data(
            current_step=NavigationStep.MAIN,
            previous_step=None,
            user_id=user_id,
        )

        await callback.message.edit_text(
            MAIN_MENU_TEXT,
            reply_markup=main_menu_keyboard(),
        )

    elif previous_step == NavigationStep.AMOUNT_INPUT:
        category_type = data['category_type']

        await state.update_data(
            current_step=NavigationStep.AMOUNT_INPUT,
            previous_step=NavigationStep.MAIN,
            user_id=user_id,
            category_type=category_type,
            message_id=message_id,
        )
        await state.set_state(AddTransaction.amount_input)

        await callback.message.edit_text(
            AMOUNT_INPUT_TEXT,
            reply_markup=back_keyboard(),
        )

    elif previous_step == NavigationStep.CATEGORY_SELECTION:
        category_type = data['category_type']
        amount = data['amount']

        await state.update_data(
            current_step=NavigationStep.CATEGORY_SELECTION,
            previous_step=NavigationStep.AMOUNT_INPUT,
            user_id=user_id,
            category_type=category_type,
            amount=amount,
            message_id=message_id,
        )
        await state.set_state(None)

        await callback.message.edit_text(
            CATEGORY_SELECTION_TEXT,
            reply_markup=await categories_keyboard(
                user_id=user_id,
                category_type=category_type,
            ),
        )

    elif previous_step == NavigationStep.ACCOUNT_SELECTION:
        category_id = data['category_id']

        await state.update_data(
            current_step=NavigationStep.ACCOUNT_SELECTION,
            previous_step=NavigationStep.CATEGORY_SELECTION,
            user_id=user_id,
            category_id=category_id,
            message_id=message_id,
        )
        await state.set_state(None)

        await callback.message.edit_text(
            ACCOUNT_SELECTION_TEXT,
            reply_markup=await accounts_keyboard(user_id),
        )

    elif previous_step == NavigationStep.DESCRIPTION_INPUT:
        account_id = data['account_id']

        await state.update_data(
            current_step=NavigationStep.DESCRIPTION_INPUT,
            previous_step=NavigationStep.ACCOUNT_SELECTION,
            user_id=user_id,
            account_id=account_id,
            message_id=message_id,
        )
        await state.set_state(AddDescription.description_input)

        await callback.message.edit_text(
            DESCRIPTION_INPUT_TEXT,
            reply_markup=back_keyboard(),
        )

    else:
        await state.clear()
        await state.update_data(
            current_step=NavigationStep.MAIN,
            previous_step=None,
            user_id=user_id,
        )

        await callback.message.edit_text(
            MAIN_MENU_TEXT,
            reply_markup=main_menu_keyboard(),
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