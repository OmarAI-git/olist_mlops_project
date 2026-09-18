import pandas as pd
import time
import logging
from app.schema import OrderRequest
from src.pipeline import run_pipeline
from src.predictor import get_model_version
from src.validation import validate_order_data
from fastapi import HTTPException


logger = logging.getLogger(__name__)


MLFLOW_MODEL_VERSION = get_model_version()


def predict_order(order: OrderRequest):
    start_time = time.perf_counter()

    data = order.model_dump()

    df = pd.DataFrame([data])

    if not validate_order_data(df):
        raise HTTPException(
            status_code=400, detail="Input data failed data quality validation"
        )

    predictions, probabilities = run_pipeline(df)

    prediction = int(predictions[0])
    probability = float(probabilities[0])

    latency_ms = (time.perf_counter() - start_time) * 1000

    logger.info(
        "Prediction completed | input = %s | prediction = %s | probabilities = %.4f | model_version = %s | latency_ms = %.2f",
        data,
        prediction,
        probability,
        MLFLOW_MODEL_VERSION,
        latency_ms,
    )

    return {
        "prediction": prediction,
        "probability": probability,
        "model_version": MLFLOW_MODEL_VERSION,
    }


def predict_orders(orders: list[OrderRequest]):
    start_time = time.perf_counter()

    data = [order.model_dump() for order in orders]
    df = pd.DataFrame(data)

    if not validate_order_data(df):
        raise HTTPException(
            status_code=400, detail="Batch input data failed data quality validation"
        )

    predictions, probabilities = run_pipeline(df)

    results = []

    for prediction, probability in zip(predictions, probabilities):
        results.append(
            {
                "prediction": int(prediction),
                "probability": float(probability),
                "model_version": MLFLOW_MODEL_VERSION,
            }
        )

    latency_ms = (time.perf_counter() - start_time) * 1000

    logger.info(
        "Batch prediction completed | count = %s | model_version = %s | latency_ms = %.2f",
        len(orders),
        MLFLOW_MODEL_VERSION,
        latency_ms,
    )

    return results
