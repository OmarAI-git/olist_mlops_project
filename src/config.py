from pathlib import Path
import yaml


BASE_DIR = Path(__file__).parent.parent

CONFIG_FILE = BASE_DIR / 'config' / 'config.yaml'

with open(CONFIG_FILE, 'r') as f:
    config = yaml.safe_load(f)


DATA = BASE_DIR / config['paths']['data']

ARTIFACTS = BASE_DIR / config['paths']['artifacts']

MODELS = BASE_DIR / config['paths']['models']

MODEL_NAME = config['models']['name']

FINAL_MODEL = MODELS / config['models']['file']

THRESHOLD = MODELS / config["models"]["threshold_file"]

API_HOST = config['api']['host']

API_PORT = config['api']['port']

MLFLOW_TRACKING_URI = config['mlflow']['tracking_uri']

MLFLOW_MODEL_NAME = config['mlflow']['model_name']

MLFLOW_MODEL_VERSION = config['mlflow']['model_version']

