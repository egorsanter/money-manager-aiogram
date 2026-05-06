from decimal import Decimal, InvalidOperation

from app.messages import INVALID_AMOUNT_MSG, NON_POSITIVE_AMOUNT_MSG
from app.exceptions import InvalidAmountError


def parse_amount(value: str | None) -> Decimal:
    if not value or not value.strip():
        raise InvalidAmountError(INVALID_AMOUNT_MSG)

    normalized_amount = (
        value
        .strip()
        .replace(' ', '')
        .replace(',', '.')
    )

    try:
        amount = Decimal(normalized_amount)
    except InvalidOperation as error:
        raise InvalidAmountError(INVALID_AMOUNT_MSG) from error

    if amount <= 0:
        raise InvalidAmountError(NON_POSITIVE_AMOUNT_MSG)

    return amount