from __future__ import annotations

from typing import Optional

from .customer import Customer
from .machine import VendingMachine
from .product import Product


def create_default_machine() -> VendingMachine:
    return VendingMachine()


class VendingMachineCLI:
    def __init__(
        self,
        machine: Optional[VendingMachine] = None,
        customer: Optional[Customer] = None,
    ):
        self.machine = machine or create_default_machine()
        self.customer = customer or Customer("0.00")

    def display_master_menu(self) -> None:
        print("\nMain Menu")
        print("1. Customer menu")
        print("2. Administrator menu")
        print("3. Exit")

    def display_customer_menu(self) -> None:
        print("\nCustomer Menu")
        print("1. View inventory")
        print("2. Insert money")
        print("3. Purchase")
        print("4. Refund")
        print("5. Back")

    def display_admin_menu(self) -> None:
        print("\nAdministrator Menu")
        print("1. View inventory")
        print("2. Insert money")
        print("3. Purchase")
        print("4. Refund")
        print("5. Restock")
        print("6. Report")
        print("7. Back")

    def handle_master_choice(self, choice: str) -> bool:
        try:
            option = int(choice)
        except ValueError:
            print("Invalid choice. Please enter a number.")
            return True

        if option == 1:
            self.run_customer_menu()
        elif option == 2:
            self.run_admin_menu()
        elif option == 3:
            print("Goodbye!")
            return False
        else:
            print("Invalid choice.")

        return True

    def handle_choice(self, choice: str) -> bool:
        return self.handle_master_choice(choice)

    def handle_customer_choice(self, choice: str) -> bool:
        try:
            option = int(choice)
        except ValueError:
            print("Invalid choice. Please enter a number.")
            return True

        if option == 1:
            self.view_inventory()
        elif option == 2:
            self.insert_money()
        elif option == 3:
            self.purchase()
        elif option == 4:
            self.refund()
        elif option == 5:
            return False
        else:
            print("Invalid choice.")

        return True

    def handle_admin_choice(self, choice: str) -> bool:
        try:
            option = int(choice)
        except ValueError:
            print("Invalid choice. Please enter a number.")
            return True

        if option == 1:
            self.view_inventory()
        elif option == 2:
            self.insert_money()
        elif option == 3:
            self.purchase()
        elif option == 4:
            self.refund()
        elif option == 5:
            self.restock()
        elif option == 6:
            self.report()
        elif option == 7:
            return False
        else:
            print("Invalid choice.")

        return True

    def view_inventory(self) -> None:
        if not self.machine.slots:
            print("No slots registered.")
            return

        for place_num, slot in sorted(self.machine.slots.items()):
            product_name = (
                slot.product_assigned.name
                if slot.product_assigned is not None
                else "Empty"
            )
            print(f"Slot {place_num}: {product_name} | stock: {slot.quantity_in_place}")

    def insert_money(self) -> None:
        try:
            amount = input("Enter amount to insert: ").strip()
            self.customer.deposit(amount)
            print(f"Inserted {amount}. Customer balance: {self.customer.balance}")
        except ValueError as exc:
            print(f"Error: {exc}")

    def purchase(self) -> None:
        try:
            slot_num = int(input("Enter slot number: ").strip())
            transaction = self.machine.purchase(slot_num, self.customer)
            print(
                f"Purchased item from slot {slot_num}. "
                f"Change: {transaction.change_amount}"
            )
        except (ValueError, TypeError) as exc:
            print(f"Error: {exc}")

    def refund(self) -> None:
        refunded = self.customer.refund()
        print(f"Refunded {refunded}. Customer balance: {self.customer.balance}")

    def restock(self) -> None:
        try:
            slot_num = int(input("Enter slot number: ").strip())
            product_name = input("Enter product name: ").strip()
            sell_price = input("Enter sell price: ").strip()
            stock_cost = input("Enter stock cost: ").strip()
            quantity = int(input("Enter quantity: ").strip())

            product = Product(product_name, sell_price, stock_cost)
            self.machine.load_slot(slot_num, product, quantity)
            print(f"Restocked slot {slot_num} with {quantity} units of {product_name}.")
        except (ValueError, TypeError) as exc:
            print(f"Error: {exc}")

    def report(self) -> None:
        print("Sales total:", self.machine.metrics.sales_total)
        print("Stock investment total:", self.machine.metrics.stock_investment_total)
        print("COGS total:", self.machine.metrics.cogs_total)
        print("Gross profit:", self.machine.metrics.gross_profit)

    def run_customer_menu(self) -> None:
        while True:
            self.display_customer_menu()
            choice = input("Choose an option: ").strip()
            if not self.handle_customer_choice(choice):
                break

    def run_admin_menu(self) -> None:
        while True:
            self.display_admin_menu()
            choice = input("Choose an option: ").strip()
            if not self.handle_admin_choice(choice):
                break

    def run(self) -> None:
        while True:
            self.display_master_menu()
            choice = input("Choose an option: ").strip()
            if not self.handle_master_choice(choice):
                break


def main() -> None:
    cli = VendingMachineCLI()
    cli.run()


if __name__ == "__main__":
    main()
