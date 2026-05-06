from sqlalchemy import select

from app.database.database import async_session
from app.database.models import Category


async def get_categories(
        user_id: int,
        category_type: str
) -> list[Category]:
    async with async_session() as session:
        result = await session.scalars(
            select(Category).where(
                Category.user_id == user_id,
                Category.category_type == category_type,
            )
        )
        
        return result.all()
    

async def get_category(
        user_id: int,
        category_id: int
) -> Category | None:
    async with async_session() as session:
        return await session.scalar(
            select(Category).where(
                Category.user_id == user_id,
                Category.category_id == category_id,
            )
        )
