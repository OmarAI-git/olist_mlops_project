import pandas as pd
import mlflow
from src.features import create_features
from src.preprocessing import load_preprocessor, transform_features
from xgboost import XGBClassifier
from src.config import MLFLOW_MODEL_NAME, MLFLOW_TRACKING_URI
from src.predictor import get_model_version


MLFLOW_MODEL_VERSION = get_model_version()


def test_registered_model_loads():
    mlflow.set_tracking_uri(MLFLOW_TRACKING_URI)

    model_uri = f"models:/{MLFLOW_MODEL_NAME}/{MLFLOW_MODEL_VERSION}"

    model = mlflow.xgboost.load_model(model_uri)

    assert isinstance(model, XGBClassifier)


def test_model_prediction_shape():
    mlflow.set_tracking_uri(MLFLOW_TRACKING_URI)

    model_uri = f"models:/{MLFLOW_MODEL_NAME}/{MLFLOW_MODEL_VERSION}"

    model = mlflow.xgboost.load_model(model_uri)

    df = pd.read_parquet("data/artifacts/03_test.parquet")

    features = create_features(df.head(5))
    preprocessor = load_preprocessor()
    X = transform_features(features, preprocessor)

    probabilities = model.predict_proba(X)

    assert probabilities.shape == (5, 2)
    assert ((probabilities >= 0) & (probabilities <= 1)).all()
