from sqlalchemy import select

from app.database.database import async_session
from app.database.models import User


async def get_user_by_telegram_id(telegram_id: int) -> User | None:
    async with async_session() as session:
        return await session.scalar(
            select(User).where(User.telegram_id == telegram_id)
        )
    

async def create_user(user: User) -> User:
    async with async_session() as session:
        session.add(user)
        await session.commit()
        return user