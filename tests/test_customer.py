from decimal import Decimal

import pytest

from vending_machine.customer import Customer


def test_customer_initializes_with_balance():
    customer = Customer("2.50")

    assert customer.balance == Decimal("2.50")


def test_customer_deposit_adds_to_balance():
    customer = Customer("1.00")
    customer.deposit("0.75")

    assert customer.balance == Decimal("1.75")


def test_customer_refund_returns_and_resets_balance():
    customer = Customer("3.25")

    refunded_amount = customer.refund()

    assert refunded_amount == Decimal("3.25")
    assert customer.balance == Decimal("0.00")


@pytest.mark.parametrize("bad_value", ["", "abc", None, -1])
def test_customer_rejects_invalid_balance_and_deposit_values(bad_value):
    with pytest.raises(ValueError):
        Customer(bad_value)

    customer = Customer("1.00")
    with pytest.raises(ValueError):
        customer.deposit(bad_value)
