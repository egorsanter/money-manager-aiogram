from sqlalchemy import select

from app.database.models import async_session
from app.database.models import User, Category


async def set_user(telegram_id) -> None:
    async with async_session() as session:
        user = await session.scalar(
            select(User).where(User.telegram_id == telegram_id)
        )
    
        if not user:
            user = User(
                telegram_id=telegram_id,
                categories=[
                    Category(name="Еда", type="expense"),
                    Category(name="Зарплата", type="income"),
                ]
            )

            session.add(user)
            await session.commit()