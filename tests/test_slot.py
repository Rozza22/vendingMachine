import pytest

from vending_machine.product import Product
from vending_machine.slot import Slot


@pytest.fixture
def sample_product():
    """Fixture to create a sample product for testing."""
    return Product("Soda", "1.50", "0.50")


@pytest.fixture
def sample_slot(sample_product):
    """Fixture to create a sample slot for testing."""
    return Slot(place_num=1, product_assigned=sample_product, quantity_in_place=10)


# ==================== Initialization Tests ====================


def test_slot_creation(sample_slot, sample_product):
    """Test valid slot creation."""
    assert sample_slot.place_num == 1
    assert sample_slot.product_assigned == sample_product
    assert sample_slot.quantity_in_place == 10


def test_slot_creation_with_string_product():
    """Test slot creation with a string product name."""
    slot = Slot(place_num=0, product_assigned="Chips", quantity_in_place=5)
    assert slot.place_num == 0
    assert slot.product_assigned == "Chips"
    assert slot.quantity_in_place == 5


def test_slot_creation_exceeds_capacity(sample_product):
    """Test that a slot cannot be created above its capacity."""
    with pytest.raises(ValueError, match="Slot capacity cannot exceed 10"):
        Slot(place_num=1, product_assigned=sample_product, quantity_in_place=11)


@pytest.mark.parametrize("bad_place_num", [-1, -100])
def test_slot_invalid_place_num(bad_place_num, sample_product):
    """Test that invalid place_num values are rejected."""
    with pytest.raises(
        ValueError, match="Slot position must be a non-negative integer"
    ):
        Slot(
            place_num=bad_place_num,
            product_assigned=sample_product,
            quantity_in_place=10,
        )


@pytest.mark.parametrize("bad_place_num", [1.5, "1", None])
def test_slot_invalid_place_num_type(bad_place_num, sample_product):
    """Test that non-integer place_num types are rejected."""
    with pytest.raises(ValueError):
        Slot(
            place_num=bad_place_num,
            product_assigned=sample_product,
            quantity_in_place=10,
        )


@pytest.mark.parametrize("bad_quantity", [-1, -100])
def test_slot_invalid_quantity(bad_quantity, sample_product):
    """Test that invalid quantity values are rejected."""
    with pytest.raises(
        ValueError, match="Quantity in place must be a non-negative integer"
    ):
        Slot(
            place_num=1, product_assigned=sample_product, quantity_in_place=bad_quantity
        )


@pytest.mark.parametrize("bad_quantity", [1.5, "10", None])
def test_slot_invalid_quantity_type(bad_quantity, sample_product):
    """Test that non-integer quantity types are rejected."""
    with pytest.raises(ValueError):
        Slot(
            place_num=1, product_assigned=sample_product, quantity_in_place=bad_quantity
        )


def test_slot_none_product():
    """Test that None product is rejected."""
    with pytest.raises(ValueError, match="Product assigned cannot be None"):
        Slot(place_num=1, product_assigned=None, quantity_in_place=10)


# ==================== add_stock Tests ====================


def test_add_stock_valid(sample_slot):
    """Test adding stock successfully."""
    sample_slot.quantity_in_place = 5
    sample_slot.add_stock(5)
    assert sample_slot.quantity_in_place == 10


def test_add_stock_zero(sample_slot):
    """Test adding zero stock."""
    sample_slot.add_stock(0)
    assert sample_slot.quantity_in_place == 10


def test_add_stock_to_full_capacity(sample_slot):
    """Test adding stock up to the slot limit."""
    sample_slot.quantity_in_place = 5
    sample_slot.add_stock(5)
    assert sample_slot.quantity_in_place == 10


def test_add_stock_exceeds_capacity(sample_slot):
    """Test that adding beyond the slot limit is rejected."""
    sample_slot.quantity_in_place = 9
    with pytest.raises(ValueError, match="Cannot add 2 items; slot capacity is 10"):
        sample_slot.add_stock(2)


@pytest.mark.parametrize("bad_quantity", [-1, -50])
def test_add_stock_negative(bad_quantity, sample_slot):
    """Test that negative stock additions are rejected."""
    with pytest.raises(
        ValueError, match="Quantity to add must be a non-negative integer"
    ):
        sample_slot.add_stock(bad_quantity)


@pytest.mark.parametrize("bad_quantity", [1.5, "5", None])
def test_add_stock_invalid_type(bad_quantity, sample_slot):
    """Test that non-integer quantities are rejected."""
    with pytest.raises(ValueError):
        sample_slot.add_stock(bad_quantity)


# ==================== remove_stock Tests ====================


def test_remove_stock_valid(sample_slot):
    """Test removing stock successfully."""
    sample_slot.remove_stock(3)
    assert sample_slot.quantity_in_place == 7


def test_remove_stock_all(sample_slot):
    """Test removing all stock."""
    sample_slot.remove_stock(10)
    assert sample_slot.quantity_in_place == 0


def test_remove_stock_zero(sample_slot):
    """Test removing zero stock."""
    sample_slot.remove_stock(0)
    assert sample_slot.quantity_in_place == 10


def test_remove_stock_exceeds_available(sample_slot):
    """Test that removing more than available is rejected."""
    with pytest.raises(ValueError, match="Cannot remove 15 items; only 10 available"):
        sample_slot.remove_stock(15)


@pytest.mark.parametrize("bad_quantity", [-1, -50])
def test_remove_stock_negative(bad_quantity, sample_slot):
    """Test that negative stock removals are rejected."""
    with pytest.raises(
        ValueError, match="Quantity to remove must be a non-negative integer"
    ):
        sample_slot.remove_stock(bad_quantity)


@pytest.mark.parametrize("bad_quantity", [1.5, "5", None])
def test_remove_stock_invalid_type(bad_quantity, sample_slot):
    """Test that non-integer quantities are rejected."""
    with pytest.raises(ValueError):
        sample_slot.remove_stock(bad_quantity)


# ==================== is_in_stock Tests ====================


def test_is_in_stock_true(sample_slot):
    """Test is_in_stock returns True when items are available."""
    assert sample_slot.is_in_stock() is True


def test_is_in_stock_false(sample_slot):
    """Test is_in_stock returns False when stock is zero."""
    sample_slot.quantity_in_place = 0
    assert sample_slot.is_in_stock() is False


def test_is_in_stock_one_item(sample_slot):
    """Test is_in_stock returns True with exactly one item."""
    sample_slot.quantity_in_place = 1
    assert sample_slot.is_in_stock() is True


# ==================== sell_item Tests ====================


def test_sell_item_valid(sample_slot):
    """Test selling one item successfully."""
    alert = sample_slot.sell_item()
    assert sample_slot.quantity_in_place == 9
    assert alert == ""


def test_sell_item_triggers_restock_alert(sample_slot):
    """Test that selling the last item triggers a restock alert."""
    sample_slot.quantity_in_place = 1
    alert = sample_slot.sell_item()
    assert sample_slot.quantity_in_place == 0
    assert "ALERT" in alert
    assert "needs restock" in alert
    assert "Slot 1" in alert


def test_sell_item_multiple_sales(sample_slot):
    """Test selling multiple items in sequence."""
    for i in range(9):
        alert = sample_slot.sell_item()
        assert alert == ""

    # Last sale should trigger alert
    alert = sample_slot.sell_item()
    assert sample_slot.quantity_in_place == 0
    assert "ALERT" in alert


def test_sell_item_out_of_stock(sample_slot):
    """Test that selling from empty stock raises an error."""
    sample_slot.quantity_in_place = 0
    with pytest.raises(ValueError, match="Cannot sell from slot 1: out of stock"):
        sample_slot.sell_item()


def test_sell_item_exact_alert_message():
    """Test the exact restock alert message format with string product."""
    slot = Slot(place_num=1, product_assigned="Soda", quantity_in_place=1)
    alert = slot.sell_item()
    assert alert == "⚠️ ALERT: Slot 1 (Soda) needs restock - stock is now empty"


def test_sell_item_with_string_product():
    """Test selling from a slot with string product."""
    slot = Slot(place_num=5, product_assigned="Candy", quantity_in_place=1)
    alert = slot.sell_item()
    assert "Slot 5" in alert
    assert "Candy" in alert


# ==================== repr Tests ====================


def test_repr_full_stock(sample_slot):
    """Test string representation with full stock."""
    repr_str = repr(sample_slot)
    assert "place_num=1" in repr_str
    assert "quantity=10" in repr_str
    assert "Slot" in repr_str


def test_repr_empty_stock(sample_slot):
    """Test string representation with empty stock."""
    sample_slot.quantity_in_place = 0
    repr_str = repr(sample_slot)
    assert "quantity=0" in repr_str


# ==================== Integration Tests ====================


def test_slot_workflow_restock_and_sell(sample_slot):
    """Test a complete workflow of restocking and selling."""
    # Start with 10 items
    assert sample_slot.quantity_in_place == 10

    # Sell 9 items
    for _ in range(9):
        alert = sample_slot.sell_item()
        assert alert == ""

    assert sample_slot.quantity_in_place == 1

    # Restock to a valid capacity below the slot limit
    sample_slot.add_stock(5)
    assert sample_slot.quantity_in_place == 6

    # Sell until empty and check for alert
    for _ in range(5):
        alert = sample_slot.sell_item()
        assert alert == ""

    # Last sale triggers alert
    alert = sample_slot.sell_item()
    assert "ALERT" in alert
    assert sample_slot.quantity_in_place == 0


def test_slot_cannot_sell_after_manual_empty(sample_slot):
    """Test that removing all stock prevents further sales."""
    sample_slot.remove_stock(10)
    assert sample_slot.quantity_in_place == 0

    with pytest.raises(ValueError, match="out of stock"):
        sample_slot.sell_item()
