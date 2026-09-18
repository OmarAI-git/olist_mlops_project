from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


def create_test_order():
    return {
        "order_purchase_timestamp": "2018-01-01T10:00:00",
        "order_estimated_delivery_date": "2018-01-15T10:00:00",
        "order_status": "delivered",
        "customer_city": "sao paulo",
        "customer_state": "SP",
        "customer_zip_code_prefix": 1000,
        "item_count": 1,
        "total_price": 100.0,
        "total_freight_value": 20.0,
        "payment_count": 1,
        "total_payment": 120.0,
        "avg_product_name_length": 50.0,
        "avg_product_description_length": 200.0,
        "avg_product_height_cm": 10.0,
        "avg_product_length_cm": 20.0,
        "avg_product_photos_qty": 2.0,
        "avg_product_width_cm": 15.0,
        "avg_product_weight_g": 500.0,
        "product_count": 1,
        "seller_count": 1,
    }


def test_health_endpoint():
    response = client.get("/health")

    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


def test_model_info_endpoint():
    response = client.get("/model-info")

    assert response.status_code == 200

    data = response.json()

    assert "model_name" in data
    assert "model_file" in data
    assert "threshold" in data


def test_predict_endpoint():
    order = {
        "order_purchase_timestamp": "2018-01-01T10:00:00",
        "order_estimated_delivery_date": "2018-01-15T10:00:00",
        "order_status": "delivered",
        "customer_city": "sao paulo",
        "customer_state": "SP",
        "customer_zip_code_prefix": 1000,
        "item_count": 1,
        "total_price": 100.0,
        "total_freight_value": 20.0,
        "payment_count": 1,
        "total_payment": 120.0,
        "avg_product_name_length": 50.0,
        "avg_product_description_length": 200.0,
        "avg_product_height_cm": 10.0,
        "avg_product_length_cm": 20.0,
        "avg_product_photos_qty": 2.0,
        "avg_product_width_cm": 15.0,
        "avg_product_weight_g": 500.0,
        "product_count": 1,
        "seller_count": 1,
    }

    response = client.post("/predict", json=order)

    assert response.status_code == 200

    data = response.json()

    assert "prediction" in data
    assert "probability" in data
    assert "model_version" in data

    assert data["prediction"] in [0, 1]
    assert 0 <= data["probability"] <= 1


def test_batch_predict_endpoint():
    orders = [create_test_order(), create_test_order()]

    response = client.post("/predict/batch", json={"orders": orders})

    assert response.status_code == 200

    data = response.json()

    assert "predictions" in data
    assert len(data["predictions"]) == 2

    for prediction in data["predictions"]:
        assert "prediction" in prediction
        assert "probability" in prediction
        assert "model_version" in prediction

        assert prediction["prediction"] in [0, 1]
        assert 0 <= prediction["probability"] <= 1


def test_batch_predict_rejects_invalid_data():
    order = create_test_order()
    order["total_price"] = -10.0

    response = client.post("/predict/batch", json={"orders": [order]})

    assert response.status_code == 400
    assert (
        response.json()["detail"] == "Batch input data failed data quality validation"
    )
