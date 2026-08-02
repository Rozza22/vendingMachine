from decimal import Decimal

from vending_machine.metrics import Metrics


def test_metrics_initializes_with_zero_values():
    metrics = Metrics()

    assert metrics.sales_total == Decimal("0.00")
    assert metrics.stock_investment_total == Decimal("0.00")
    assert metrics.cogs_total == Decimal("0.00")
    assert metrics.gross_profit == Decimal("0.00")


def test_metrics_updates_for_sales_and_cogs():
    metrics = Metrics()
    metrics.add_sales("2.50")
    metrics.add_cogs("0.75")

    assert metrics.sales_total == Decimal("2.50")
    assert metrics.cogs_total == Decimal("0.75")
    assert metrics.gross_profit == Decimal("1.75")


def test_metrics_tracks_stock_investment():
    metrics = Metrics()
    metrics.add_stock_investment(3, Decimal("0.50"))

    assert metrics.stock_investment_total == Decimal("1.50")
