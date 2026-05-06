from aiogram.fsm.context import FSMContext

from app.logger import setup_logger


logger = setup_logger(__name__)


async def set_step(
    state: FSMContext,
    current_step: str,
    user_id: int,
    **kwargs,
) -> None:
    data = await state.get_data()
    previous_step = data.get('current_step')

    await state.update_data(
        previous_step=previous_step,
        current_step=current_step,
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