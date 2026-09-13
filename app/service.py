import pandas as pd
import time
import logging
from app.schema import OrderRequest
from src.pipeline import run_pipeline
from src.config import MLFLOW_MODEL_VERSION
from src.validation import validate_order_data


logger = logging.getLogger(__name__)


def predict_order(order: OrderRequest):

    start_time = time.perf_counter()

    data = order.model_dump()

    df = pd.DataFrame([data])

    if not validate_order_data(df):
        raise ValueError("Input data failed data quality validation")

    predictions, probabilities = run_pipeline(df)

    prediction = int(predictions[0])
    probability = float(probabilities[0])

    latency_ms = (time.perf_counter() - start_time) * 1000

    logger.info(
        'Prediction completed | input = %s | prediction = %s | probabilities = %.4f | model_version = %s | latency_ms = %.2f',
        data,
        prediction,
        probability,
        MLFLOW_MODEL_VERSION,
        latency_ms
    )

    return{
        'prediction': prediction,
        'probability': probability,
        'model_version': MLFLOW_MODEL_VERSION
    }



