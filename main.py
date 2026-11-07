"""Application entry point for the retail sales dashboard."""

from pathlib import Path

from src.csv_data_loader import CSVDataLoader
from src.retail_dashboard import RetailSalesDashboard


def main() -> None:
    data_file = Path(__file__).parent / "data" / "retail_sales.csv"
    records = CSVDataLoader().load(data_file)
    RetailSalesDashboard(records, data_file).run()


if __name__ == "__main__":
    main()

