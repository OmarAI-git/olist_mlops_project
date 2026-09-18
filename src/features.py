def create_features(df):
    df = df.copy()

    df["purchase_year"] = df["order_purchase_timestamp"].dt.year
    df["purchase_month"] = df["order_purchase_timestamp"].dt.month
    df["purchase_dayofweek"] = df["order_purchase_timestamp"].dt.dayofweek
    df["purchase_hour"] = df["order_purchase_timestamp"].dt.hour

    df["estimated_year"] = df["order_estimated_delivery_date"].dt.year

    df["estimated_month"] = df["order_estimated_delivery_date"].dt.month

    df["estimated_dayofweek"] = df["order_estimated_delivery_date"].dt.dayofweek

    # Drop some columns
    drop_cols = [
        "order_id",
        "customer_id",
        "customer_unique_id",
        "late",
        "order_purchase_timestamp",
        "order_approved_at",
        "order_delivered_carrier_date",
        "order_delivered_customer_date",
        "order_estimated_delivery_date",
    ]

    df = df.drop(columns=drop_cols, errors="ignore")

    return df
