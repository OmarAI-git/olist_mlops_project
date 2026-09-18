import mlflow
import joblib
import logging
from src.config import FINAL_MODEL


MODEL_NAME = "olist-xgboost"


logging.basicConfig(
    level=logging.INFO, format="%(asctime)s | %(levelname)s | %(message)s"
)

logger = logging.getLogger(__name__)


def register_model():
    logger.info("loading model from %s", FINAL_MODEL)

    model = joblib.load(FINAL_MODEL)

    mlflow.set_tracking_uri("http://127.0.0.1:5000")

    mlflow.set_experiment("olist-xgboost-test")

    with mlflow.start_run() as run:
        mlflow.log_param("model_name", "xgboost")
        mlflow.log_param("model_fit", FINAL_MODEL.name)

        mlflow.xgboost.log_model(
            xgb_model=model, name="model", registered_model_name=MODEL_NAME
        )

        logger.info("Model registered successfully")
        logger.info("Run ID: %s", run.info.run_id)
        logger.info("Model name: %s", MODEL_NAME)


if __name__ == "__main__":
    register_model()
