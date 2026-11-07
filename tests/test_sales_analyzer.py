import unittest
from datetime import date

from src.sales_analyzer import SalesAnalyzer
from src.sales_record import SalesRecord


class SalesAnalyzerTests(unittest.TestCase):
    def setUp(self):
        self.records = [
            SalesRecord("A", date(2025, 1, 2), "Laptop", "Electronics", 1, 1000, "North", "UPI"),
            SalesRecord("A", date(2025, 1, 2), "Mouse", "Electronics", 2, 25, "North", "UPI"),
            SalesRecord("B", date(2025, 2, 3), "Shirt", "Clothing", 3, 40, "South", "Cash"),
        ]
        self.analyzer = SalesAnalyzer(self.records)

    def test_metrics_use_unique_orders(self):
        self.assertEqual(self.analyzer.metrics(), {
            "total_revenue": 1170,
            "total_orders": 2,
            "total_units": 6,
            "average_order_value": 585,
        })

    def test_grouped_and_top_product_revenue(self):
        self.assertEqual(self.analyzer.revenue_by_category()["Electronics"], 1050)
        self.assertEqual(self.analyzer.top_products()[0], ("Laptop", 1000))

    def test_filters_do_not_modify_source_data(self):
        selected = self.analyzer.filtered(category="Clothing")
        self.assertEqual(len(selected), 1)
        self.assertEqual(len(self.analyzer.records), 3)


if __name__ == "__main__":
    unittest.main()

