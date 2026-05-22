"""Data cleaning logic for raw sales transactions."""

from __future__ import annotations

import pandas as pd

try:
    from .config import NUMERIC_COLUMNS, REQUIRED_COLUMNS
    from .logger import get_logger
    from .validation import validate_non_empty, validate_numeric_ranges, validate_required_columns
except ImportError:  # pragma: no cover
    from config import NUMERIC_COLUMNS, REQUIRED_COLUMNS
    from logger import get_logger
    from validation import validate_non_empty, validate_numeric_ranges, validate_required_columns


logger = get_logger(__name__)

CATEGORY_NORMALIZATION = {
    "electronics": "Electronics",
    "electronic": "Electronics",
    "furniture": "Furniture",
    "home and kitchen": "Home & Kitchen",
    "home & kitchen": "Home & Kitchen",
    "kitchen": "Home & Kitchen",
    "apparel": "Apparel",
    "clothing": "Apparel",
    "software": "Software",
    "office supplies": "Office Supplies",
    "office": "Office Supplies",
}


def normalize_text(value: object) -> str:
    """Convert common text fields to title-style values with clean whitespace."""
    if pd.isna(value):
        return "Unknown"
    return " ".join(str(value).strip().split())


def clean_sales_data(raw_df: pd.DataFrame) -> pd.DataFrame:
    """Clean raw sales transactions and enforce business-quality rules."""
    validate_non_empty(raw_df, "raw sales")
    validate_required_columns(raw_df, "raw sales")

    df = raw_df[REQUIRED_COLUMNS].copy()
    starting_rows = len(df)

    duplicate_count = int(df.duplicated(subset=["transaction_id"]).sum())
    df = df.drop_duplicates(subset=["transaction_id"], keep="first")

    df["transaction_date"] = pd.to_datetime(df["transaction_date"], format="%Y-%m-%d", errors="coerce")
    invalid_dates = int(df["transaction_date"].isna().sum())
    df = df.dropna(subset=["transaction_date"])

    for column in NUMERIC_COLUMNS:
        df[column] = pd.to_numeric(df[column], errors="coerce")

    validate_numeric_ranges(df)

    text_columns = ["customer_id", "product_id", "product_name", "category", "region", "sales_channel", "payment_method"]
    for column in text_columns:
        df[column] = df[column].apply(normalize_text)

    category_key = df["category"].str.lower().str.replace(r"\s+", " ", regex=True)
    df["category"] = category_key.map(CATEGORY_NORMALIZATION).fillna(df["category"].str.title())
    df["region"] = df["region"].str.title()
    df["sales_channel"] = df["sales_channel"].replace({"Retail store": "Retail Store", "Inside sales": "Inside Sales"})
    df["payment_method"] = df["payment_method"].replace({"Ach": "ACH", "Paypal": "PayPal"})

    df["quantity"] = df["quantity"].fillna(df["quantity"].median()).round().astype(int)
    df["unit_price"] = df["unit_price"].fillna(df["unit_price"].median()).round(2)
    df["discount"] = df["discount"].fillna(0).clip(lower=0, upper=0.75).round(4)

    invalid_numeric = int(((df["quantity"] <= 0) | (df["unit_price"] <= 0)).sum())
    df = df[(df["quantity"] > 0) & (df["unit_price"] > 0)]

    for column in text_columns:
        df[column] = df[column].replace("", "Unknown").fillna("Unknown")

    df = df.sort_values("transaction_date").reset_index(drop=True)
    df["transaction_date"] = df["transaction_date"].dt.strftime("%Y-%m-%d")

    logger.info(
        "Cleaned sales data: start=%s, duplicates=%s, invalid_dates=%s, invalid_numeric=%s, final=%s",
        starting_rows,
        duplicate_count,
        invalid_dates,
        invalid_numeric,
        len(df),
    )
    return df
