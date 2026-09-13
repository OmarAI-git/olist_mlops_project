import great_expectations as gx


def validate_order_data(df):

    context = gx.get_context()

    data_source = context.data_sources.add_pandas('olist_validation_source')
    data_asset = data_source.add_dataframe_asset('order_data')

    batch_definition = data_asset.add_batch_definition_whole_dataframe('order_batch')

    batch = batch_definition.get_batch(batch_parameters = {'dataframe': df})

    NON_NEGATIVE_COLUMNS = [
    "total_price",
    "total_freight_value",
    "item_count",
    "payment_count",
    "total_payment",
    "avg_product_name_length",
    "avg_product_description_length",
    "avg_product_height_cm",
    "avg_product_length_cm",
    "avg_product_photos_qty",
    "avg_product_width_cm",
    "avg_product_weight_g",
    "product_count",
    "seller_count"]

    expectations = [
        gx.expectations.ExpectColumnToExist(column = 'order_status'),
    ]
    for column in NON_NEGATIVE_COLUMNS:
        expectations.append(
            gx.expectations.ExpectColumnValuesToBeBetween(
                column = column,
                min_value = 0
                )
            )

    results = []

    for expectation in expectations:
        result = batch.validate(expectation)
        results.append(result)

    return all(result.success for result in results)





