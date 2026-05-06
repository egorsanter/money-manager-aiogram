from decimal import Decimal

from app.database.database import async_session
from app.database.models import Transaction


async def create_transaction(
    user_id: int,
    account_id: int,
    category_id: int,
    amount: Decimal,
    description: str | None = None,
) -> int:
    async with async_session() as session:
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