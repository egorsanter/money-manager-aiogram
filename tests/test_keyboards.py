import asyncio
from types import SimpleNamespace

from aiogram.types import InlineKeyboardMarkup

from app import keyboards
from app.messages import Button, Buttons


def button_pair(button: Button) -> tuple[str, str]:
    return button.text, button.callback_data


def get_button_pairs(markup: InlineKeyboardMarkup) -> list[tuple[str, str]]:
    return [
        (button.text, button.callback_data)
        for row in markup.inline_keyboard
        for button in row
    ]


def test_back_keyboard() -> None:
    assert get_button_pairs(keyboards.back_keyboard()) == [
        button_pair(Buttons.BACK),
    ]


def test_main_menu_button_keyboard() -> None:
    assert get_button_pairs(keyboards.main_menu_button_keyboard()) == [
        button_pair(Buttons.MAIN_MENU),
    ]


def test_main_menu_keyboard() -> None:
    assert get_button_pairs(keyboards.main_menu_keyboard()) == [
        button_pair(Buttons.INCOME),
        button_pair(Buttons.EXPENSE),
        button_pair(Buttons.BALANCE),
    ]


def test_description_keyboard() -> None:
    assert get_button_pairs(keyboards.description_keyboard()) == [
        button_pair(Buttons.SKIP),
        button_pair(Buttons.BACK),
    ]


def test_categories_keyboard(monkeypatch) -> None:
    async def test_get_categories(
        user_id: int,
        category_type: str,
    ) -> list[SimpleNamespace]:
        assert user_id == 1
        assert category_type == 'expense'
        return [
            SimpleNamespace(category_id=10, name='Food'),
            SimpleNamespace(category_id=20, name='Transport'),
        ]

    monkeypatch.setattr(keyboards, 'get_categories', test_get_categories)

    markup = asyncio.run(
        keyboards.categories_keyboard(user_id=1, category_type='expense')
    )

    assert get_button_pairs(markup) == [
        ('Food', 'category_10'),
        ('Transport', 'category_20'),
        button_pair(Buttons.BACK),
    ]


def test_accounts_keyboard(monkeypatch) -> None:
    async def test_get_accounts(user_id: int) -> list[SimpleNamespace]:
        assert user_id == 1
        return [
            SimpleNamespace(account_id=10, name='Cash'),
            SimpleNamespace(account_id=20, name='Card'),
        ]

    monkeypatch.setattr(keyboards, 'get_accounts', test_get_accounts)

    markup = asyncio.run(keyboards.accounts_keyboard(user_id=1))

    assert get_button_pairs(markup) == [
        ('Cash', 'account_10'),
        ('Card', 'account_20'),
        button_pair(Buttons.BACK),
    ]
