import asyncio
from typing import Any

import pytest

from app.exceptions import InvalidStateDataError
from app.services.navigation.service import (
    get_required_state_data,
    set_navigation_step,
)
from app.services.navigation.steps import NavigationStep


class FakeState:
    def __init__(self, data: dict[str, Any] | None = None) -> None:
        self.data = data.copy() if data else {}

    async def get_data(self) -> dict[str, Any]:
        return self.data.copy()

    async def update_data(self, **kwargs: Any) -> None:
        self.data.update(kwargs)


def test_set_navigation_step() -> None:
    state = FakeState({'current_step': NavigationStep.MAIN_MENU})

    asyncio.run(
        set_navigation_step(
            state=state,
            current_step=NavigationStep.AMOUNT_INPUT,
            user_id=1,
            extra_value='test',
        )
    )

    assert state.data == {
        'previous_step': NavigationStep.MAIN_MENU,
        'current_step': NavigationStep.AMOUNT_INPUT,
        'user_id': 1,
        'extra_value': 'test',
    }


def test_set_navigation_step_previous_step_none() -> None:
    state = FakeState()

    asyncio.run(
        set_navigation_step(
            state=state,
            current_step=NavigationStep.MAIN_MENU,
            user_id=1,
        )
    )

    assert state.data == {
        'previous_step': None,
        'current_step': NavigationStep.MAIN_MENU,
        'user_id': 1,
    }


def test_set_navigation_step_accepts_explicit_previous_step() -> None:
    state = FakeState({'current_step': NavigationStep.CATEGORY_SELECTION})

    asyncio.run(
        set_navigation_step(
            state=state,
            current_step=NavigationStep.AMOUNT_INPUT,
            user_id=1,
            previous_step=NavigationStep.MAIN_MENU,
            category_type='expense',
        )
    )

    assert state.data == {
        'current_step': NavigationStep.AMOUNT_INPUT,
        'previous_step': NavigationStep.MAIN_MENU,
        'user_id': 1,
        'category_type': 'expense',
    }


def test_get_required_state_data_returns_data_when_keys_exist() -> None:
    state = FakeState({'message_id': 1, 'amount': 100})

    result = asyncio.run(
        get_required_state_data(state, 'message_id', 'amount')
    )

    assert result == {'message_id': 1, 'amount': 100}


def test_get_required_state_data_raises_when_key_is_missing() -> None:
    state = FakeState({'message_id': 1})

    with pytest.raises(InvalidStateDataError) as error:
        asyncio.run(
            get_required_state_data(state, 'message_id', 'amount')
        )

    assert str(error.value) == 'Missing state data: amount'
