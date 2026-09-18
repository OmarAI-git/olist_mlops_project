from src.preprocessing import load_preprocessor
from src.predictor import load_model, load_threshold
from functools import lru_cache


@lru_cache(maxsize=1)
def load_inference_artifacts():
    preprocessor = load_preprocessor()
    model = load_model()
    threshold = load_threshold()

    return preprocessor, model, threshold
