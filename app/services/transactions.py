import re
from decimal import Decimal

from app.exceptions import InvalidAmountError
from app.messages import INVALID_AMOUNT_MSG, NON_POSITIVE_AMOUNT_MSG


AMOUNT_PATTERN = re.compile(r'^-?\d+(?:\.\d{1,2})?$')


def parse_amount(value: str | None) -> Decimal:
    if not value or not value.strip():
        raise InvalidAmountError(INVALID_AMOUNT_MSG)

    normalized_amount = (
        value
        .strip()
        .replace(' ', '')
        .replace(',', '.')
    )

    if not AMOUNT_PATTERN.fullmatch(normalized_amount):
        raise InvalidAmountError(INVALID_AMOUNT_MSG)

    amount = Decimal(normalized_amount)

    if amount <= 0:
        raise InvalidAmountError(NON_POSITIVE_AMOUNT_MSG)

    return amount.quantize(Decimal('0.01'))
