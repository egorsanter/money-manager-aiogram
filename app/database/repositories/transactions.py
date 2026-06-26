from decimal import Decimal

from sqlalchemy import select

from app.database.database import async_session
from app.database.models import Account, Transaction
from app.exceptions import AccountNotFoundError


async def create_transaction(
    user_id: int,
    account_id: int,
    category_id: int,
    amount: Decimal,
    balance_delta: Decimal,
    description: str | None = None,
) -> int:
    async with async_session() as session:
        account = await session.scalar(
            select(Account).where(
                Account.account_id == account_id,
                Account.user_id == user_id,
            )
        )
        if account is None:
            raise AccountNotFoundError('Account not found')

        account.balance += balance_delta

        transaction = Transaction(
            user_id=user_id,
            account_id=account_id,
            category_id=category_id,
            amount=amount,
            description=description,
        )

        session.add(transaction)
        await session.flush()
        transaction_id = transaction.transaction_id

        await session.commit()

        return transaction_id
