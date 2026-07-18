from decimal import Decimal

import pytest

from vending_machine.product import Product


def test_product_creation():
    product = Product("Soda", "1.50", "0.50")

    assert product.name == "Soda"
    assert product.sell_price == Decimal(1.5)
    assert product.unit_stock_cost == Decimal("0.50")


@pytest.mark.parametrize("bad_name", ["", "   ", None, 9])
def test_product_invalid_name(bad_name):
    with pytest.raises(ValueError):
        Product(bad_name, "1.50", "0.50")


@pytest.mark.parametrize("bad_price", ["", "abc", "-1.00", None])
def test_product_invalid_sell_price(bad_price):
    with pytest.raises(ValueError):
        Product("Soda", bad_price, "0.50")


@pytest.mark.parametrize("bad_cost", ["", "abc", "-0.01", None])
def test_product_invalid_unit_stock_cost(bad_cost):
    with pytest.raises(ValueError):
        Product("Soda", "1.50", bad_cost)
