import asyncio
from decimal import Decimal
from types import SimpleNamespace

from app.messages import (
    BALANCE_EMPTY_TEXT,
    BALANCE_TEXT,
)
from app.services import balance


def test_get_balance_text_returns_accounts(monkeypatch) -> None:
    async def test_get_accounts(user_id: int) -> list[SimpleNamespace]:
        assert user_id == 1
        return [
            SimpleNamespace(
                name='Cash',
                balance=Decimal('100.00'),
                currency='RUB',
            ),
            SimpleNamespace(
                name='Card',
                balance=Decimal('250.50'),
                currency='RUB',
            ),
        ]

    monkeypatch.setattr(balance, 'get_accounts', test_get_accounts)

    text = asyncio.run(balance.get_balance_text(user_id=1))

    assert text == (
        f'{BALANCE_TEXT}\n\n'
        'Cash: 100.00 RUB\n'
        'Card: 250.50 RUB'
    )


def test_get_balance_text_returns_empty_text(monkeypatch) -> None:
    async def test_get_accounts(user_id: int) -> list[SimpleNamespace]:
        assert user_id == 1
        return []

    monkeypatch.setattr(balance, 'get_accounts', test_get_accounts)

    text = asyncio.run(balance.get_balance_text(user_id=1))

    assert text == BALANCE_EMPTY_TEXT
