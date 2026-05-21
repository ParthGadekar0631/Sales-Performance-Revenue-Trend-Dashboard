import pandas as pd

from src.data_cleaning import clean_sales_data


def test_clean_sales_data_removes_duplicates_and_normalizes_values():
    raw = pd.DataFrame(
        [
            {
                "transaction_id": "TXN1",
                "transaction_date": "2025-01-01",
                "customer_id": " C1 ",
                "product_id": "P1",
                "product_name": "Laptop",
                "category": "electronics",
                "quantity": "2",
                "unit_price": "1000",
                "discount": "0.1",
                "region": "west",
                "sales_channel": "online",
                "payment_method": "credit card",
            },
            {
                "transaction_id": "TXN1",
                "transaction_date": "2025-01-01",
                "customer_id": "C1",
                "product_id": "P1",
                "product_name": "Laptop",
                "category": "electronics",
                "quantity": "2",
                "unit_price": "1000",
                "discount": "0.1",
                "region": "west",
                "sales_channel": "online",
                "payment_method": "credit card",
            },
        ]
    )

    cleaned = clean_sales_data(raw)

    assert len(cleaned) == 1
    assert cleaned.loc[0, "category"] == "Electronics"
    assert cleaned.loc[0, "region"] == "West"
    assert cleaned.loc[0, "quantity"] == 2


def test_clean_sales_data_drops_invalid_dates_and_non_positive_prices():
    raw = pd.DataFrame(
        [
            {
                "transaction_id": "TXN1",
                "transaction_date": "not-a-date",
                "customer_id": "C1",
                "product_id": "P1",
                "product_name": "Laptop",
                "category": "Electronics",
                "quantity": 1,
                "unit_price": 100,
                "discount": 0,
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
                "unit_price": -1,
                "discount": 0,
                "region": "South",
                "sales_channel": "Retail Store",
                "payment_method": "ACH",
            },
            {
                "transaction_id": "TXN3",
                "transaction_date": "2025-02-02",
                "customer_id": "C3",
                "product_id": "P3",
                "product_name": "Chair",
                "category": "Furniture",
                "quantity": 2,
                "unit_price": 50,
                "discount": 0.05,
                "region": "South",
                "sales_channel": "Retail Store",
                "payment_method": "ACH",
            },
        ]
    )

    cleaned = clean_sales_data(raw)

    assert cleaned["transaction_id"].tolist() == ["TXN3"]

