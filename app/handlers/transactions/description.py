from aiogram import F, Router
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, Message

from app.database.repositories.transactions import create_transaction
from app.database.repositories.users import get_user_by_telegram_id
from app.keyboards import show_main_menu
from app.logger import setup_logger
from app.states import AddDescription
from app.database.repositories.categories import get_category
from app.database.repositories.accounts import get_account


router = Router()
logger = setup_logger(__name__)


@router.callback_query(F.data == 'description_skip')
async def description_skipped(
    callback: CallbackQuery,
    state: FSMContext,
) -> None:
    user = await get_user_by_telegram_id(callback.from_user.id)
    user_id = user.user_id

    data = await state.get_data()
    message_id = data['message_id']

    transaction_id = await create_transaction(
        user_id=user_id,
        account_id=data['account_id'],
        category_id=data['category_id'],
        amount=data['amount'],
        description=None,
    )

    category = await get_category(user_id, data['category_id'])
    account = await get_account(user_id, data['account_id'])

    category_name = data.get('category_name') or category.name
    account_name = data.get('account_name') or account.name

    text = (
        "✅ Transaction created\n\n"
        f"💸 Amount: {data['amount']}\n"
        f'📂 Category: {category_name}\n'
        f'🏦 Account: {account_name}\n'
    )

    await state.clear()

    await callback.message.edit_text(
        text=text,
        reply_markup=await show_main_menu(),
    )
    await callback.answer()

    logger.info(
        'Transaction created',
        extra={
            'user_id': user_id,
            'message_id': message_id,
            'transaction_id': transaction_id,
        },
    )


@router.message(AddDescription.description_input)
async def description_submitted(
    message: Message, 
    state: FSMContext
) -> None:
    user = await get_user_by_telegram_id(message.from_user.id)
    user_id = user.user_id

    data = await state.get_data()
    message_id = data['message_id']
    description = message.text

    transaction_id = await create_transaction(
        user_id=user.user_id,
        account_id=data['account_id'],
        category_id=data['category_id'],
        amount=data['amount'],
        description=description,
    )

    category = await get_category(user_id, data['category_id'])
    account = await get_account(user_id, data['account_id'])

    category_name = data.get('category_name') or category.name
    account_name = data.get('account_name') or account.name

    text = (
        "✅ Transaction created\n\n"
        f"💸 Amount: {data['amount']}\n"
        f'📂 Category: {category_name}\n'
        f'🏦 Account: {account_name}\n'
    )

    if description:
        text += f"📝 Description: {description}"

    await state.clear()

    await message.delete()
    await message.bot.edit_message_text(
        text=text,
        chat_id=message.chat.id,
        message_id=message_id,
        reply_markup=await show_main_menu(),
    )

    logger.info(
        'Transaction created',
        extra={
            'user_id': user_id,
            'message_id': message_id,
            'transaction_id': transaction_id,
        },
    )