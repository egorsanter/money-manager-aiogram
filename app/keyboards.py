from aiogram.types import InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder

from app.database.repositories.accounts import get_accounts
from app.database.repositories.categories import get_categories
from app.messages import Button, Buttons


def _build_keyboard(
    *buttons: Button,
    adjust: int = 1,
) -> InlineKeyboardMarkup:
    kb = InlineKeyboardBuilder()

    for button in buttons:
        kb.button(
            text=button.text,
            callback_data=button.callback_data,
        )

    kb.adjust(adjust)

    return kb.as_markup()


def back_keyboard() -> InlineKeyboardMarkup:
    return _build_keyboard(Buttons.BACK)


def main_menu_button_keyboard() -> InlineKeyboardMarkup:
    return _build_keyboard(Buttons.MAIN_MENU)


def main_menu_keyboard() -> InlineKeyboardMarkup:
    return _build_keyboard(
        Buttons.INCOME,
        Buttons.EXPENSE,
        Buttons.BALANCE,
        adjust=2,
    )


def description_keyboard() -> InlineKeyboardMarkup:
    return _build_keyboard(
        Buttons.SKIP,
        Buttons.BACK,
    )


async def categories_keyboard(
    user_id: int,
    category_type: str,
) -> InlineKeyboardMarkup:
    categories = await get_categories(
        user_id=user_id,
        category_type=category_type
    )

    return _build_keyboard(
        *[
            Button(
                text=category.name,
                callback_data=f'category_{category.category_id}',
            )
            for category in categories
        ],
        Buttons.BACK,
        adjust=4,
    )


async def accounts_keyboard(user_id: int) -> InlineKeyboardMarkup:
    accounts = await get_accounts(user_id)

    return _build_keyboard(
        *[
            Button(
                text=account.name,
                callback_data=f'account_{account.account_id}',
            )
            for account in accounts
        ],
        Buttons.BACK,
        adjust=4,
    )
