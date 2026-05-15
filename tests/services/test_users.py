import asyncio
from types import SimpleNamespace

from app.defaults import DEFAULT_ACCOUNTS, DEFAULT_CATEGORIES
from app.services import users as users_service


def test_get_or_create_user_returns_existing_user(monkeypatch) -> None:
    existing_user = SimpleNamespace(user_id=1, telegram_id=123)

    async def fake_get_user_by_telegram_id(telegram_id: int):
        assert telegram_id == 123
        return existing_user

    async def fake_create_user(user):
        raise AssertionError('create_user should not be called')

    monkeypatch.setattr(
        users_service,
        'get_user_by_telegram_id',
        fake_get_user_by_telegram_id,
    )
    monkeypatch.setattr(users_service, 'create_user', fake_create_user)

    result = asyncio.run(users_service.get_or_create_user(123))

    assert result is existing_user


def test_get_or_create_user_creates_user_with_defaults(monkeypatch) -> None:
    created_users = []

    async def fake_get_user_by_telegram_id(telegram_id: int):
        assert telegram_id == 123
        return None

    async def fake_create_user(user):
        created_users.append(user)
        return user

    monkeypatch.setattr(
        users_service,
        'get_user_by_telegram_id',
        fake_get_user_by_telegram_id,
    )
    monkeypatch.setattr(users_service, 'create_user', fake_create_user)

    result = asyncio.run(users_service.get_or_create_user(123))

    assert result is created_users[0]
    assert result.telegram_id == 123
    assert [account.name for account in result.accounts] == [
        account['name'] for account in DEFAULT_ACCOUNTS
    ]
    assert [
        (category.name, category.category_type)
        for category in result.categories
    ] == [
        (category['name'], category['category_type'])
        for category in DEFAULT_CATEGORIES
    ]
