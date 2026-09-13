from datetime import datetime
from app.schema import OrderRequest
from app.service import predict_order


def test_predict_order():
    order = OrderRequest(
        order_purchase_timestamp=datetime(2018, 1, 1, 10, 30),
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

    result = predict_order(order)

    assert "prediction" in result
    assert "probability" in result

    assert result["prediction"] in [0, 1]
    assert 0 <= result["probability"] <= 1



