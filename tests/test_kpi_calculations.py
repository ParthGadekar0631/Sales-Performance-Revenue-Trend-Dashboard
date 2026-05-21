import pandas as pd

from src.feature_engineering import add_revenue_features
from src.kpi_calculations import calculate_all_kpis


def test_calculate_all_kpis_returns_consistent_revenue_totals():
    clean = pd.DataFrame(
        [
            {
                "transaction_id": "TXN1",
                "transaction_date": "2025-01-01",
                "customer_id": "C1",
                "product_id": "P1",
                "product_name": "Laptop",
                "category": "Electronics",
                "quantity": 2,
                "unit_price": 100.0,
                "discount": 0.10,
                "region": "West",
                "sales_channel": "Online",
                "payment_method": "Credit Card",
            },
            {
                "transaction_id": "TXN2",
                "transaction_date": "2025-02-01",
                "customer_id": "C2",
                "product_id": "P2",
                "product_name": "Desk",
                "category": "Furniture",
                "quantity": 1,
                "unit_price": 300.0,
                "discount": 0.00,
                "region": "South",
                "sales_channel": "Retail Store",
                "payment_method": "ACH",
            },
        ]
    )
    featured = add_revenue_features(clean)

    outputs = calculate_all_kpis(featured)
    dashboard = outputs["dashboard_kpis"].set_index("kpi_name")

    assert dashboard.loc["Total Revenue", "kpi_value"] == 480.0
    assert dashboard.loc["Total Orders", "kpi_value"] == 2
    assert outputs["monthly_revenue_summary"]["total_revenue"].sum() == 480.0
    assert set(outputs.keys()) == {
        "monthly_revenue_summary",
        "product_performance",
        "category_performance",
        "regional_performance",
        "sales_channel_performance",
        "dashboard_kpis",
    }

