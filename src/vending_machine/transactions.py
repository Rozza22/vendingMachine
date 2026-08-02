from datetime import datetime
from decimal import Decimal

from .money import InvalidMoney, parse_money


class transactions:
    def __init__(
        self,
        transaction_time,
        slot,
        paid_amount,
        sale_amount,
        stock_cost,
        change_amount,
    ):
        if not isinstance(transaction_time, datetime):
            raise ValueError("Transaction time must be a datetime")
        if slot is None:
            raise ValueError("Slot cannot be None")

        self.timestamp = transaction_time
        self.slot = slot
        self.paid_amount = self._parse_money(paid_amount, "paid amount")
        self.sale_price = self._parse_money(sale_amount, "sale price")
        self.stock_cost = self._parse_money(stock_cost, "stock cost")
        self.change_amount = self._parse_money(change_amount, "change amount")

    @staticmethod
    def _parse_money(value, field_name: str) -> Decimal:
        try:
            return parse_money(value)
        except (InvalidMoney, TypeError) as exc:
            raise ValueError(f"Invalid {field_name}: {value!r}") from exc

    # good for saving properties of a sale to a database
    def to_dict(self) -> dict:
        return {
            "timestamp": self.timestamp,
            "slot": self.slot,
            "paid_amount": self.paid_amount,
            "sale_price": self.sale_price,
            "stock_cost": self.stock_cost,
            "change_amount": self.change_amount,
        }
