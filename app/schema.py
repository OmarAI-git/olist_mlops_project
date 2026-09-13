from datetime import datetime
from pydantic import BaseModel


class OrderRequest(BaseModel):

    order_purchase_timestamp: datetime
    order_estimated_delivery_date: datetime

    order_status: str
    customer_city: str
    customer_state: str

    customer_zip_code_prefix: int
    item_count: int

    total_price: float
    total_freight_value: float

    payment_count: int
    total_payment: float

    avg_product_name_length: float
    avg_product_description_length: float
    avg_product_height_cm: float
    avg_product_length_cm: float
    avg_product_photos_qty: float
    avg_product_width_cm: float
    avg_product_weight_g: float

    product_count: int
    seller_count: int


