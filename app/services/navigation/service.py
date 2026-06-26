from typing import Any

from aiogram.fsm.context import FSMContext

from app.exceptions import InvalidStateDataError
from app.logger import setup_logger

logger = setup_logger(__name__)
_AUTO_PREVIOUS_STEP = object()


async def set_navigation_step(
    state: FSMContext,
    current_step: str,
    user_id: int,
    previous_step: str | None | object = _AUTO_PREVIOUS_STEP,
    **kwargs: Any,
) -> None:
    if previous_step is _AUTO_PREVIOUS_STEP:
        data = await state.get_data()
        previous_step = data.get('current_step')

    await state.update_data(
        current_step=current_step,
        previous_step=previous_step,
        user_id=user_id,
        **kwargs,
    )

    logger.debug(
        'Navigation step changed',
        extra={
            'user_id': user_id,
            'previous_step': previous_step,
            'current_step': current_step,
        },
    )


async def get_required_state_data(
    state: FSMContext,
    *keys: str,
) -> dict:
    data = await state.get_data()
    missing_keys = [key for key in keys if key not in data]

    if missing_keys:
        raise InvalidStateDataError(
            f"Missing state data: {', '.join(missing_keys)}"
        )

    return data