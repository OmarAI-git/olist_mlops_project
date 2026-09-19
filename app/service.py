import logging
import time

import pandas as pd
from fastapi import HTTPException

from app.schema import OrderRequest
from src.monitoring import (
    PREDICTION_ERRORS,
    PREDICTION_LATENCY,
    PREDICTION_REQUESTS,
    PREDICTIONS,
)
from src.pipeline import run_pipeline
from src.predictor import get_model_version
from src.validation import validate_order_data


logger = logging.getLogger(__name__)


def predict_order(order: OrderRequest):
    PREDICTION_REQUESTS.inc()

    start_time = time.perf_counter()

    try:
        data = order.model_dump()
        df = pd.DataFrame([data])

        if not validate_order_data(df):
            PREDICTION_ERRORS.inc()

            raise HTTPException(
                status_code=400,
                detail="Input data failed data quality validation",
            )

        predictions, probabilities = run_pipeline(df)

        prediction = int(predictions[0])
        probability = float(probabilities[0])
        model_version = get_model_version()

        PREDICTIONS.labels(prediction=str(prediction)).inc()

        latency_ms = (time.perf_counter() - start_time) * 1000

        logger.info(
            "Prediction completed | input = %s | prediction = %s | "
            "probability = %.4f | model_version = %s | latency_ms = %.2f",
            data,
            prediction,
            probability,
            model_version,
            latency_ms,
        )

        return {
            "prediction": prediction,
            "probability": probability,
            "model_version": model_version,
        }

    except HTTPException:
        raise

    except Exception:
        PREDICTION_ERRORS.inc()

        logger.exception("Prediction failed")

        raise

    finally:
        PREDICTION_LATENCY.observe(time.perf_counter() - start_time)


def predict_orders(orders: list[OrderRequest]):
    PREDICTION_REQUESTS.inc()

    start_time = time.perf_counter()

    try:
        data = [order.model_dump() for order in orders]
        df = pd.DataFrame(data)

        if not validate_order_data(df):
            PREDICTION_ERRORS.inc()

            raise HTTPException(
                status_code=400,
                detail="Batch input data failed data quality validation",
            )

        predictions, probabilities = run_pipeline(df)

        model_version = get_model_version()

        results = []

        for prediction, probability in zip(predictions, probabilities):
            prediction = int(prediction)
            probability = float(probability)

            PREDICTIONS.labels(prediction=str(prediction)).inc()

            results.append(
                {
                    "prediction": prediction,
                    "probability": probability,
                    "model_version": model_version,
                }
            )

        latency_ms = (time.perf_counter() - start_time) * 1000

        logger.info(
            "Batch prediction completed | count = %s | "
            "model_version = %s | latency_ms = %.2f",
            len(orders),
            model_version,
            latency_ms,
        )

        return results

    except HTTPException:
        raise

    except Exception:
        PREDICTION_ERRORS.inc()

        logger.exception("Batch prediction failed")

        raise

    finally:
        PREDICTION_LATENCY.observe(time.perf_counter() - start_time)
