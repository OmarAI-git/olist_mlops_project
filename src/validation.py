import great_expectations as gx

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
    "seller_count",
]

EXPECTED_TYPES = {
    "order_status": "str",
    "customer_city": "str",
    "customer_state": "str",
    "customer_zip_code_prefix": "int64",
    "item_count": "int64",
    "total_price": "float64",
    "total_freight_value": "float64",
    "payment_count": "int64",
    "total_payment": "float64",
    "avg_product_name_length": "float64",
    "avg_product_description_length": "float64",
    "avg_product_height_cm": "float64",
    "avg_product_length_cm": "float64",
    "avg_product_photos_qty": "float64",
    "avg_product_width_cm": "float64",
    "avg_product_weight_g": "float64",
    "product_count": "int64",
    "seller_count": "int64",
}

ALLOWED_CATEGORIES = {"order_status": ["canceled", "delivered"]}


REQUIRED_COLUMNS = [
    "order_status",
    "customer_city",
    "customer_state",
    "customer_zip_code_prefix",
    "item_count",
    "total_price",
    "total_freight_value",
    "payment_count",
    "total_payment",
    "product_count",
    "seller_count",
]

IMPUTABLE_COLUMNS = [
    "avg_product_name_length",
    "avg_product_description_length",
    "avg_product_height_cm",
    "avg_product_length_cm",
    "avg_product_photos_qty",
    "avg_product_width_cm",
    "avg_product_weight_g",
]


def validate_order_data(df):
    context = gx.get_context()

    data_source = context.data_sources.add_pandas("olist_validation_source")
    data_asset = data_source.add_dataframe_asset("order_data")

    batch_definition = data_asset.add_batch_definition_whole_dataframe("order_batch")

    batch = batch_definition.get_batch(batch_parameters={"dataframe": df})

    expectations = [
        gx.expectations.ExpectColumnToExist(column="order_status"),
    ]

    for column in NON_NEGATIVE_COLUMNS:
        expectations.append(
            gx.expectations.ExpectColumnValuesToBeBetween(column=column, min_value=0)
        )

    for column, expected_type in EXPECTED_TYPES.items():
        expectations.append(
            gx.expectations.ExpectColumnValuesToBeOfType(
                column=column, type_=expected_type
            )
        )

    for column in REQUIRED_COLUMNS:
        expectations.append(
            gx.expectations.ExpectColumnValuesToNotBeNull(column=column)
        )

    for column in IMPUTABLE_COLUMNS:
        expectations.append(
            gx.expectations.ExpectColumnProportionOfNonNullValuesToBeBetween(
                column=column, min_value=0.95, max_value=1.0
            )
        )

    for column, allowed_values in ALLOWED_CATEGORIES.items():
        expectations.append(
            gx.expectations.ExpectColumnValuesToBeInSet(
                column=column, value_set=allowed_values
            )
        )

    results = []

    for expectation in expectations:
        result = batch.validate(expectation)
        results.append(result)

    return all(result.success for result in results)
