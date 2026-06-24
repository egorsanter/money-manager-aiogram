import asyncio
from types import SimpleNamespace
from typing import Any

from app.middlewares import user as user_middleware


def test_user_middleware_provides_user_id(monkeypatch) -> None:
    async def fake_get_or_create_user(telegram_id: int) -> SimpleNamespace:
        assert telegram_id == 123
        return SimpleNamespace(user_id=1)

    async def handler(event: object, data: dict[str, Any]) -> str:
        assert data['user_id'] == 1
        return 'handled'

    monkeypatch.setattr(
        user_middleware,
        'get_or_create_user',
        fake_get_or_create_user,
    )

    data = {'event_from_user': SimpleNamespace(id=123)}
    result = asyncio.run(
        user_middleware.UserMiddleware()(handler, object(), data)
    )

    assert result == 'handled'


def test_user_middleware_skips_event_without_user(monkeypatch) -> None:
    async def fake_get_or_create_user(telegram_id: int) -> None:
        raise AssertionError('get_or_create_user should not be called')

    async def handler(event: object, data: dict[str, Any]) -> str:
        assert 'user_id' not in data
        return 'handled'

    monkeypatch.setattr(
        user_middleware,
        'get_or_create_user',
        fake_get_or_create_user,
    )

    result = asyncio.run(
        user_middleware.UserMiddleware()(handler, object(), {})
    )

    assert result == 'handled'
