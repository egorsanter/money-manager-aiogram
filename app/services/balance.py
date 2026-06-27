from app.database.repositories.accounts import get_accounts
from app.messages import (
    BALANCE_ACCOUNT_TEXT,
    BALANCE_EMPTY_TEXT,
    BALANCE_TEXT,
)


async def get_balance_text(user_id: int) -> str:
    accounts = await get_accounts(user_id)

    account_lines = [
        BALANCE_ACCOUNT_TEXT.format(
            account_name=account.name,
            balance=account.balance,
            currency=account.currency,
        )
        for account in accounts
    ]

    if not account_lines:
        return BALANCE_EMPTY_TEXT

    return f'{BALANCE_TEXT}\n\n' + '\n'.join(account_lines)
