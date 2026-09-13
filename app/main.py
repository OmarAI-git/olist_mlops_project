from fastapi import FastAPI
from src.config import MODEL_NAME, FINAL_MODEL
from src.predictor import load_threshold
from src.logging_config import setup_logging
from app.schema import OrderRequest
from app.service import predict_order


setup_logging()

app = FastAPI(
    title = 'Olist Late Delivery Prediction API',
    version = '0.1.0'
)


@app.get('/health')
def home():
    return {'status':'ok'}

@app.get('/model-info')
def model_info():
    threshold = load_threshold()
    return {
        'model_name': MODEL_NAME,
        'model_file': FINAL_MODEL.name,
        'threshold': threshold
    }

@app.post('/predict')
def predict(order: OrderRequest):
    return predict_order(order)


