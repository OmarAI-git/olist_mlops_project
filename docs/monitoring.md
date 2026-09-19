# Monitoring

The Olist inference service exposes Prometheus-compatible metrics through:

GET /metrics

## Metrics

- `prediction_requests_total`
  - Total number of prediction requests.

- `prediction_errors_total`
  - Total number of failed prediction requests.

- `prediction_latency_seconds`
  - Histogram of prediction request latency.

- `predictions_total{prediction="0"}`
  - Number of on-time predictions.

- `predictions_total{prediction="1"}`
  - Number of late predictions.

## Prediction Logs

Each prediction is logged with:

- input data
- prediction
- probability
- model version
- latency

Application logs are available in:

logs/app.log

These logs can later be used for offline evaluation and drift analysis.

## Alert Criteria

The following thresholds are recommended operational alert criteria:

### Error rate

Trigger an alert if the prediction error rate exceeds 5% over a 5-minute window.

### Latency

Trigger an alert if p95 prediction latency exceeds 1 second over a 5-minute window.

### Prediction distribution

Monitor the percentage of late predictions.

An alert should be investigated when the production late-prediction rate deviates materially from the established baseline.

The baseline should be calculated from a representative validation or historical production period rather than hardcoded without evidence.

### Model version

Investigate immediately if the served model version does not match the expected MLflow `champion` alias.

## Data Quality

Incoming requests are validated before reaching the model.

Invalid requests are rejected with HTTP 400.

Validation covers:

- required columns
- data types
- numeric ranges
- allowed categorical values
- missing-value limits

This prevents invalid data from silently reaching the inference model.
