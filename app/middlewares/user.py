from collections.abc import Awaitable, Callable
from typing import Any

from aiogram import BaseMiddleware
from aiogram.types import TelegramObject

from app.services.users import get_or_create_user


class UserMiddleware(BaseMiddleware):
    async def __call__(
        self,
        handler: Callable[[TelegramObject, dict[str, Any]], Awaitable[Any]],
        event: TelegramObject,
        data: dict[str, Any],
    ) -> Any:
        telegram_user = data.get('event_from_user')

        if telegram_user is None:
            return await handler(event, data)

        user = await get_or_create_user(telegram_user.id)
        data['user_id'] = user.user_id

        return await handler(event, data)