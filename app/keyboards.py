from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.types import InlineKeyboardMarkup

from app.database.models import User
from app.database.repositories.accounts import get_accounts
from app.database.repositories.categories import get_categories
from app.database.repositories.users import get_user_by_telegram_id


async def description() -> InlineKeyboardMarkup:
    kb = InlineKeyboardBuilder()

    kb.button(text='No need', callback_data='description_skip')

    return kb.as_markup()


async def categories(
    user: User,
    category_type: str,
) -> InlineKeyboardMarkup:

    if user is None:
        raise ValueError(f'User with telegram_id={telegram_id} not found')

    all_categories = await get_categories(
        user_id=user.user_id,
        category_type=category_type,
    )

    kb = InlineKeyboardBuilder()

    for category in all_categories:
        kb.button(
            text=category.name,
            callback_data=f'category_{category.category_id}',
        )

    kb.button(text='Back', callback_data='back')
    kb.adjust(4)

    return kb.as_markup()


async def accounts(user_id: int) -> InlineKeyboardMarkup:
    # user = await get_user_by_telegram_id(telegram_id)

    # if user is None:
    #     raise ValueError(f'User with telegram_id={telegram_id} not found')

    all_accounts = await get_accounts(user_id)

    kb = InlineKeyboardBuilder()

    for account in all_accounts:
        kb.button(
            text=account.name,
            callback_data=f'account_{account.account_id}',
        )

    kb.button(text='Back', callback_data='back')
    kb.adjust(4)

    return kb.as_markup()


async def main_menu() -> InlineKeyboardMarkup:
    kb = InlineKeyboardBuilder()

    kb.button(text='💰 Income', callback_data='income')
    kb.button(text='💸 Expense', callback_data='expense')

    kb.adjust(2)

    return kb.as_markup()


async def back_keyboard() -> InlineKeyboardMarkup:
    kb = InlineKeyboardBuilder()
    kb.button(
        text='Back',
        callback_data='back',
    )
    return kb.as_markup()


async def show_main_menu() -> InlineKeyboardMarkup:
    kb = InlineKeyboardBuilder()
    kb.button(
        text='Main',
        callback_data='main',
    )
    return kb.as_markup()