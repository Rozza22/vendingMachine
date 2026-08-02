import pytest

from vending_machine.machine import VendingMachine
from vending_machine.product import Product
from vending_machine.slot import Slot


@pytest.fixture
def sample_product():
    return Product("Soda", "1.50", "0.50")


def test_machine_can_register_and_retrieve_slots(sample_product):
    machine = VendingMachine()
    slot = Slot(1, sample_product, 0)

    machine.add_slot(slot)

    assert machine.get_slot(1) is slot


def test_machine_allows_slot_number_48(sample_product):
    machine = VendingMachine()
    slot = Slot(48, sample_product, 0)

    machine.add_slot(slot)

    assert machine.get_slot(48) is slot


def test_machine_rejects_slot_number_above_max_on_add(sample_product):
    machine = VendingMachine()

    with pytest.raises(ValueError, match="cannot exceed 48"):
        machine.add_slot(Slot(49, sample_product, 0))


def test_machine_rejects_slot_number_above_max_on_lookup():
    machine = VendingMachine()

    with pytest.raises(ValueError, match="cannot exceed 48"):
        machine.get_slot(49)


def test_machine_rejects_duplicate_slot_registration(sample_product):
    machine = VendingMachine()
    machine.add_slot(Slot(1, sample_product, 0))

    with pytest.raises(ValueError, match="already exists"):
        machine.add_slot(Slot(1, sample_product, 0))


def test_machine_rejects_invalid_slot_type():
    machine = VendingMachine()

    with pytest.raises(TypeError, match="Slot must be a Slot instance"):
        machine.add_slot("not-a-slot")


def test_machine_rejects_unknown_slot_lookup():
    machine = VendingMachine()

    with pytest.raises(ValueError, match="does not exist"):
        machine.get_slot(5)


def test_machine_can_load_product_and_quantity_into_slot(sample_product):
    machine = VendingMachine()
    slot = Slot(2, None, 0)
    machine.add_slot(slot)

    loaded_slot = machine.load_slot(2, sample_product, 4)

    assert loaded_slot is slot
    assert loaded_slot.product_assigned is sample_product
    assert loaded_slot.quantity_in_place == 4


def test_machine_rejects_invalid_product_type(sample_product):
    machine = VendingMachine()
    machine.add_slot(Slot(3, None, 0))

    with pytest.raises(TypeError, match="Product must be a Product instance"):
        machine.load_slot(3, "not-a-product", 2)


def test_machine_rejects_invalid_quantity(sample_product):
    machine = VendingMachine()
    machine.add_slot(Slot(4, None, 0))

    with pytest.raises(ValueError, match="Quantity must be a non-negative integer"):
        machine.load_slot(4, sample_product, -1)
