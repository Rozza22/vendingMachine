from datetime import datetime
from decimal import Decimal

from vending_machine.product import Product
from vending_machine.slot import Slot
from vending_machine.transactions import transactions


def test_transaction_stores_the_expected_fields():
    product = Product("Soda", "2.00", "0.50")
    slot = Slot(1, product, 3)
    timestamp = datetime(2024, 1, 1, 10, 15, 0)

    record = transactions(timestamp, slot, "2.50", "2.00", "0.50", "0.50")

    assert record.timestamp == timestamp
    assert record.slot is slot
    assert record.paid_amount == Decimal("2.50")
    assert record.sale_price == Decimal("2.00")
    assert record.stock_cost == Decimal("0.50")
    assert record.change_amount == Decimal("0.50")


def test_transaction_can_be_inspected_for_reports():
    product = Product("Soda", "2.00", "0.50")
    slot = Slot(2, product, 1)
    timestamp = datetime(2024, 1, 1, 11, 0, 0)

    record = transactions(timestamp, slot, "2.00", "2.00", "0.50", "0.00")

    report_data = record.to_dict()

    assert report_data["timestamp"] == timestamp
    assert report_data["slot"] is slot
    assert report_data["paid_amount"] == Decimal("2.00")
    assert report_data["sale_price"] == Decimal("2.00")
    assert report_data["stock_cost"] == Decimal("0.50")
    assert report_data["change_amount"] == Decimal("0.00")
