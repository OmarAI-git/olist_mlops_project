import joblib
from src.config import ARTIFACTS


PREPROCESSOR_PATH = ARTIFACTS / "preprocessor.joblib"


def load_preprocessor():
    return joblib.load(PREPROCESSOR_PATH)


def transform_features(df, preprocessor):
    return preprocessor.transform(df)
