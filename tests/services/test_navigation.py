import asyncio
from typing import Any

from app.services.navigation.service import set_step
from app.services.navigation.steps import NavigationStep


class FakeState:
    def __init__(self, data: dict[str, Any] | None = None) -> None:
        self.data = data.copy() if data else {}

    async def get_data(self) -> dict[str, Any]:
        return self.data.copy()

    async def update_data(self, **kwargs: Any) -> None:
        self.data.update(kwargs)


def test_set_step() -> None:
    state = FakeState({'current_step': NavigationStep.MAIN})

    asyncio.run(
        set_step(
            state=state,
            current_step=NavigationStep.AMOUNT_INPUT,
            user_id=1,
            extra_value='test',
        )
    )

    assert state.data == {
        'previous_step': NavigationStep.MAIN,
        'current_step': NavigationStep.AMOUNT_INPUT,
        'extra_value': 'test',
    }


def test_set_step_previous_step_none() -> None:
    state = FakeState()

    asyncio.run(
        set_step(
            state=state,
            current_step=NavigationStep.MAIN,
            user_id=1,
        )
    )

    assert state.data == {
        'previous_step': None,
        'current_step': NavigationStep.MAIN,
    }
