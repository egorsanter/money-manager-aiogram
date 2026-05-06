DEFAULT_ACCOUNTS = [
    {'name': 'Cash'},
    {'name': 'Card'},
    {'name': 'Savings'},
]

DEFAULT_EXPENSE_CATEGORIES = [
    {"name": "Food", "category_type": "expense"},
    {"name": "Transport", "category_type": "expense"},
    {"name": "Housing", "category_type": "expense"},
    {"name": "Entertainment", "category_type": "expense"},
    {"name": "Health", "category_type": "expense"},
    {"name": "Clothing", "category_type": "expense"},
    {"name": "Education", "category_type": "expense"},
    {"name": "Utilities", "category_type": "expense"},
    {"name": "Gifts", "category_type": "expense"},
    {"name": "Other", "category_type": "expense"},
]

DEFAULT_INCOME_CATEGORIES = [
    {"name": "Salary", "category_type": "income"},
    {"name": "Freelance", "category_type": "income"},
    {"name": "Investments", "category_type": "income"},
    {"name": "Gifts", "category_type": "income"},
    {"name": "Debt Repayment", "category_type": "income"},
    {"name": "Other", "category_type": "income"},
]

DEFAULT_CATEGORIES = [
    *DEFAULT_EXPENSE_CATEGORIES,
    *DEFAULT_INCOME_CATEGORIES,
]