import pandas as pd

from src.feature_engineering import add_revenue_features


def test_add_revenue_features_calculates_financial_fields():
    clean = pd.DataFrame(
        [
            {
                "transaction_id": "TXN1",
                "transaction_date": "2025-01-15",
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
            }
        ]
    )

    featured = add_revenue_features(clean)

    assert featured.loc[0, "gross_revenue"] == 200.0
    assert featured.loc[0, "discount_amount"] == 20.0
    assert featured.loc[0, "net_revenue"] == 180.0
    assert featured.loc[0, "transaction_month"] == "2025-01"
    assert featured.loc[0, "transaction_year"] == 2025

