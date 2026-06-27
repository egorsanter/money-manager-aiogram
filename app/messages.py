from dataclasses import dataclass

START_TEXT = (
    '👋 Hey, fellow!\n\n'
    'I was made by the best man in the world '
    'to help you track your finances. '
    "Let's get started 👇\n\n"
)

CATEGORY_MESSAGES = {
    'expense': 'Select an expense category',
    'income': 'Select an income category',
}

MAIN_MENU_TEXT = '🏠 Main menu'
BALANCE_TEXT = '💳 Balance'
BALANCE_EMPTY_TEXT = 'You do not have any accounts yet.'
BALANCE_ACCOUNT_TEXT = '{account_name}: {balance} {currency}'
NAVIGATION_RESET_TEXT = (
    'This action is no longer available. '
    'Please start again from the main menu.'
)

INVALID_AMOUNT_MSG = 'Please enter the correct amount!'
NON_POSITIVE_AMOUNT_MSG = 'Amount must be greater than 0!'

AMOUNT_INPUT_TEXT = 'Please enter the amount:'
CATEGORY_SELECTION_TEXT = 'Choose a category:'
ACCOUNT_SELECTION_TEXT = 'Choose an account:'
DESCRIPTION_INPUT_TEXT = 'Please enter the description:'
TRANSACTION_CREATE_TEXT = 'Done!'
TRANSACTION_CREATE_FAILED_TEXT = (
    'Could not create transaction. Please start again from the main menu.'
)
INVALID_STATE_TEXT = (
    'This action is no longer available. '
    'Please start again from the main menu.'
)
TRANSACTION_CREATED_TEXT = (
    "✅ Transaction created\n\n"
    "💸 Amount: {amount}\n"
    "📂 Category: {category_name}\n"
    "🏦 Account: {account_name}\n"
    "📝 Description: {description}"
)
NO_DESCRIPTION_TEXT = '–'


@dataclass(frozen=True)
class Button:
    text: str
    callback_data: str


class Buttons:
    BACK = Button('⬅️ Back', 'back')
    MAIN_MENU = Button('🏠 Main menu', 'main_menu')

    INCOME = Button('💰 Income', 'income')
    EXPENSE = Button('💸 Expense', 'expense')

    SKIP = Button('⏭️ Skip', 'description_skip')

    BALANCE = Button('💳 Balance', 'balance')
