from aiogram import F, Router
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery

from app.database.repositories.users import get_user_by_telegram_id
from app.keyboards import description
from app.logger import setup_logger
from app.services.navigation.service import set_step
from app.services.navigation.steps import NavigationStep
from app.states import AddDescription
from app.messages import DESCRIPTION_INPUT_TEXT


router = Router()
logger = setup_logger(__name__)


@router.callback_query(F.data.startswith('account_'))
async def account_selected(
    callback: CallbackQuery,
    state: FSMContext,
) -> None: 
    user = await get_user_by_telegram_id(callback.from_user.id)
    user_id = user.user_id

    data = await state.get_data()
    account_id = int(callback.data.split('_')[1])
    message_id = data['message_id']

    await set_step(
        state=state,
        current_step=NavigationStep.DESCRIPTION_INPUT,
        user_id=user_id,
        account_id=account_id,
        message_id=message_id,
    )
    await state.set_state(AddDescription.description_input)

    await callback.message.edit_text(
        DESCRIPTION_INPUT_TEXT,
        reply_markup=await description(),
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