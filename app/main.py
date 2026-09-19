from fastapi import FastAPI, Response
from src.config import MODEL_NAME, FINAL_MODEL, MLFLOW_MODEL_ALIAS
from src.predictor import load_threshold, get_model_version
from src.logging_config import setup_logging
from app.schema import OrderRequest, BatchPredictionRequest, BatchPredictionsResponse
from app.service import predict_order, predict_orders
from src.model_loader import load_inference_artifacts
from contextlib import asynccontextmanager
from prometheus_client import CONTENT_TYPE_LATEST, generate_latest


setup_logging()


@asynccontextmanager
async def lifespan(app: FastAPI):
    load_inference_artifacts()
    yield


app = FastAPI(title="Olist Late Delivery Prediction API", version="0.1.0")


@app.get("/health")
def home():
    return {"status": "ok"}


@app.get("/model-info")
def model_info():
    threshold = load_threshold()
    return {
        "model_name": MODEL_NAME,
        "model_file": FINAL_MODEL.name,
        "model_alias": MLFLOW_MODEL_ALIAS,
        "model_version": get_model_version(),
        "threshold": threshold,
    }


@app.get("/metrics")
def metrics():
    return Response(content=generate_latest(), media_type=CONTENT_TYPE_LATEST)


@app.post("/predict")
def predict(order: OrderRequest):
    return predict_order(order)


@app.post("/predict/batch", response_model=BatchPredictionsResponse)
def predict_batch(request: BatchPredictionRequest):
    predictions = predict_orders(request.orders)

    return {"predictions": predictions}
