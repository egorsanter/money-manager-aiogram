from aiogram.fsm.state import State, StatesGroup


class AddTransaction(StatesGroup):
    amount_input = State()


class AddDescription(StatesGroup):
    description_input = State()
