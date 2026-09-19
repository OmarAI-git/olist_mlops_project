from prometheus_client import Counter, Histogram


PREDICTION_REQUESTS = Counter(
    "prediction_request_total", "Total number of prediction request."
)


PREDICTION_ERRORS = Counter(
    "prediction_errors_total", "Total number of prediction errors."
)


PREDICTION_LATENCY = Histogram(
    "prediction_latency_seconds", "Prediction request latency in seconds."
)


PREDICTIONS = Counter(
    "prediction_total", "Total number of prediction by class.", ["prediction"]
)
