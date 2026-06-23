from decimal import Decimal

import pytest

from vending_machine.money import InvalidMoney, parse_money


@pytest.mark.parametrize(
    "inp,expected",
    [
        ("1.50", Decimal("1.50")),
        ("1.5", Decimal("1.50")),
        (1, Decimal("1.00")),
        (1.234, Decimal("1.23")),  # rounded down
        (1.235, Decimal("1.24")),  # ROUND_HALF_UP -> up
        (Decimal("2.00"), Decimal("2.00")),
    ],
)
def test_parse_money_valid(inp, expected):
    assert parse_money(inp) == expected


@pytest.mark.parametrize("bad", ["abc", "", "  ", None])
def test_parse_money_invalid(bad):
    with pytest.raises((InvalidMoney, TypeError)):
        parse_money(bad)


def test_parse_money_negative():
    with pytest.raises(InvalidMoney):
        parse_money("-0.01")
