"""Tkinter and Matplotlib user interface."""

import tkinter as tk
from pathlib import Path
from tkinter import filedialog, messagebox, ttk

from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure

from .csv_data_loader import CSVDataLoader
from .sales_analyzer import SalesAnalyzer
from .sales_record import SalesRecord


class RetailSalesDashboard:
    """Display metrics and charts for a collection of sales records."""

    COLORS = {"navy": "#16324F", "blue": "#2878B5", "teal": "#2A9D8F", "gold": "#E9C46A"}

    def __init__(self, records: list[SalesRecord], source_path: Path) -> None:
        self.records = records
        self.source_path = source_path
        self.analyzer = SalesAnalyzer(records)
        self.root = tk.Tk()
        self.root.title("Retail Sales Analytics Dashboard")
        self.root.geometry("1280x820")
        self.root.minsize(980, 650)
        self.root.configure(bg="#F4F7FB")
        self.category_var = tk.StringVar(value="All Categories")
        self.region_var = tk.StringVar(value="All Regions")
        self.status_var = tk.StringVar()
        self.kpi_values: dict[str, tk.StringVar] = {}
        self._build_layout()
        self.refresh()

    def _build_layout(self) -> None:
        sidebar = tk.Frame(self.root, bg=self.COLORS["navy"], width=230)
        sidebar.pack(side="left", fill="y")
        sidebar.pack_propagate(False)
        tk.Label(
            sidebar,
            text="RETAIL SALES\nANALYTICS",
            font=("Segoe UI", 18, "bold"),
            fg="white",
            bg=self.COLORS["navy"],
            justify="left",
        ).pack(anchor="w", padx=24, pady=(30, 45))
        tk.Label(sidebar, text="FILTERS", font=("Segoe UI", 10, "bold"), fg="#AFC6DB",
                 bg=self.COLORS["navy"]).pack(anchor="w", padx=24, pady=(0, 8))
        self._sidebar_combo(sidebar, "Product category", self.category_var,
                            ["All Categories", "Electronics", "Clothing", "Grocery", "Home & Kitchen", "Sports"])
        self._sidebar_combo(sidebar, "Region", self.region_var,
                            ["All Regions", "North", "South", "East", "West"])
        tk.Button(sidebar, text="Apply Filters", command=self.refresh, bg=self.COLORS["teal"],
                  fg="white", relief="flat", font=("Segoe UI", 10, "bold"), padx=8, pady=8).pack(
            fill="x", padx=24, pady=(22, 8))
        tk.Button(sidebar, text="Reset Filters", command=self.reset_filters, bg="#31516E",
                  fg="white", relief="flat", font=("Segoe UI", 10), padx=8, pady=8).pack(
            fill="x", padx=24)
        tk.Button(sidebar, text="Upload CSV", command=self.upload_csv, bg="#31516E",
                  fg="white", relief="flat", font=("Segoe UI", 10), padx=8, pady=8).pack(
            fill="x", padx=24, pady=8)
        tk.Label(sidebar, textvariable=self.status_var, wraplength=180, justify="left",
                 fg="#D5E4F0", bg=self.COLORS["navy"], font=("Segoe UI", 9)).pack(
            side="bottom", anchor="w", padx=24, pady=25)

        content = tk.Frame(self.root, bg="#F4F7FB")
        content.pack(side="left", fill="both", expand=True, padx=25, pady=22)
        tk.Label(content, text="Retail Sales Analytics Dashboard", font=("Segoe UI", 23, "bold"),
                 fg=self.COLORS["navy"], bg="#F4F7FB").pack(anchor="w")
        tk.Label(content, text="Monitor revenue, orders, products, and regional performance",
                 font=("Segoe UI", 10), fg="#617589", bg="#F4F7FB").pack(anchor="w", pady=(2, 18))
        self.kpi_frame = tk.Frame(content, bg="#F4F7FB")
        self.kpi_frame.pack(fill="x", pady=(0, 18))
        for title in ("Total Revenue", "Total Orders", "Total Units Sold", "Average Order Value"):
            card = tk.Frame(self.kpi_frame, bg="white", highlightthickness=1,
                            highlightbackground="#E2E8F0")
            card.pack(side="left", fill="both", expand=True, padx=(0, 12))
            tk.Label(card, text=title.upper(), font=("Segoe UI", 9, "bold"), fg="#718096",
                     bg="white").pack(anchor="w", padx=16, pady=(14, 3))
            value = tk.StringVar(value="-")
            self.kpi_values[title] = value
            tk.Label(card, textvariable=value, font=("Segoe UI", 17, "bold"),
                     fg=self.COLORS["navy"], bg="white").pack(anchor="w", padx=16, pady=(0, 14))
        self.figure = Figure(figsize=(10, 6), dpi=100, facecolor="#F4F7FB")
        self.canvas = FigureCanvasTkAgg(self.figure, master=content)
        self.canvas.get_tk_widget().pack(fill="both", expand=True)

    @staticmethod
    def _sidebar_combo(parent, label, variable, values) -> None:
        tk.Label(parent, text=label, fg="#D5E4F0", bg=parent["bg"],
                 font=("Segoe UI", 9)).pack(anchor="w", padx=24, pady=(12, 4))
        ttk.Combobox(parent, textvariable=variable, values=values, state="readonly").pack(
            fill="x", padx=24)

    def refresh(self) -> None:
        selected = self.analyzer.filtered(self.category_var.get(), self.region_var.get())
        metrics = self.analyzer.metrics(selected)
        self.kpi_values["Total Revenue"].set(f"₹{metrics['total_revenue']:,.2f}")
        self.kpi_values["Total Orders"].set(f"{metrics['total_orders']:,}")
        self.kpi_values["Total Units Sold"].set(f"{metrics['total_units']:,}")
        self.kpi_values["Average Order Value"].set(f"₹{metrics['average_order_value']:,.2f}")
        self.status_var.set(f"{len(selected)} line items shown\nSource: {self.source_path.name}")
        self._draw_charts(selected)

    def _draw_charts(self, records: list[SalesRecord]) -> None:
        self.figure.clear()
        axes = self.figure.subplots(2, 2)
        axes = axes.flatten()
        monthly = self.analyzer.monthly_revenue(records)
        axes[0].plot(range(1, 13), list(monthly.values()), marker="o", color=self.COLORS["blue"])
        axes[0].set_title("Monthly Sales Trend", loc="left", fontweight="bold")
        axes[0].set_xlabel("Month"); axes[0].set_ylabel("Revenue (₹)")
        axes[0].set_xticks(range(1, 13)); axes[0].grid(alpha=0.25)
        category = self.analyzer.revenue_by_category(records)
        axes[1].bar(category.keys(), category.values(), color=self.COLORS["teal"])
        axes[1].set_title("Sales by Category", loc="left", fontweight="bold")
        axes[1].set_ylabel("Revenue (₹)"); axes[1].tick_params(axis="x", rotation=25)
        products = self.analyzer.top_products(records)
        products.reverse()
        axes[2].barh([name for name, _ in products], [value for _, value in products], color=self.COLORS["gold"])
        axes[2].set_title("Top 5 Best-Selling Products", loc="left", fontweight="bold")
        axes[2].set_xlabel("Revenue (₹)")
        regions = self.analyzer.revenue_by_region(records)
        if regions:
            axes[3].pie(regions.values(), labels=regions.keys(), autopct="%1.1f%%",
                       startangle=90, colors=["#2878B5", "#2A9D8F", "#E9C46A", "#E76F51"])
        axes[3].set_title("Sales by Region", loc="left", fontweight="bold")
        if not records:
            for axis in axes:
                axis.text(0.5, 0.5, "No data for these filters", ha="center", va="center",
                          transform=axis.transAxes, color="#718096")
                axis.set_xticks([]); axis.set_yticks([])
        self.figure.tight_layout()
        self.canvas.draw()

    def reset_filters(self) -> None:
        self.category_var.set("All Categories")
        self.region_var.set("All Regions")
        self.refresh()

    def upload_csv(self) -> None:
        path = filedialog.askopenfilename(filetypes=[("CSV files", "*.csv"), ("All files", "*.*")])
        if not path:
            return
        try:
            records = CSVDataLoader().load(path)
        except (FileNotFoundError, ValueError) as error:
            messagebox.showerror("Could not load CSV", str(error))
            return
        self.records = records
        self.source_path = Path(path)
        self.analyzer = SalesAnalyzer(records)
        self.reset_filters()

    def run(self) -> None:
        self.root.mainloop()

