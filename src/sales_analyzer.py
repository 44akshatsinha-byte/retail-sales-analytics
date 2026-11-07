"""Analysis operations for retail sales records."""

from collections import defaultdict
from typing import Iterable

from .sales_record import SalesRecord


class SalesAnalyzer:
    """Calculate dashboard metrics without depending on the GUI."""

    def __init__(self, records: Iterable[SalesRecord] = ()) -> None:
        self.records = list(records)

    def filtered(
        self, category: str = "All Categories", region: str = "All Regions"
    ) -> list[SalesRecord]:
        """Return a new list matching the selected filters."""
        return [
            record
            for record in self.records
            if (category == "All Categories" or record.category == category)
            and (region == "All Regions" or record.region == region)
        ]

    @staticmethod
    def total_revenue(records: Iterable[SalesRecord]) -> float:
        return sum(record.revenue() for record in records)

    @staticmethod
    def total_orders(records: Iterable[SalesRecord]) -> int:
        return len({record.order_id for record in records})

    @staticmethod
    def total_units(records: Iterable[SalesRecord]) -> int:
        return sum(record.quantity for record in records)

    def metrics(self, records: Iterable[SalesRecord] | None = None) -> dict[str, float | int]:
        selected = list(self.records if records is None else records)
        revenue = self.total_revenue(selected)
        orders = self.total_orders(selected)
        return {
            "total_revenue": revenue,
            "total_orders": orders,
            "total_units": self.total_units(selected),
            "average_order_value": revenue / orders if orders else 0.0,
        }

    def monthly_revenue(
        self, records: Iterable[SalesRecord] | None = None
    ) -> dict[int, float]:
        selected = self.records if records is None else records
        totals = {month: 0.0 for month in range(1, 13)}
        for record in selected:
            totals[record.order_date.month] += record.revenue()
        return totals

    def revenue_by_category(
        self, records: Iterable[SalesRecord] | None = None
    ) -> dict[str, float]:
        selected = self.records if records is None else records
        return self._group_revenue(selected, lambda record: record.category)

    def top_products(
        self, records: Iterable[SalesRecord] | None = None, limit: int = 5
    ) -> list[tuple[str, float]]:
        selected = self.records if records is None else records
        totals = self._group_revenue(selected, lambda record: record.product_name)
        return sorted(totals.items(), key=lambda item: item[1], reverse=True)[:limit]

    def revenue_by_region(
        self, records: Iterable[SalesRecord] | None = None
    ) -> dict[str, float]:
        selected = self.records if records is None else records
        return self._group_revenue(selected, lambda record: record.region)

    @staticmethod
    def _group_revenue(records: Iterable[SalesRecord], key_function) -> dict[str, float]:
        totals: defaultdict[str, float] = defaultdict(float)
        for record in records:
            totals[key_function(record)] += record.revenue()
        return dict(sorted(totals.items()))
