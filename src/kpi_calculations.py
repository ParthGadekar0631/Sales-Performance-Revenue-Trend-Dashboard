"""Business KPI calculations for the dashboard exports."""

from __future__ import annotations

import pandas as pd

try:
    from .logger import get_logger
    from .validation import validate_cleaned_sales
except ImportError:  # pragma: no cover
    from logger import get_logger
    from validation import validate_cleaned_sales


logger = get_logger(__name__)


def _contribution(series: pd.Series) -> pd.Series:
    total = series.sum()
    if total == 0:
        return pd.Series([0.0] * len(series), index=series.index)
    return (series / total * 100).round(2)


def calculate_monthly_revenue_summary(df: pd.DataFrame) -> pd.DataFrame:
    """Calculate monthly revenue, orders, units, AOV, and growth."""
    summary = (
        df.groupby("transaction_month", as_index=False)
        .agg(
            total_revenue=("net_revenue", "sum"),
            gross_revenue=("gross_revenue", "sum"),
            discount_amount=("discount_amount", "sum"),
            total_orders=("transaction_id", "nunique"),
            total_units_sold=("quantity", "sum"),
            average_transaction_value=("net_revenue", "mean"),
        )
        .sort_values("transaction_month")
    )
    summary["monthly_growth_pct"] = summary["total_revenue"].pct_change().mul(100).fillna(0).round(2)
    summary["total_revenue"] = summary["total_revenue"].round(2)
    summary["gross_revenue"] = summary["gross_revenue"].round(2)
    summary["discount_amount"] = summary["discount_amount"].round(2)
    summary["average_transaction_value"] = summary["average_transaction_value"].round(2)
    summary["revenue_rank"] = summary["total_revenue"].rank(method="dense", ascending=False).astype(int)
    return summary


def calculate_dimension_performance(df: pd.DataFrame, dimension: str) -> pd.DataFrame:
    """Calculate revenue contribution for a business dimension."""
    performance = (
        df.groupby(dimension, as_index=False)
        .agg(
            total_revenue=("net_revenue", "sum"),
            gross_revenue=("gross_revenue", "sum"),
            discount_amount=("discount_amount", "sum"),
            total_orders=("transaction_id", "nunique"),
            total_units_sold=("quantity", "sum"),
            average_transaction_value=("net_revenue", "mean"),
        )
        .sort_values("total_revenue", ascending=False)
        .reset_index(drop=True)
    )
    performance["revenue_contribution_pct"] = _contribution(performance["total_revenue"])
    performance["revenue_rank"] = performance["total_revenue"].rank(method="dense", ascending=False).astype(int)

    rounded_columns = ["total_revenue", "gross_revenue", "discount_amount", "average_transaction_value"]
    performance[rounded_columns] = performance[rounded_columns].round(2)
    return performance


def calculate_product_performance(df: pd.DataFrame) -> pd.DataFrame:
    """Calculate product-level performance with category context."""
    product = (
        df.groupby(["product_id", "product_name", "category"], as_index=False)
        .agg(
            total_revenue=("net_revenue", "sum"),
            gross_revenue=("gross_revenue", "sum"),
            discount_amount=("discount_amount", "sum"),
            total_orders=("transaction_id", "nunique"),
            total_units_sold=("quantity", "sum"),
            average_transaction_value=("net_revenue", "mean"),
        )
        .sort_values("total_revenue", ascending=False)
        .reset_index(drop=True)
    )
    product["revenue_contribution_pct"] = _contribution(product["total_revenue"])
    product["revenue_rank"] = product["total_revenue"].rank(method="dense", ascending=False).astype(int)
    product[["total_revenue", "gross_revenue", "discount_amount", "average_transaction_value"]] = product[
        ["total_revenue", "gross_revenue", "discount_amount", "average_transaction_value"]
    ].round(2)
    return product


def calculate_dashboard_kpis(df: pd.DataFrame, monthly_summary: pd.DataFrame) -> pd.DataFrame:
    """Calculate executive KPI cards for the dashboard."""
    total_revenue = float(df["net_revenue"].sum())
    total_orders = int(df["transaction_id"].nunique())
    total_units = int(df["quantity"].sum())
    avg_transaction_value = float(df["net_revenue"].mean())
    total_discount = float(df["discount_amount"].sum())
    latest_month = monthly_summary["transaction_month"].max()
    latest_month_row = monthly_summary.loc[monthly_summary["transaction_month"] == latest_month].iloc[0]

    previous_month_revenue = 0.0
    if len(monthly_summary) > 1:
        previous_month_revenue = float(monthly_summary.iloc[-2]["total_revenue"])

    kpis = [
        ("Total Revenue", round(total_revenue, 2), "USD", "Net revenue after discounts"),
        ("Total Orders", total_orders, "Orders", "Unique sales transactions"),
        ("Total Units Sold", total_units, "Units", "Quantity sold across all transactions"),
        ("Average Transaction Value", round(avg_transaction_value, 2), "USD", "Average net revenue per order"),
        ("Total Discount Amount", round(total_discount, 2), "USD", "Total discounts applied"),
        ("Latest Month Revenue", round(float(latest_month_row["total_revenue"]), 2), "USD", f"Revenue for {latest_month}"),
        ("Latest Monthly Growth %", round(float(latest_month_row["monthly_growth_pct"]), 2), "Percent", f"Growth for {latest_month}"),
        ("Previous Month Revenue", round(previous_month_revenue, 2), "USD", "Comparison baseline for latest month"),
    ]

    return pd.DataFrame(kpis, columns=["kpi_name", "kpi_value", "unit", "description"])


def calculate_all_kpis(df: pd.DataFrame) -> dict[str, pd.DataFrame]:
    """Calculate all KPI datasets used by SQL, Tableau, and reports."""
    validate_cleaned_sales(df)
    monthly = calculate_monthly_revenue_summary(df)
    outputs = {
        "monthly_revenue_summary": monthly,
        "product_performance": calculate_product_performance(df),
        "category_performance": calculate_dimension_performance(df, "category"),
        "regional_performance": calculate_dimension_performance(df, "region"),
        "sales_channel_performance": calculate_dimension_performance(df, "sales_channel"),
        "dashboard_kpis": calculate_dashboard_kpis(df, monthly),
    }
    logger.info("Calculated KPI datasets: %s", ", ".join(outputs.keys()))
    return outputs

