"""Data validation helpers used across the project."""

from __future__ import annotations

from pathlib import Path

import pandas as pd

try:
    from .config import NUMERIC_COLUMNS, REQUIRED_COLUMNS
    from .logger import get_logger
except ImportError:  # pragma: no cover - supports python src/main.py
    from config import NUMERIC_COLUMNS, REQUIRED_COLUMNS
    from logger import get_logger


logger = get_logger(__name__)


def validate_file_exists(path: Path) -> None:
    """Raise a clear error when an expected input file is missing."""
    if not path.exists():
        raise FileNotFoundError(f"Required file not found: {path}")


def validate_non_empty(df: pd.DataFrame, dataset_name: str) -> None:
    """Validate that a dataframe contains records."""
    if df.empty:
        raise ValueError(f"{dataset_name} is empty and cannot be processed.")


def validate_required_columns(df: pd.DataFrame, dataset_name: str) -> None:
    """Validate the required raw sales schema."""
    missing = [column for column in REQUIRED_COLUMNS if column not in df.columns]
    if missing:
        raise ValueError(f"{dataset_name} is missing required columns: {missing}")


def validate_numeric_ranges(df: pd.DataFrame) -> dict[str, int]:
    """Return counts of invalid numeric values before cleaning."""
    results = {
        "invalid_quantity": int((pd.to_numeric(df["quantity"], errors="coerce") <= 0).sum()),
        "invalid_unit_price": int((pd.to_numeric(df["unit_price"], errors="coerce") <= 0).sum()),
        "invalid_discount": int(
            (
                (pd.to_numeric(df["discount"], errors="coerce") < 0)
                | (pd.to_numeric(df["discount"], errors="coerce") > 0.75)
            ).sum()
        ),
    }
    logger.info("Numeric validation summary: %s", results)
    return results


def validate_cleaned_sales(df: pd.DataFrame) -> None:
    """Validate core invariants after cleaning and feature engineering."""
    validate_non_empty(df, "cleaned sales")

    if df["transaction_id"].duplicated().any():
        raise ValueError("Cleaned sales contains duplicate transaction_id values.")

    for column in NUMERIC_COLUMNS:
        if df[column].isna().any():
            raise ValueError(f"Cleaned sales contains null values in {column}.")

    if (df["quantity"] <= 0).any():
        raise ValueError("Cleaned sales contains non-positive quantity values.")
    if (df["unit_price"] <= 0).any():
        raise ValueError("Cleaned sales contains non-positive unit_price values.")
    if ((df["discount"] < 0) | (df["discount"] > 0.75)).any():
        raise ValueError("Cleaned sales contains discounts outside the accepted 0-75% range.")
    if "net_revenue" in df.columns and (df["net_revenue"] < 0).any():
        raise ValueError("Cleaned sales contains negative net_revenue values.")

