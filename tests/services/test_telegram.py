import asyncio

import pytest
from aiogram.exceptions import TelegramBadRequest

from app.services.telegram import safe_delete_message, safe_edit_text


def telegram_bad_request(message: str) -> TelegramBadRequest:
    return TelegramBadRequest(method=None, message=message)


def test_safe_delete_message_suppresses_telegram_bad_request() -> None:
    class FakeMessage:
        async def delete(self) -> None:
            raise telegram_bad_request('message to delete not found')

    asyncio.run(safe_delete_message(FakeMessage()))


def test_safe_edit_text_suppresses_message_not_modified() -> None:
    class FakeMessage:
        async def edit_text(self, **kwargs) -> None:
            raise telegram_bad_request('message is not modified')

    asyncio.run(safe_edit_text(FakeMessage(), text='Hello'))


def test_safe_edit_text_reraises_other_telegram_bad_request() -> None:
    class FakeMessage:
        async def edit_text(self, **kwargs) -> None:
            raise telegram_bad_request('message to edit not found')

    with pytest.raises(TelegramBadRequest):
        asyncio.run(safe_edit_text(FakeMessage(), text='Hello'))
