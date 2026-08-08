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


def test_cli_inventory_report_shows_correct_details(monkeypatch, capsys):
    cli = VendingMachineCLI(machine=VendingMachine(), customer=Customer("0.00"))

    inputs = iter(
        [
            "1",
            "Lucky Strike",
            "20",
            "5",
            "9",
            "2",
            "Twix",
            "2",
            "0.5",
            "5",
            "7",  # select Full Inventory Report in admin menu
            "8",  # leave admin menu
        ]
    )

    monkeypatch.setattr("builtins.input", lambda _: next(inputs))

    cli.restock()
    cli.restock()

    cli.handle_choice("2")  # enter admin menu

    output = capsys.readouterr().out

    assert "Inventory Report" in output
    assert "Lucky Strike" in output
    assert "20.00" in output
    assert "5.00" in output
    assert "Twix" in output
    assert "Quantity" in output


def test_cli_finance_report_shows_correct_values(capsys):
    """Finance report should show sales,
    stock investment, COGS, gross profit, and transaction count."""
    machine = VendingMachine()
    customer = Customer("10.00")
    cli = VendingMachineCLI(machine=machine, customer=customer)

    # Set up products in slots
    product1 = Product("Soda", "2.50", "0.75")
    product2 = Product("Chips", "1.50", "0.40")
    machine.load_slot(1, product1, 3)
    machine.load_slot(2, product2, 5)

    # Verify stock investment before purchases
    # Stock investment = (3 * $0.75) + (5 * $0.40) = $2.25 + $2.00 = $4.25
    assert machine.metrics.stock_investment_total == Decimal("4.25")

    # Make purchases
    machine.purchase(1, customer)  # Sale: $2.50, COGS: $0.75
    machine.purchase(2, customer)  # Sale: $1.50, COGS: $0.40

    # Verify metrics before report
    assert machine.metrics.sales_total == Decimal("4.00")
    assert machine.metrics.cogs_total == Decimal("1.15")
    assert machine.metrics.gross_profit == Decimal("2.85")
    assert len(machine.transactions_history) == 2

    # Call finance report
    cli.report()

    output = capsys.readouterr().out

    # Verify all required finance report elements are present and correct
    assert "Sales total" in output
    assert "4.00" in output

    assert "Stock investment total" in output
    assert "4.25" in output

    assert "COGS total" in output
    assert "1.15" in output

    assert "Gross profit" in output
    assert "2.85" in output

    # Transaction count should be displayed
    assert "2" in output
