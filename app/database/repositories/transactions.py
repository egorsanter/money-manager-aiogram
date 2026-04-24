from sqlalchemy import select

from app.database.models import async_session
from app.database.models import Transaction, User


async def add_transaction(telegram_id: int, category_id: int, amount: float) -> None:
    async with async_session() as session:
        user = await session.scalar(select(User).where(User.telegram_id == telegram_id))
        
        new_transaction = Transaction(
            user_id=user.user_id,
            category_id=category_id,
            amount=amount
        )
        session.add(new_transaction)
        await session.commit()