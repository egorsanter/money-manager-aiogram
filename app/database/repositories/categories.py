from sqlalchemy import select

from app.database.models import async_session
from app.database.models import Category


async def get_categories(type) -> None:
    async with async_session() as session:
        return await session.scalars(
            select(Category).where(Category.type == type)
        )
    

async def get_category(category_id):
    async with async_session() as session:
        return await session.scalar(
            select(Category).where(Category.category_id == category_id)
        )