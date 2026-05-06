from aiogram.fsm.context import FSMContext
from aiogram.types import Message

from app.keyboards import main_menu
from app.logger import setup_logger
from app.messages import MAIN_MENU_TEXT
from app.services.navigation.service import set_step
from app.services.navigation.steps import NavigationStep


logger = setup_logger(__name__)


async def show_main_menu(
    message: Message,
    state: FSMContext,
    user_id: int
) -> None:
    await state.clear()
    
    await set_step(
        state=state,
        current_step=NavigationStep.MAIN,
        user_id=user_id,
    )

    await message.answer(MAIN_MENU_TEXT, reply_markup=await main_menu())