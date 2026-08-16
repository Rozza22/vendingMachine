import csv

from .product import Product


def load_machine_from_csv(filename, machine):
    with open(filename, newline="") as file:
        reader = csv.DictReader(file)

        for row in reader:
            product = Product(
                row["product"],
                row["sell_price"],
                row["unit_stock_cost"],
            )

            machine.load_slot(
                int(row["slot"]),
                product,
                int(row["quantity"]),
            )
