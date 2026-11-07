# Retail Sales Analytics Dashboard

A beginner-friendly academic project demonstrating Python OOP, CSV processing, basic data analysis, Tkinter, and embedded Matplotlib charts.

## Features

- KPI cards for revenue, unique orders, units, and average order value.
- Monthly trend, category, top-product, and regional revenue charts.
- Category and region filters.
- CSV upload with required-column and data validation.
- Synthetic 2025 dataset with 200 line items.

## Setup and run

```powershell
python -m pip install -r requirements.txt
python -m unittest discover -s tests -v
python main.py
```

The application expects `data/retail_sales.csv` by default. Uploaded files must contain
`order_id`, `order_date` (`YYYY-MM-DD`), `product_name`, `category`, `quantity`,
`unit_price`, `region`, and `payment_method`.

## Structure

```text
main.py
data/retail_sales.csv
src/
  csv_data_loader.py
  retail_dashboard.py
  sales_analyzer.py
  sales_record.py
tests/test_sales_analyzer.py
```

`SalesRecord` models one transaction item, `CSVDataLoader` validates and parses rows,
`SalesAnalyzer` performs calculations, and `RetailSalesDashboard` coordinates the GUI.
Revenue is calculated dynamically as `quantity * unit_price`; filters create a new
selection and never alter the original records.

