from sqlalchemy import select

from app.database.database import async_session
from app.database.models import Account


async def get_accounts(user_id: int) -> list[Account]:
    async with async_session() as session:
        result = await session.scalars(
            select(Account).where(Account.user_id == user_id)
        )
        return result.all()
    

async def get_account(
        user_id: int,
        account_id: int
) -> Account | None:
    async with async_session() as session:
        return await session.scalar(
            select(Account).where(
                Account.user_id == user_id,
                Account.account_id == account_id,
            )
        )