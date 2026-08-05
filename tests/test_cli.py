from decimal import Decimal

from vending_machine.cli import VendingMachineCLI
from vending_machine.customer import Customer
from vending_machine.machine import VendingMachine
from vending_machine.product import Product
from vending_machine.slot import Slot


def test_cli_rejects_invalid_menu_choice(capsys):
    cli = VendingMachineCLI(machine=VendingMachine(), customer=Customer("0.00"))

    assert cli.handle_choice("9") is True

    output = capsys.readouterr().out
    assert "Invalid choice" in output


def test_cli_can_show_inventory_for_registered_slots(capsys):
    machine = VendingMachine()
    machine.add_slot(Slot(1, Product("Soda", "1.50", "0.50"), 2))
    cli = VendingMachineCLI(machine=machine, customer=Customer("0.00"))

    cli.view_inventory()

    output = capsys.readouterr().out
    assert "Slot 1" in output
    assert "Soda" in output
    assert "(2)" in output


def test_cli_restock_creates_product_and_allows_purchase(monkeypatch):
    cli = VendingMachineCLI(machine=VendingMachine(), customer=Customer("2.00"))
    inputs = iter(["1", "Soda", "1.50", "0.50", "2", "1"])
    monkeypatch.setattr("builtins.input", lambda _: next(inputs))

    cli.restock()
    cli.purchase()

    slot = cli.machine.get_slot(1)
    assert slot.product_assigned.name == "Soda"
    assert slot.quantity_in_place == 1
    assert cli.customer.balance == Decimal("0.50")
