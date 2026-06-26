import asyncio
from decimal import Decimal
from types import SimpleNamespace

import pytest

from app.exceptions import InvalidAmountError, InvalidTransactionReferenceError
from app.messages import (
    INVALID_AMOUNT_MSG,
    NO_DESCRIPTION_TEXT,
    NON_POSITIVE_AMOUNT_MSG,
)
from app.services import transactions as transactions_service
from app.services.transactions import parse_amount


@pytest.mark.parametrize(
    ('value', 'expected'),
    [
        ('0.01', Decimal('0.01')),
        ('10', Decimal('10.00')),
        ('10.5', Decimal('10.50')),
        ('10.50', Decimal('10.50')),
        ('10,50', Decimal('10.50')),
        ('  10  ', Decimal('10.00')),
        ('1 000,50', Decimal('1000.50')),
    ],
)
def test_parse_amount_accepts_valid_values(
    value: str,
    expected: Decimal,
) -> None:
    assert parse_amount(value) == expected


@pytest.mark.parametrize(
    'value',
    [
        None,
        '',
        '   ',
    ],
)
def test_parse_amount_rejects_empty_values(value: str | None) -> None:
    with pytest.raises(InvalidAmountError) as error:
        parse_amount(value)

    assert str(error.value) == INVALID_AMOUNT_MSG


@pytest.mark.parametrize(
    'value',
    [
        'abc',
        '.50',
        '10.',
        '1.2.3',
        '1,2,3',
        '1.50000',
        '1.505',
    ],
)
def test_parse_amount_rejects_invalid_format(value: str) -> None:
    with pytest.raises(InvalidAmountError) as error:
        parse_amount(value)

    assert str(error.value) == INVALID_AMOUNT_MSG


@pytest.mark.parametrize('value', ['0', '0.00', '-0.00', '-1', '-0.01'])
def test_parse_amount_rejects_non_positive_values(value: str) -> None:
    with pytest.raises(InvalidAmountError) as error:
        parse_amount(value)

    assert str(error.value) == NON_POSITIVE_AMOUNT_MSG


def test_create_transaction_for_user_validates_references(monkeypatch) -> None:
    created_transactions = []

    async def fake_get_category(user_id: int, category_id: int):
        assert user_id == 1
        assert category_id == 10
        return SimpleNamespace(name='Food', category_type='expense')

    async def fake_get_account(user_id: int, account_id: int):
        assert user_id == 1
        assert account_id == 20
        return SimpleNamespace(name='Cash')

    async def fake_create_transaction(**kwargs):
        created_transactions.append(kwargs)
        return 30

    monkeypatch.setattr(
        transactions_service,
        'get_category',
        fake_get_category,
    )
    monkeypatch.setattr(
        transactions_service,
        'get_account',
        fake_get_account,
    )
    monkeypatch.setattr(
        transactions_service,
        'create_transaction',
        fake_create_transaction,
    )

    result = asyncio.run(
        transactions_service.create_transaction_for_user(
            user_id=1,
            account_id=20,
            category_id=10,
            amount=Decimal('100.00'),
            description='Lunch',
        )
    )

    assert result.transaction_id == 30
    assert result.category_name == 'Food'
    assert result.account_name == 'Cash'
    assert created_transactions == [
        {
            'user_id': 1,
            'account_id': 20,
            'category_id': 10,
            'amount': Decimal('100.00'),
            'balance_delta': Decimal('-100.00'),
            'description': 'Lunch',
        }
    ]


def test_create_transaction_for_user_adds_income_to_balance(
    monkeypatch,
) -> None:
    created_transactions = []

    async def fake_get_category(user_id: int, category_id: int):
        return SimpleNamespace(name='Salary', category_type='income')

    async def fake_get_account(user_id: int, account_id: int):
        return SimpleNamespace(name='Card')

    async def fake_create_transaction(**kwargs):
        created_transactions.append(kwargs)
        return 30

    monkeypatch.setattr(
        transactions_service,
        'get_category',
        fake_get_category,
    )
    monkeypatch.setattr(
        transactions_service,
        'get_account',
        fake_get_account,
    )
    monkeypatch.setattr(
        transactions_service,
        'create_transaction',
        fake_create_transaction,
    )

    asyncio.run(
        transactions_service.create_transaction_for_user(
            user_id=1,
            account_id=20,
            category_id=10,
            amount=Decimal('100.00'),
            description=None,
        )
    )

    assert created_transactions[0]['balance_delta'] == Decimal('100.00')


@pytest.mark.parametrize(
    ('category', 'account'),
    [
        (None, SimpleNamespace(name='Cash')),
        (SimpleNamespace(name='Food'), None),
    ],
)
def test_create_transaction_for_user_rejects_invalid_references(
    monkeypatch,
    category,
    account,
) -> None:
    async def fake_get_category(user_id: int, category_id: int):
        return category

    async def fake_get_account(user_id: int, account_id: int):
        return account

    async def fake_create_transaction(**kwargs):
        raise AssertionError('create_transaction should not be called')

    monkeypatch.setattr(
        transactions_service,
        'get_category',
        fake_get_category,
    )
    monkeypatch.setattr(
        transactions_service,
        'get_account',
        fake_get_account,
    )
    monkeypatch.setattr(
        transactions_service,
        'create_transaction',
        fake_create_transaction,
    )

    with pytest.raises(InvalidTransactionReferenceError):
        asyncio.run(
            transactions_service.create_transaction_for_user(
                user_id=1,
                account_id=20,
                category_id=10,
                amount=Decimal('100.00'),
                description='Lunch',
            )
        )


def test_finalize_transaction_builds_text_with_description(
    monkeypatch,
) -> None:
    async def fake_create_transaction_for_user(**kwargs):
        assert kwargs == {
            'user_id': 1,
            'account_id': 20,
            'category_id': 10,
            'amount': Decimal('100.00'),
            'description': 'Lunch',
        }
        return transactions_service.CreatedTransaction(
            transaction_id=30,
            category_name='Food',
            account_name='Cash',
        )

    monkeypatch.setattr(
        transactions_service,
        'create_transaction_for_user',
        fake_create_transaction_for_user,
    )

    result = asyncio.run(
        transactions_service.finalize_transaction(
            user_id=1,
            account_id=20,
            category_id=10,
            amount=Decimal('100.00'),
            description='Lunch',
        )
    )

    assert result.transaction_id == 30
    assert 'Amount: 100.00' in result.text
    assert 'Category: Food' in result.text
    assert 'Account: Cash' in result.text
    assert 'Description: Lunch' in result.text


def test_finalize_transaction_uses_no_description_text(
    monkeypatch,
) -> None:
    async def fake_create_transaction_for_user(**kwargs):
        return transactions_service.CreatedTransaction(
            transaction_id=30,
            category_name='Food',
            account_name='Cash',
        )

    monkeypatch.setattr(
        transactions_service,
        'create_transaction_for_user',
        fake_create_transaction_for_user,
    )

    result = asyncio.run(
        transactions_service.finalize_transaction(
            user_id=1,
            account_id=20,
            category_id=10,
            amount=Decimal('100.00'),
            description=None,
        )
    )

    assert f'Description: {NO_DESCRIPTION_TEXT}' in result.text
