from datetime import datetime

import pytest
from pydantic import ValidationError

from app.schema import OrderRequest


def test_valid_order_request():
    order = OrderRequest(
        order_purchase_timestamp=datetime(2018, 1, 1, 10, 30),
        order_estimated_delivery_date=datetime(2018, 1, 10),
        order_status="delivered",
        customer_city="sao paulo",
        customer_state="SP",
        customer_zip_code_prefix=12345,
        item_count=2,
        total_price=100.0,
        total_freight_value=20,
        payment_count=1,
        total_payment=120,
        avg_product_name_length=50,
        avg_product_description_length=200,
        avg_product_height_cm=10,
        avg_product_length_cm=20,
        avg_product_photos_qty=3,
        avg_product_width_cm=15,
        avg_product_weight_g=500,
        product_count=2,
        seller_count=1,
    )

    assert order.order_status == "delivered"
    assert order.total_price == 100.0


def test_invalid_order_request():
    with pytest.raises(ValidationError):
        OrderRequest(
            order_purchase_timestamp="not-a-date",
            order_estimated_delivery_date=datetime(2018, 1, 10),
            order_status="delivered",
            customer_city="sao paulo",
            customer_state="SP",
            customer_zip_code_prefix=12345,
            item_count=2,
            total_price=100.0,
            total_freight_value=20.0,
            payment_count=1,
            total_payment=120.0,
            avg_product_name_length=50.0,
            avg_product_description_length=200.0,
            avg_product_height_cm=10.0,
            avg_product_length_cm=20.0,
            avg_product_photos_qty=3.0,
            avg_product_width_cm=15.0,
            avg_product_weight_g=500.0,
            product_count=2,
            seller_count=1,
        )
