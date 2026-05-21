"""CSV export utilities for Tableau-ready datasets."""

from __future__ import annotations

import pandas as pd

try:
    from .config import PROCESSED_FILES
    from .logger import get_logger
except ImportError:  # pragma: no cover
    from config import PROCESSED_FILES
    from logger import get_logger


logger = get_logger(__name__)


def export_processed_datasets(cleaned_sales: pd.DataFrame, kpi_outputs: dict[str, pd.DataFrame]) -> None:
    """Export cleaned and aggregated dataframes as Tableau-ready CSV files."""
    PROCESSED_FILES["cleaned_sales"].parent.mkdir(parents=True, exist_ok=True)
    cleaned_sales.to_csv(PROCESSED_FILES["cleaned_sales"], index=False)
    logger.info("Exported cleaned sales to %s", PROCESSED_FILES["cleaned_sales"])

    for dataset_name, dataframe in kpi_outputs.items():
        output_path = PROCESSED_FILES[dataset_name]
        dataframe.to_csv(output_path, index=False)
        logger.info("Exported %s to %s", dataset_name, output_path)

