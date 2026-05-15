from decimal import Decimal

import pytest

from app.exceptions import InvalidAmountError
from app.messages import INVALID_AMOUNT_MSG, NON_POSITIVE_AMOUNT_MSG
from app.services.transactions import parse_amount


@pytest.mark.parametrize(
    ('value', 'expected'),
    [
        ('0.01', Decimal('0.01')),
        ('10', Decimal('10.00')),
        ('10.5', Decimal('10.50')),
        ('10.50', Decimal('10.50')),
        ('10,50', Decimal('10.50')),
        ('  10  ', Decimal('10.00')),
        ('1 000,50', Decimal('1000.50')),
    ],
)
def test_parse_amount_accepts_valid_values(
    value: str,
    expected: Decimal,
) -> None:
    assert parse_amount(value) == expected


@pytest.mark.parametrize(
    'value',
    [
        None,
        '',
        '   ',
    ],
)
def test_parse_amount_rejects_empty_values(value: str | None) -> None:
    with pytest.raises(InvalidAmountError) as error:
        parse_amount(value)

    assert str(error.value) == INVALID_AMOUNT_MSG


@pytest.mark.parametrize(
    'value',
    [
        'abc',
        '.50',
        '10.',
        '1.2.3',
        '1,2,3',
        '1.50000',
        '1.505',
    ],
)
def test_parse_amount_rejects_invalid_format(value: str) -> None:
    with pytest.raises(InvalidAmountError) as error:
        parse_amount(value)

    assert str(error.value) == INVALID_AMOUNT_MSG


@pytest.mark.parametrize('value', ['0', '0.00', '-0.00', '-1', '-0.01'])
def test_parse_amount_rejects_non_positive_values(value: str) -> None:
    with pytest.raises(InvalidAmountError) as error:
        parse_amount(value)

    assert str(error.value) == NON_POSITIVE_AMOUNT_MSG
