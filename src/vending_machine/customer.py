from decimal import Decimal

from .money import InvalidMoney, parse_money


class Customer:
    def __init__(self, balance=0):
        self.balance = self._parse_money(balance, "customer balance")

    @staticmethod
    def _parse_money(value, field_name: str) -> Decimal:
        try:
            return parse_money(value)
        except (InvalidMoney, TypeError) as exc:
            raise ValueError(f"Invalid {field_name}: {value!r}") from exc

    def deposit(self, amount) -> None:
        self.balance += self._parse_money(amount, "deposit amount")

    def refund(self) -> Decimal:
        refunded_amount = self.balance
        self.balance = Decimal("0.00")
        return refunded_amount
