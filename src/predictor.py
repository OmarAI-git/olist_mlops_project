import mlflow
import joblib
from src.config import THRESHOLD, MLFLOW_MODEL_VERSION, MLFLOW_TRACKING_URI, MLFLOW_MODEL_NAME

MODEL_URI = f'models:/{MLFLOW_MODEL_NAME}/{MLFLOW_MODEL_VERSION}'



def load_model():
    mlflow.set_tracking_uri(MLFLOW_TRACKING_URI)
    return mlflow.xgboost.load_model(MODEL_URI)


def load_threshold():
    return joblib.load(THRESHOLD)


def predict(model, X, threshold):
    probabilities = model.predict_proba(X)[:, 1]
    predictions = (probabilities >= threshold).astype(int)

    return predictions, probabilities



