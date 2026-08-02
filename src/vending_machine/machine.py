from .money import parse_money
from .product import Product
from .slot import Slot


class VendingMachine:
    MAX_SLOT_NUMBER = 48

    def __init__(self, balance=0):
        self.balance = balance
        self.slots = {}

    def deposit(self, amount):
        amt = parse_money(amount)
        self.balance += amt

    def _validate_place_num(self, place_num: int) -> int:
        if not isinstance(place_num, int):
            raise ValueError("Slot position must be a non-negative integer")
        if place_num < 0:
            raise ValueError("Slot position must be a non-negative integer")
        if place_num > self.MAX_SLOT_NUMBER:
            raise ValueError(f"Slot position cannot exceed {self.MAX_SLOT_NUMBER}")

        return place_num

    def add_slot(self, slot: Slot) -> None:
        if not isinstance(slot, Slot):
            raise TypeError("Slot must be a Slot instance")

        place_num = self._validate_place_num(slot.place_num)
        if place_num in self.slots:
            raise ValueError(f"Slot {place_num} already exists / in-use")

        self.slots[place_num] = slot

    def get_slot(self, place_num: int) -> Slot:
        place_num = self._validate_place_num(place_num)

        if place_num not in self.slots:
            raise ValueError(f"Slot {place_num} does not exist")

        return self.slots[place_num]

    def load_slot(self, place_num: int, product: Product, quantity: int) -> Slot:
        if not isinstance(product, Product):
            raise TypeError("Product must be a Product instance")

        slot = self.get_slot(place_num)

        if quantity < 0 or not isinstance(quantity, int):
            raise ValueError("Quantity must be a non-negative integer")

        if slot.product_assigned is not None and slot.product_assigned != product:
            raise ValueError(f"Slot {place_num} already contains a different product")

        if slot.product_assigned is None:
            slot.product_assigned = product

        slot.add_stock(quantity)
        return slot
