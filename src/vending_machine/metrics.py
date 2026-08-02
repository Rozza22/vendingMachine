from decimal import Decimal

from .money import parse_money


class Metrics:
    def __init__(self, sales_total=0, stock_investment_total=0, cogs_total=0):
        self.sales_total = self._parse_money(sales_total, "sales total")
        self.stock_investment_total = self._parse_money(
            stock_investment_total, "stock investment total"
        )
        self.cogs_total = self._parse_money(cogs_total, "COGS total")

    @staticmethod
    def _parse_money(value, field_name: str) -> Decimal:
        try:
            return parse_money(value)
        except (TypeError, ValueError) as exc:
            raise ValueError(f"Invalid {field_name}: {value!r}") from exc

    @property
    def gross_profit(self) -> Decimal:
        return self.sales_total - self.cogs_total

    def add_sales(self, amount) -> None:
        self.sales_total += self._parse_money(amount, "sales amount")

    def add_stock_investment(self, quantity, unit_cost) -> None:
        self.stock_investment_total += (
            self._parse_money(quantity, "stock quantity") * unit_cost
        )

    def add_cogs(self, amount) -> None:
        self.cogs_total += self._parse_money(amount, "COGS amount")
