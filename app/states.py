from aiogram.fsm.state import StatesGroup, State

class AddTransaction(StatesGroup):
    amount_input = State()


class AddDescription(StatesGroup):
    description_input = State()
