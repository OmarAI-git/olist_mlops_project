FROM python:3.13-slim

WORKDIR /app

COPY requirements/runtime.txt requirements/runtime.txt

RUN pip install --no-cache-dir -r requirements/runtime.txt

COPY app/ app/
COPY src/ src/
COPY config/ config/

COPY data/artifacts/preprocessor.joblib data/artifacts/preprocessor.joblib 
COPY models/decision_threshold.joblib models/decision_threshold.joblib

EXPOSE 8000

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]



