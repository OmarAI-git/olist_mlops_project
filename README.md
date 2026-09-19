# Olist MLOps - From Notebooks to Production

Production-style MLOps project for predicting whether an Olist order will be delivered late.

The project converts the original notebook-based machine learning workflow into a reproducible inference service using Python modules, FastAPI, MLflow, DVC, Great Expectations, Docker, pytest, Ruff, pre-commit, and GitHub Actions.

---

## 1. Project Goal

The service receives information about a new order and returns:

* `prediction`: `0` for on-time, `1` for late
* `probability`: predicted probability of late delivery
* `model_version`: MLflow model version used for inference

Training remains in the notebooks. The production service only loads already-fitted preprocessing objects and the registered model.

The inference service never refits the model or preprocessing pipeline.

---

## 2. Project Structure

```text
Olist_project/
│
├── app/
│   ├── main.py
│   ├── schema.py
│   └── service.py
│
├── config/
│   └── config.yaml
│
├── data/
│   ├── csv_files/
│   └── artifacts/
│
├── docs/
│   └── monitoring.md
│
├── models/
│   └── decision_threshold.joblib
│
├── notebooks/
│   ├── Notebook 1
│   ├── Notebook 2
│   ├── Notebook 3
│   ├── Notebook 4
│   ├── Notebook 5
│   └── Notebook 6
│
├── requirements/
│   ├── runtime.txt
│   └── dev.txt
│
├── src/
│   ├── config.py
│   ├── data_quality.py
│   ├── logging_config.py
│   ├── mlflow_register.py
│   ├── monitoring.py
│   ├── model_loader.py
│   ├── pipeline.py
│   ├── predictor.py
│   └── validation.py
│
├── tests/
│
├── Dockerfile
├── docker-compose.yml
├── pyproject.toml
├── .pre-commit-config.yaml
├── .github/workflows/ci.yml
└── README.md
```

---

## 3. Main Components

### FastAPI

Provides the production inference API.

Available endpoints:

* `GET /health`
* `GET /model-info`
* `GET /metrics`
* `POST /predict`
* `POST /predict/batch`

Interactive API documentation is automatically available through FastAPI.

### MLflow

MLflow stores and serves the registered production model.

The registered model is:

```text
olist-xgboost
```

The production alias is:

```text
champion
```

The API loads the model using the MLflow alias rather than loading the XGBoost model directly from the local notebook/model folder.

### DVC

DVC versions important datasets and fitted preprocessing artifacts.

Tracked artifacts include:

* training data
* validation data
* test data
* preprocessing object
* original data files

### Great Expectations / Data Validation

Incoming inference data is validated before reaching the model.

Validation covers:

* required columns
* data types
* numeric ranges
* allowed categorical values
* missing-value limits

Invalid requests are rejected with HTTP `400`.

### Docker

The application runs inside a container.

Docker Compose provides:

* FastAPI inference service
* MLflow tracking/model registry service

### Testing

The project uses pytest for:

* schema tests
* preprocessing tests
* feature tests
* model tests
* API integration tests
* service tests
* data validation tests

### Code Quality

Ruff is used for linting and formatting.

Pre-commit runs the configured code-quality hooks before commits.

### CI/CD

GitHub Actions runs automated code-quality checks and tests on pushes and pull requests.

---

## 4. Configuration

Application configuration is stored in:

```text
config/config.yaml
```

The configuration contains:

* data paths
* artifact paths
* model information
* API host and port
* MLflow tracking URI
* MLflow model name
* MLflow model alias

Environment variables can override deployment-specific values such as the MLflow tracking URI.

---

## 5. Local Development

Create and activate a virtual environment:

```powershell
python -m venv venv_olist_project
.\venv_olist_project\Scripts\Activate.ps1
```

Install development dependencies:

```powershell
pip install -r requirements/dev.txt
```

---

## 6. Running Tests

Run the complete test suite:

```powershell
python -m pytest -q
```

Expected result:

```text
17 passed
```

Run Ruff:

```powershell
ruff check app src tests
```

Check formatting:

```powershell
ruff format --check app src tests
```

Run pre-commit:

```powershell
pre-commit run --all-files
```

---

## 7. Running with Docker Compose

Start the complete service:

```powershell
docker compose up -d
```

Check container status:

```powershell
docker compose ps
```

Expected services:

```text
api       Up
mlflow    Up (healthy)
```

The API is available at:

```text
http://localhost:8000
```

MLflow is available at:

```text
http://localhost:5000
```

Stop the services:

```powershell
docker compose down
```

---

## 8. API Usage

### Health Check

```text
GET /health
```

Expected response:

```json
{
  "status": "ok"
}
```

### Model Information

```text
GET /model-info
```

Returns:

* model name
* model alias
* model version
* threshold

### Single Prediction

```text
POST /predict
```

The response contains:

```json
{
  "prediction": 0,
  "probability": 0.22,
  "model_version": "1"
}
```

### Batch Prediction

```text
POST /predict/batch
```

Returns a list of predictions with their probabilities and model version.

### Metrics

```text
GET /metrics
```

The endpoint exposes Prometheus-compatible application metrics.

---

## 9. Model and Inference Pipeline

The inference flow is:

```text
API Request
    |
    v
Pydantic Schema Validation
    |
    v
Data Quality Validation
    |
    v
Feature Engineering
    |
    v
Saved Preprocessor
    |
    v
MLflow Registered XGBoost Model
    |
    v
Probability
    |
    v
Decision Threshold
    |
    v
Prediction + Probability + Model Version
```

The preprocessing pipeline is loaded from:

```text
data/artifacts/preprocessor.joblib
```

The decision threshold is loaded from:

```text
models/decision_threshold.joblib
```

The XGBoost model is loaded from MLflow using:

```text
models:/olist-xgboost@champion
```

No model fitting or preprocessing fitting occurs during inference.

---

## 10. Reproducibility

The production pipeline was checked against the notebook inference pipeline.

For the same test input, the production preprocessing and model produced matching predictions and probabilities.

The final XGBoost model uses the same fitted preprocessing artifacts and model configuration from the training notebooks.

The final decision threshold is:

```text
0.50
```

---

## 11. Logging

Application logging is configured with Python's logging system.

Logs are written to:

```text
logs/app.log
```

Prediction logs contain:

* request input
* prediction
* probability
* model version
* latency

Logging is intended to support troubleshooting and later model evaluation.

---

## 12. Monitoring

The service exposes Prometheus-compatible metrics through:

```text
GET /metrics
```

Current metrics include:

* total prediction requests
* prediction errors
* prediction latency
* prediction counts by class

Detailed monitoring and alert criteria are documented in:

```text
docs/monitoring.md
```

The monitoring design covers:

* request volume
* latency
* error rate
* prediction distribution
* model version
* data quality failures

---

## 13. DVC

DVC is used to version important data and preprocessing artifacts.

Check DVC status:

```powershell
dvc status
```

Tracked DVC artifacts include the training, validation, and test datasets and the fitted preprocessing artifact.

---

## 14. MLflow Model Registry

The final XGBoost model is registered in MLflow as:

```text
olist-xgboost
```

The production alias is:

```text
champion
```

The API resolves the model through this alias.

This allows a new registered model version to be promoted by changing the MLflow alias without changing application code.

---

## 15. CI/CD

GitHub Actions runs automated checks for repository changes.

The CI workflow includes:

* dependency installation
* Ruff linting
* Ruff formatting checks
* automated tests

A failing quality check or test causes the CI job to fail.

Pre-commit is also configured locally to run Ruff checks and formatting.

---

## 16. Production Design Principles

The project follows these principles:

1. Training and inference are separated.
2. Inference never refits preprocessing or models.
3. Model artifacts are versioned.
4. The production model is loaded from MLflow.
5. Configuration is separated from application code.
6. Input data is validated before inference.
7. Errors are handled explicitly.
8. Predictions are logged.
9. API behavior is tested.
10. The service is containerized.
11. Code quality is automated.
12. Monitoring metrics are exposed for operational visibility.

---

## 17. Quick Start

For a machine with Docker installed:

```powershell
git clone <repository-url>
cd Olist_project
docker compose up -d
```

Check the services:

```powershell
docker compose ps
```

Then open:

```text
http://localhost:8000/docs
```

The FastAPI Swagger UI provides interactive documentation and allows testing the prediction endpoints.
