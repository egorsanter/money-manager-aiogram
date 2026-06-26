import re
from dataclasses import dataclass
from decimal import Decimal

from app.database.repositories.accounts import get_account
from app.database.repositories.categories import get_category
from app.database.repositories.transactions import create_transaction
from app.exceptions import InvalidAmountError, InvalidTransactionReferenceError
from app.messages import (
    INVALID_AMOUNT_MSG,
    NO_DESCRIPTION_TEXT,
    NON_POSITIVE_AMOUNT_MSG,
    TRANSACTION_CREATED_TEXT,
)

AMOUNT_PATTERN = re.compile(r'^-?\d+(?:\.\d{1,2})?$')


@dataclass(frozen=True)
class CreatedTransaction:
    transaction_id: int
    category_name: str
    account_name: str


@dataclass(frozen=True)
class FinalizedTransaction:
    text: str
    transaction_id: int


def parse_amount(value: str | None) -> Decimal:
    if not value or not value.strip():
        raise InvalidAmountError(INVALID_AMOUNT_MSG)

    normalized_amount = (
        value
        .strip()
        .replace(' ', '')
        .replace(',', '.')
    )

    if not AMOUNT_PATTERN.fullmatch(normalized_amount):
        raise InvalidAmountError(INVALID_AMOUNT_MSG)

    amount = Decimal(normalized_amount)

    if amount <= 0:
        raise InvalidAmountError(NON_POSITIVE_AMOUNT_MSG)

    return amount.quantize(Decimal('0.01'))


async def create_transaction_for_user(
    user_id: int,
    account_id: int,
    category_id: int,
    amount: Decimal,
    description: str | None = None,
) -> CreatedTransaction:
    category = await get_category(user_id, category_id)
    account = await get_account(user_id, account_id)

    if category is None or account is None:
        raise InvalidTransactionReferenceError(
            'Category or account does not belong to the user'
        )

    balance_delta = amount
    if category.category_type == 'expense':
        balance_delta = -amount

    transaction_id = await create_transaction(
        user_id=user_id,
        account_id=account_id,
        category_id=category_id,
        amount=amount,
        balance_delta=balance_delta,
        description=description,
    )

    return CreatedTransaction(
        transaction_id=transaction_id,
        category_name=category.name,
        account_name=account.name,
    )


async def finalize_transaction(
    *,
    user_id: int,
    account_id: int,
    category_id: int,
    amount: Decimal,
    description: str | None,
) -> FinalizedTransaction:
    transaction = await create_transaction_for_user(
        user_id=user_id,
        account_id=account_id,
        category_id=category_id,
        amount=amount,
        description=description,
    )

    text = TRANSACTION_CREATED_TEXT.format(
        amount=amount,
        category_name=transaction.category_name,
        account_name=transaction.account_name,
        description=description or NO_DESCRIPTION_TEXT,
    )

    return FinalizedTransaction(
        text=text,
        transaction_id=transaction.transaction_id,
    )
