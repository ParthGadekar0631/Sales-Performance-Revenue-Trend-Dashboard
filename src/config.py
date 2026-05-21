"""Central configuration for the sales analytics pipeline."""

from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[1]

DATA_DIR = PROJECT_ROOT / "data"
RAW_DIR = DATA_DIR / "raw"
PROCESSED_DIR = DATA_DIR / "processed"
SAMPLE_DIR = DATA_DIR / "sample"
DATABASE_DIR = PROJECT_ROOT / "database"
REPORTS_DIR = PROJECT_ROOT / "reports"

RAW_SALES_FILE = RAW_DIR / "sales_transactions.csv"
SAMPLE_SALES_FILE = SAMPLE_DIR / "sample_sales_transactions.csv"
DATABASE_FILE = DATABASE_DIR / "sales_dashboard.db"

SYNTHETIC_ROW_COUNT = 50000
SAMPLE_ROW_COUNT = 1000
RANDOM_SEED = 42

REQUIRED_COLUMNS = [
    "transaction_id",
    "transaction_date",
    "customer_id",
    "product_id",
    "product_name",
    "category",
    "quantity",
    "unit_price",
    "discount",
    "region",
    "sales_channel",
    "payment_method",
]

NUMERIC_COLUMNS = ["quantity", "unit_price", "discount"]

PROCESSED_FILES = {
    "cleaned_sales": PROCESSED_DIR / "cleaned_sales.csv",
    "monthly_revenue_summary": PROCESSED_DIR / "monthly_revenue_summary.csv",
    "product_performance": PROCESSED_DIR / "product_performance.csv",
    "category_performance": PROCESSED_DIR / "category_performance.csv",
    "regional_performance": PROCESSED_DIR / "regional_performance.csv",
    "sales_channel_performance": PROCESSED_DIR / "sales_channel_performance.csv",
    "dashboard_kpis": PROCESSED_DIR / "dashboard_kpis.csv",
}

DIRECTORIES = [
    RAW_DIR,
    PROCESSED_DIR,
    SAMPLE_DIR,
    DATABASE_DIR,
    REPORTS_DIR,
]

START_DATE = "2022-01-01"
END_DATE = "2025-12-31"

