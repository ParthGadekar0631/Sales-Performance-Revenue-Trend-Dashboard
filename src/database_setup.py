"""SQLite database setup and loading utilities."""

from __future__ import annotations

import sqlite3
from pathlib import Path

import pandas as pd

try:
    from .config import DATABASE_FILE
    from .logger import get_logger
except ImportError:  # pragma: no cover
    from config import DATABASE_FILE
    from logger import get_logger


logger = get_logger(__name__)

TABLE_ORDER = [
    "sales_transactions",
    "monthly_revenue_summary",
    "product_performance",
    "category_performance",
    "regional_performance",
    "sales_channel_performance",
    "dashboard_kpis",
]


def get_connection(database_file: Path = DATABASE_FILE) -> sqlite3.Connection:
    """Open a SQLite connection with clear failure handling."""
    try:
        database_file.parent.mkdir(parents=True, exist_ok=True)
        return sqlite3.connect(database_file)
    except sqlite3.Error as exc:
        raise ConnectionError(f"Unable to connect to SQLite database: {database_file}") from exc


def create_indexes(connection: sqlite3.Connection) -> None:
    """Create practical indexes for dashboard-style analytical queries."""
    statements = [
        "CREATE INDEX IF NOT EXISTS idx_sales_transaction_date ON sales_transactions(transaction_date);",
        "CREATE INDEX IF NOT EXISTS idx_sales_category ON sales_transactions(category);",
        "CREATE INDEX IF NOT EXISTS idx_sales_region ON sales_transactions(region);",
        "CREATE INDEX IF NOT EXISTS idx_sales_channel ON sales_transactions(sales_channel);",
        "CREATE INDEX IF NOT EXISTS idx_sales_product ON sales_transactions(product_id);",
    ]
    cursor = connection.cursor()
    for statement in statements:
        cursor.execute(statement)
    connection.commit()


def load_dataframes_to_database(cleaned_sales: pd.DataFrame, kpi_outputs: dict[str, pd.DataFrame]) -> None:
    """Persist cleaned and aggregated datasets to SQLite tables."""
    tables = {"sales_transactions": cleaned_sales, **kpi_outputs}

    with get_connection() as connection:
        try:
            for table_name in TABLE_ORDER:
                tables[table_name].to_sql(table_name, connection, if_exists="replace", index=False)
                logger.info("Loaded %s rows into %s.", len(tables[table_name]), table_name)
            create_indexes(connection)
        except sqlite3.Error as exc:
            raise RuntimeError("Failed while loading dataframes into SQLite.") from exc

