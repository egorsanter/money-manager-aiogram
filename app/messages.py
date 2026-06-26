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


class Buttons:
    BACK = ('⬅️ Back', 'back')
    MAIN_MENU = ('🏠 Main menu', 'main_menu')

    INCOME = ('💰 Income', 'income')
    EXPENSE = ('💸 Expense', 'expense')

    SKIP = ('⏭️ Skip', 'description_skip')
