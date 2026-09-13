USE MLOps_qafza



WITH ml_table AS (
	     SELECT 
				o.order_id,
				o.customer_id,
				o.order_status,
				o.order_purchase_timestamp,
				o.order_approved_at,
				o.order_delivered_carrier_date,
				o.order_delivered_customer_date,
				o.order_estimated_delivery_date,

				c.customer_unique_id,
				c.customer_city,
				c.customer_state,
				c.customer_zip_code_prefix,

				i.item_count,
				i.total_price,
				i.total_freight_value,

				pay.payment_count,
				pay.total_payment,

				pro.avg_product_name_length,
				pro.avg_product_description_length,
				pro.avg_product_height_cm,
				pro.avg_product_length_cm,
				pro.avg_product_photos_qty,
				pro.avg_product_width_cm,
				pro.avg_product_wight_g,
				pro.product_count,

				sel.seller_count
			FROM dbo.olist_orders_dataset AS o
			LEFT JOIN dbo.olist_customers_dataset AS c
			ON o.customer_id = c.customer_id
			LEFT JOIN (
			SELECT 
				order_id,
				COUNT(order_item_id) AS item_count,
				SUM(price) AS total_price,
				SUM(freight_value) AS total_freight_value
			FROM dbo.olist_order_items_dataset
			GROUP BY order_id) AS i
			ON o.order_id = i.order_id
			LEFT JOIN (
			SELECT
				order_id,
				COUNT(*) AS payment_count,
				SUM(payment_value) AS total_payment
			FROM dbo.olist_order_payments_dataset
			GROUP BY order_id) AS pay
			ON o.order_id = pay.order_id
			LEFT JOIN (
			SELECT 
				oi.order_id,
				COUNT(pro.product_id) AS product_count,
				AVG(pro.product_height_cm) AS avg_product_height_cm,
				AVG(pro.product_description_lenght) AS avg_product_description_length,
				AVG(pro.product_length_cm) AS avg_product_length_cm,
				AVG(pro.product_name_lenght) AS avg_product_name_length,
				AVG(pro.product_photos_qty) AS avg_product_photos_qty,
				AVG(pro.product_weight_g) AS avg_product_wight_g,
				AVG(pro.product_width_cm) AS avg_product_width_cm
			FROM dbo.olist_order_items_dataset AS oi
			LEFT JOIN dbo.olist_products_dataset AS pro
			ON oi.product_id = pro.product_id
			GROUP BY oi.order_id
			) AS pro
			ON o.order_id = pro.order_id
			LEFT JOIN (
			SELECT
				oi.order_id,
				COUNT(DISTINCT oi.seller_id) AS seller_count
			FROM dbo.olist_order_items_dataset AS oi
			GROUP BY oi.order_id) AS sel
			ON o.order_id = sel.order_id
)


SELECT 
	COUNT(*) AS total_rows,
	COUNT(DISTINCT order_id) AS distinct_rows
FROM ml_table

