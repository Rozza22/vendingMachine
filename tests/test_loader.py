import pytest

from vending_machine.loader import load_machine_from_csv
from vending_machine.machine import VendingMachine


def test_loader_populates_correct_slots():
    machine = VendingMachine()
    load_machine_from_csv("tests/test_data/initial_stock_test.csv", machine)

    assert machine.get_slot(1).product_assigned.name == "Coke"
    assert machine.get_slot(1).quantity_in_place == 10

    assert machine.get_slot(2).product_assigned.name == "Twix"
    assert machine.get_slot(2).quantity_in_place == 10

    assert machine.get_slot(3).product_assigned.name == "Lucky Strike"
    assert machine.get_slot(3).quantity_in_place == 10


def test_loader_rejects_invalid_sell_price():
    with pytest.raises(ValueError):
        machine = VendingMachine()
        load_machine_from_csv("tests/test_data/invalid_products.csv", machine)
