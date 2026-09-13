import pandas as pd
from src.features import create_features
from src.preprocessing import load_preprocessor, transform_features
from src.predictor import load_model, load_threshold, predict


def run_pipeline(df: pd.DataFrame):

    features = create_features(df)

    preprocessor = load_preprocessor()

    X = transform_features(features, preprocessor)

    model = load_model()

    threshold = load_threshold()

    predictions, probabilities = predict(model, X, threshold)

    return predictions, probabilities



