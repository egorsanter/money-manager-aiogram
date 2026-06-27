from aiogram import F, Router
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, Message

from app.exceptions import InvalidTransactionReferenceError
from app.keyboards import main_menu_button_keyboard
from app.logger import setup_logger
from app.messages import TRANSACTION_CREATE_FAILED_TEXT, Buttons
from app.services.telegram import (
    safe_delete_message,
    safe_edit_message_text,
    safe_edit_text,
)
from app.services.transactions import finalize_transaction
from app.states import AddDescription

router = Router()
logger = setup_logger(__name__)


@router.callback_query(F.data == Buttons.SKIP.callback_data)
async def description_skipped(
    callback: CallbackQuery,
    state: FSMContext,
    user_id: int,
) -> None:
    data = await state.get_data()
    message_id = data['message_id']

    try:
        transaction = await finalize_transaction(
            user_id=user_id,
            account_id=data['account_id'],
            category_id=data['category_id'],
            amount=data['amount'],
            description=None,
        )
    except InvalidTransactionReferenceError:
        await state.clear()
        await safe_edit_text(
            callback.message,
            text=TRANSACTION_CREATE_FAILED_TEXT,
            reply_markup=main_menu_button_keyboard(),
        )
        await callback.answer()

        logger.warning(
            'Transaction references are invalid',
            extra={
                'user_id': user_id,
                'message_id': message_id,
                'account_id': data.get('account_id'),
                'category_id': data.get('category_id'),
            },
        )

        return

    await state.clear()

    await safe_edit_text(
        callback.message,
        text=transaction.text,
        reply_markup=main_menu_button_keyboard(),
    )
    await callback.answer()

    logger.info(
        'Transaction created',
        extra={
            'user_id': user_id,
            'message_id': message_id,
            'transaction_id': transaction.transaction_id,
        },
    )


@router.message(AddDescription.description_input)
async def description_submitted(
    message: Message,
    state: FSMContext,
    user_id: int,
) -> None:
    data = await state.get_data()
    message_id = data['message_id']
    description = message.text

    try:
        transaction = await finalize_transaction(
            user_id=user_id,
            account_id=data['account_id'],
            category_id=data['category_id'],
            amount=data['amount'],
            description=description,
        )
    except InvalidTransactionReferenceError:
        await state.clear()
        await safe_delete_message(message)
        await safe_edit_message_text(
            bot=message.bot,
            text=TRANSACTION_CREATE_FAILED_TEXT,
            chat_id=message.chat.id,
            message_id=message_id,
            reply_markup=main_menu_button_keyboard(),
        )

        logger.warning(
            'Transaction references are invalid',
            extra={
                'user_id': user_id,
                'message_id': message_id,
                'account_id': data.get('account_id'),
                'category_id': data.get('category_id'),
            },
        )

        return

    await state.clear()

    await safe_delete_message(message)
    await safe_edit_message_text(
        bot=message.bot,
        text=transaction.text,
        chat_id=message.chat.id,
        message_id=message_id,
        reply_markup=main_menu_button_keyboard(),
    )

    logger.info(
        'Transaction created',
        extra={
            'user_id': user_id,
            'message_id': message_id,
            'transaction_id': transaction.transaction_id,
        },
    )
