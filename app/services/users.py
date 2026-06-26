from sqlalchemy.exc import IntegrityError

from app.database.models import Account, Category, User
from app.database.repositories.users import (
    create_user,
    get_user_by_telegram_id,
)
from app.defaults import DEFAULT_ACCOUNTS, DEFAULT_CATEGORIES


async def get_or_create_user(telegram_id: int) -> User:
    user = await get_user_by_telegram_id(telegram_id)

    if user:
        return user

    user = User(
        telegram_id=telegram_id,
        categories=[
            Category(**category) for category in DEFAULT_CATEGORIES
        ],
        accounts=[
            Account(**account) for account in DEFAULT_ACCOUNTS
        ],
    )

    try:
        return await create_user(user)
    except IntegrityError:
        existing_user = await get_user_by_telegram_id(telegram_id)
        if existing_user:
            return existing_user

        raise
