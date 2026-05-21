"""Feature engineering for revenue analytics."""

from __future__ import annotations

import pandas as pd

try:
    from .logger import get_logger
    from .validation import validate_cleaned_sales, validate_non_empty
except ImportError:  # pragma: no cover
    from logger import get_logger
    from validation import validate_cleaned_sales, validate_non_empty


logger = get_logger(__name__)


def add_revenue_features(clean_df: pd.DataFrame) -> pd.DataFrame:
    """Add Tableau-ready revenue, discount, and time dimensions."""
    validate_non_empty(clean_df, "cleaned sales")
    df = clean_df.copy()

    df["transaction_date"] = pd.to_datetime(df["transaction_date"], errors="coerce")
    df = df.dropna(subset=["transaction_date"]).copy()

    df["gross_revenue"] = (df["quantity"] * df["unit_price"]).round(2)
    df["discount_amount"] = (df["gross_revenue"] * df["discount"]).round(2)
    df["net_revenue"] = (df["gross_revenue"] - df["discount_amount"]).round(2)
    df["average_order_value"] = df["net_revenue"].round(2)
    df["transaction_month"] = df["transaction_date"].dt.to_period("M").astype(str)
    df["transaction_year"] = df["transaction_date"].dt.year.astype(int)
    df["monthly_sales"] = df["transaction_month"]
    df["yearly_sales"] = df["transaction_year"]
    df["transaction_date"] = df["transaction_date"].dt.strftime("%Y-%m-%d")

    validate_cleaned_sales(df)
    logger.info("Added revenue and date features to %s records.", len(df))
    return df

