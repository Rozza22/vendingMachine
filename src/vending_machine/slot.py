class Slot:
    MAX_CAPACITY = 10

    def __init__(self, place_num: int, product_assigned, quantity_in_place: int):
        if not isinstance(place_num, int) or place_num < 0:
            raise ValueError("Slot position must be a non-negative integer")
        if not isinstance(quantity_in_place, int) or quantity_in_place <= 0:
            raise ValueError("Quantity in place must be a non-negative integer")
        if product_assigned is None:
            raise ValueError("Product assigned cannot be None")
        if quantity_in_place > self.MAX_CAPACITY:
            raise ValueError("Slot capacity cannot exceed 10")

        self.place_num = place_num
        self.product_assigned = product_assigned
        self.quantity_in_place = quantity_in_place

    def add_stock(self, quantity: int) -> None:
        """Add items to the slot stock."""
        if not isinstance(quantity, int) or quantity < 0:
            raise ValueError("Quantity to add must be a non-negative integer")

        if self.quantity_in_place + quantity > self.MAX_CAPACITY:
            raise ValueError(
                f"Cannot add {quantity} items; slot capacity is {self.MAX_CAPACITY}"
            )

        self.quantity_in_place += quantity

    def remove_stock(self, quantity: int) -> None:
        """Remove items from the slot stock."""
        if not isinstance(quantity, int) or quantity < 0:
            raise ValueError("Quantity to remove must be a non-negative integer")
        if quantity > self.quantity_in_place:
            raise ValueError(
                f"Cannot remove {quantity} items; "
                f"only {self.quantity_in_place} available"
            )
        self.quantity_in_place -= quantity

    def is_in_stock(self) -> bool:
        """Check if there are items in stock."""
        return self.quantity_in_place > 0

    def sell_item(self) -> str:
        """Sell one item to a customer.
        Returns a restock alert if stock reaches zero."""
        if not self.is_in_stock():
            raise ValueError(f"Cannot sell from slot {self.place_num}: out of stock")

        self.quantity_in_place -= 1

        if self.quantity_in_place == 0:
            message = (
                f"⚠️ ALERT: Slot {self.place_num} ({self.product_assigned}) "
                "needs restock - stock is now empty"
            )
            return message

        return ""

    def __repr__(self) -> str:
        message = (
            f"Slot(place_num={self.place_num}, "
            f"product={self.product_assigned}, quantity={self.quantity_in_place})"
        )

        return message
