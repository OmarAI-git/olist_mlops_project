import pandas as pd
import great_expectations as gx


def test_order_status_column_exists():

    df = pd.read_parquet('data/artifacts/03_train.parquet')

    context = gx.get_context()

    data_source = context.data_sources.add_pandas('olist_data_source')

    data_asset = data_source.add_dataframe_asset('test_data')

    batch_definition = data_asset.add_batch_definition_whole_dataframe('test_batch')

    batch = batch_definition.get_batch(batch_parameters = {'dataframe':df})

    expectation = gx.expectations.ExpectColumnToExist(column = 'order_status')

    result = batch.validate(expectation)

    assert result.success


def test_total_price_is_not_negative():

    df = pd.read_parquet('data/artifacts/03_train.parquet')

    context = gx.get_context()

    data_source = context.data_sources.add_pandas('olist_data_source')
    data_asset = data_source.add_dataframe_asset('test_data')

    batch_definition = data_asset.add_batch_definition_whole_dataframe('test_batch')

    batch = batch_definition.get_batch(batch_parameters = {'dataframe':df})

    expectation = gx.expectations.ExpectColumnValuesToBeBetween(column = 'total_price', min_value = 0)

    result = batch.validate(expectation)

    assert result.success





