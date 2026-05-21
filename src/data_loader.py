"""Raw sales data loading and synthetic dataset generation."""

from __future__ import annotations

from dataclasses import dataclass

import numpy as np
import pandas as pd

try:
    from .config import (
        DIRECTORIES,
        END_DATE,
        RANDOM_SEED,
        RAW_SALES_FILE,
        SAMPLE_ROW_COUNT,
        SAMPLE_SALES_FILE,
        START_DATE,
        SYNTHETIC_ROW_COUNT,
    )
    from .logger import get_logger
    from .validation import validate_non_empty, validate_required_columns
except ImportError:  # pragma: no cover
    from config import (
        DIRECTORIES,
        END_DATE,
        RANDOM_SEED,
        RAW_SALES_FILE,
        SAMPLE_ROW_COUNT,
        SAMPLE_SALES_FILE,
        START_DATE,
        SYNTHETIC_ROW_COUNT,
    )
    from logger import get_logger
    from validation import validate_non_empty, validate_required_columns


logger = get_logger(__name__)


@dataclass(frozen=True)
class Product:
    product_id: str
    product_name: str
    category: str
    base_price: float


PRODUCT_CATALOG = [
    Product("P1001", "Laptop Pro 14", "Electronics", 1299.00),
    Product("P1002", "Wireless Headphones", "Electronics", 149.00),
    Product("P1003", "Smartphone Max", "Electronics", 899.00),
    Product("P1004", "4K Monitor", "Electronics", 349.00),
    Product("P2001", "Office Chair", "Furniture", 229.00),
    Product("P2002", "Standing Desk", "Furniture", 599.00),
    Product("P2003", "Bookshelf", "Furniture", 179.00),
    Product("P3001", "Coffee Maker", "Home & Kitchen", 119.00),
    Product("P3002", "Air Fryer", "Home & Kitchen", 139.00),
    Product("P3003", "Cookware Set", "Home & Kitchen", 249.00),
    Product("P4001", "Running Shoes", "Apparel", 129.00),
    Product("P4002", "Performance Jacket", "Apparel", 189.00),
    Product("P4003", "Travel Backpack", "Apparel", 99.00),
    Product("P5001", "Project Management Suite", "Software", 39.00),
    Product("P5002", "Analytics Platform License", "Software", 249.00),
    Product("P5003", "Security Monitoring Plan", "Software", 159.00),
    Product("P6001", "Commercial Printer", "Office Supplies", 449.00),
    Product("P6002", "Desk Organizer Set", "Office Supplies", 35.00),
]


def ensure_directories() -> None:
    """Create the project output directories if they do not exist."""
    for directory in DIRECTORIES:
        directory.mkdir(parents=True, exist_ok=True)


def generate_synthetic_sales_data(row_count: int = SYNTHETIC_ROW_COUNT) -> pd.DataFrame:
    """Generate realistic synthetic sales transactions for portfolio analysis."""
    rng = np.random.default_rng(RANDOM_SEED)
    catalog_df = pd.DataFrame([product.__dict__ for product in PRODUCT_CATALOG])

    product_weights = np.array(
        [0.08, 0.07, 0.08, 0.06, 0.06, 0.05, 0.04, 0.06, 0.06, 0.05, 0.07, 0.05, 0.06, 0.07, 0.08, 0.06, 0.03, 0.02]
    )
    product_weights = product_weights / product_weights.sum()
    product_indices = rng.choice(catalog_df.index, size=row_count, p=product_weights)
    products = catalog_df.loc[product_indices].reset_index(drop=True)

    dates = pd.date_range(START_DATE, END_DATE, freq="D")
    month_weights = np.array([0.82, 0.78, 0.88, 0.94, 1.00, 1.06, 1.08, 1.02, 1.12, 1.20, 1.38, 1.48])
    date_weights = np.array([month_weights[date.month - 1] for date in dates], dtype=float)
    date_weights = date_weights / date_weights.sum()
    transaction_dates = rng.choice(dates, size=row_count, p=date_weights)

    regions = rng.choice(
        ["Northeast", "South", "Midwest", "West", "International"],
        size=row_count,
        p=[0.24, 0.27, 0.18, 0.23, 0.08],
    )
    channels = rng.choice(
        ["Online", "Retail Store", "Wholesale", "Partner", "Inside Sales"],
        size=row_count,
        p=[0.42, 0.25, 0.13, 0.10, 0.10],
    )
    payments = rng.choice(
        ["Credit Card", "Debit Card", "ACH", "PayPal", "Invoice"],
        size=row_count,
        p=[0.46, 0.18, 0.12, 0.16, 0.08],
    )

    quantity = rng.choice(np.arange(1, 8), size=row_count, p=[0.36, 0.24, 0.16, 0.10, 0.07, 0.04, 0.03])
    price_noise = rng.normal(loc=1.0, scale=0.08, size=row_count)
    unit_price = np.maximum(products["base_price"].to_numpy(dtype=float) * price_noise, 5).round(2)
    discount = rng.choice([0.00, 0.05, 0.10, 0.15, 0.20, 0.25, 0.30], size=row_count, p=[0.38, 0.18, 0.16, 0.12, 0.08, 0.05, 0.03])

    df = pd.DataFrame(
        {
            "transaction_id": [f"TXN{1000000 + index}" for index in range(row_count)],
            "transaction_date": pd.to_datetime(transaction_dates).strftime("%Y-%m-%d"),
            "customer_id": [f"CUST{value:06d}" for value in rng.integers(1, 16000, size=row_count)],
            "product_id": products["product_id"],
            "product_name": products["product_name"],
            "category": products["category"],
            "quantity": quantity,
            "unit_price": unit_price,
            "discount": discount,
            "region": regions,
            "sales_channel": channels,
            "payment_method": payments,
        }
    )
    return df


def load_sales_data() -> pd.DataFrame:
    """Load raw sales data, generating synthetic data when no raw file exists."""
    ensure_directories()

    if not RAW_SALES_FILE.exists():
        logger.info("Raw sales file not found. Generating %s synthetic transactions.", SYNTHETIC_ROW_COUNT)
        synthetic_df = generate_synthetic_sales_data(SYNTHETIC_ROW_COUNT)
        synthetic_df.to_csv(RAW_SALES_FILE, index=False)
        synthetic_df.head(SAMPLE_ROW_COUNT).to_csv(SAMPLE_SALES_FILE, index=False)
        logger.info("Generated raw dataset at %s", RAW_SALES_FILE)

    try:
        sales_df = pd.read_csv(RAW_SALES_FILE)
    except pd.errors.EmptyDataError as exc:
        raise ValueError(f"Invalid CSV: {RAW_SALES_FILE} is empty.") from exc
    except pd.errors.ParserError as exc:
        raise ValueError(f"Invalid CSV format in {RAW_SALES_FILE}.") from exc

    validate_non_empty(sales_df, "raw sales")
    validate_required_columns(sales_df, "raw sales")
    logger.info("Loaded %s raw sales records.", len(sales_df))
    return sales_df

