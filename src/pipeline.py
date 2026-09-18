import pandas as pd
from src.features import create_features
from src.preprocessing import transform_features
from src.predictor import predict
from src.model_loader import load_inference_artifacts


def run_pipeline(df: pd.DataFrame):
    preprocessor, model, threshold = load_inference_artifacts()

    features = create_features(df)

    X = transform_features(features, preprocessor)

    predictions, probabilities = predict(model, X, threshold)

    return predictions, probabilities
