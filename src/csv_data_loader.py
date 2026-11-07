"""CSV loading and validation."""

import csv
from datetime import datetime
from pathlib import Path

from .sales_record import SalesRecord


class CSVDataLoader:
    """Convert validated CSV rows into SalesRecord objects."""

    REQUIRED_COLUMNS = {
        "order_id",
        "order_date",
        "product_name",
        "category",
        "quantity",
        "unit_price",
        "region",
        "payment_method",
    }

    def load(self, file_path: str | Path) -> list[SalesRecord]:
        """Load records, raising a useful ValueError for invalid input."""
        path = Path(file_path)
        if not path.is_file():
            raise FileNotFoundError(f"CSV file not found: {path}")

        try:
            with path.open("r", newline="", encoding="utf-8-sig") as file:
                reader = csv.DictReader(file)
                columns = set(reader.fieldnames or [])
                missing = self.REQUIRED_COLUMNS - columns
                if missing:
                    names = ", ".join(sorted(missing))
                    raise ValueError(f"Missing required column(s): {names}")

                records: list[SalesRecord] = []
                for line_number, row in enumerate(reader, start=2):
                    try:
                        order_id = (row["order_id"] or "").strip()
                        product_name = (row["product_name"] or "").strip()
                        category = (row["category"] or "").strip()
                        region = (row["region"] or "").strip()
                        payment_method = (row["payment_method"] or "").strip()
                        if not all((order_id, product_name, category, region, payment_method)):
                            raise ValueError("text fields cannot be empty")

                        order_date = datetime.strptime(
                            row["order_date"].strip(), "%Y-%m-%d"
                        ).date()
                        quantity = int(row["quantity"])
                        unit_price = float(row["unit_price"])
                        if quantity <= 0 or unit_price < 0:
                            raise ValueError("quantity must be positive and price non-negative")
                    except (AttributeError, TypeError, ValueError) as error:
                        raise ValueError(
                            f"Invalid data on CSV line {line_number}: {error}"
                        ) from error

                    records.append(
                        SalesRecord(
                            order_id,
                            order_date,
                            product_name,
                            category,
                            quantity,
                            unit_price,
                            region,
                            payment_method,
                        )
                    )
        except UnicodeDecodeError as error:
            raise ValueError("The CSV file must use UTF-8 encoding.") from error
        except csv.Error as error:
            raise ValueError(f"Could not parse CSV file: {error}") from error

        if not records:
            raise ValueError("The CSV file contains no data rows.")
        return records

