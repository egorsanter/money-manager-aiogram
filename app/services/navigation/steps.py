# navigation_steps.py
from enum import Enum

class NavigationStep(str, Enum):
    MAIN = 'main'
    AMOUNT_INPUT = 'amount_input'
    CATEGORY_SELECTION = 'category_selection'
    ACCOUNT_SELECTION = 'account_selection'
    DESCRIPTION_INPUT = 'description_input'