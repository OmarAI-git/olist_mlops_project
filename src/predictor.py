import mlflow
import joblib
from functools import lru_cache
from mlflow import MlflowClient
from src.config import (
    THRESHOLD,
    MLFLOW_MODEL_ALIAS,
    MLFLOW_TRACKING_URI,
    MLFLOW_MODEL_NAME,
)

MODEL_URI = f"models:/{MLFLOW_MODEL_NAME}@{MLFLOW_MODEL_ALIAS}"


def load_model():
    mlflow.set_tracking_uri(MLFLOW_TRACKING_URI)
    return mlflow.xgboost.load_model(MODEL_URI)


@lru_cache(maxsize=1)
def get_model_version():
    mlflow.set_tracking_uri(MLFLOW_TRACKING_URI)

    client = MlflowClient()

    model_version = client.get_model_version_by_alias(
        MLFLOW_MODEL_NAME, MLFLOW_MODEL_ALIAS
    )

    return str(model_version.version)


def load_threshold():
    return joblib.load(THRESHOLD)


def predict(model, X, threshold):
    probabilities = model.predict_proba(X)[:, 1]
    predictions = (probabilities >= threshold).astype(int)

    return predictions, probabilities
