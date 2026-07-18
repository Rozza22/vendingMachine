from decimal import Decimal

from .money import InvalidMoney, parse_money


class Product:
    def __init__(self, name: str, sell_price, unit_stock_cost):
        if not isinstance(name, str) or not name.strip():
            raise ValueError("Product name must not be empty")

        self.name = name.strip()
        self.sell_price = self._parse_price(sell_price, "sell price")
        self.unit_stock_cost = self._parse_price(unit_stock_cost, "unit stock cost")

    @staticmethod
    def _parse_price(value, field_name: str) -> Decimal:
        try:
            return parse_money(value)
        except (InvalidMoney, TypeError) as exc:
            raise ValueError(f"Invalid {field_name}: {value!r}") from exc
