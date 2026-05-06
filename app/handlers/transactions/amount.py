from aiogram import Router
from aiogram.fsm.context import FSMContext
from aiogram.types import Message

from app.database.repositories.users import get_user_by_telegram_id
from app.exceptions import InvalidAmountError
from app.keyboards import back_keyboard, categories
from app.logger import setup_logger
from app.services.navigation.service import set_step
from app.services.navigation.steps import NavigationStep
from app.services.transactions import parse_amount
from app.states import AddTransaction
from app.messages import CATEGORY_SELECTION_TEXT


router = Router()
logger = setup_logger(__name__)


@router.message(AddTransaction.amount_input)
async def amount_submitted(
    message: Message,
    state: FSMContext,
) -> None:
    user = await get_user_by_telegram_id(message.from_user.id)
    user_id = user.user_id

    data = await state.get_data()
    message_id = data['message_id']
    transaction_type = data['transaction_type']

    try:
        amount = parse_amount(message.text)
    except InvalidAmountError as error:  
        await message.delete()
        await message.bot.edit_message_text(
            text=str(error),
            chat_id=message.chat.id,
            message_id=message_id,
            reply_markup=await back_keyboard(),
        )

        logger.warning(
            'Invalid transaction amount submitted',
            extra={
                'user_id': user_id,
                'transaction_type': transaction_type,
                'message_id': message_id,
                'error': str(error),
            },
        )

        return

    await set_step(
        state=state,
        current_step=NavigationStep.CATEGORY_SELECTION,
        user_id=user_id,
        amount=amount,
        message_id=message_id,
    )

    await message.delete()
    await message.bot.edit_message_text(
        text=CATEGORY_SELECTION_TEXT,
        chat_id=message.chat.id,
        message_id=message_id,
        reply_markup=await categories(
            user,
            transaction_type,
        ),
    )

    logger.info(
        'Amount submitted',
        extra={
            'user_id': user_id,
            'transaction_type': transaction_type,
            'message_id': message_id,
        },
    )