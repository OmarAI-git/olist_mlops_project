import pandas as pd
from src.pipeline import run_pipeline
from src.features import create_features


def test_pipeline_runs_on_test_data():
    df = pd.read_parquet(r"data/artifacts/03_test.parquet")

    predictions, probabilities = run_pipeline(df.head(5))

    assert len(predictions) == 5
    assert len(probabilities) == 5

    assert all(predictions >= 0)
    assert all(predictions <= 1)

    assert all(probabilities >= 0)
    assert all(probabilities <= 1)


def test_pipeline_reproduces_known_predictions():
    df = pd.read_parquet("data/artifacts/03_test.parquet")

    predictions, probabilities = run_pipeline(df.head(5))

    expected_predictions = [0, 0, 0, 0, 1]

    assert predictions.tolist() == expected_predictions


def test_no_data_leakage_in_features():
    df = pd.read_parquet("data/artifacts/03_train.parquet")

    features = create_features(df)

    forbidden_columns = {
        "late",
        "order_delivered_carrier_date",
        "order_delivered_customer_date",
        "order_id",
        "customer_id",
        "customer_unique_id",
    }

    assert forbidden_columns.isdisjoint(features.columns)
