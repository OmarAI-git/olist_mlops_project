USE MLOps_qafza

-- order_items, order_reviews, order_payments


SELECT order_id, COUNT(*) AS item_count
FROM dbo.olist_order_items_dataset
GROUP BY order_id



SELECT 
	order_id,
	COUNT(order_item_id) AS item_count,
	SUM(price) AS total_price,
	SUM(freight_value) AS total_freight_value
FROM dbo.olist_order_items_dataset
GROUP BY order_id



SELECT order_id, COUNT(payment_type)
FROM dbo.olist_order_payments_dataset
GROUP BY order_id
HAVING COUNT(payment_type) > 1



SELECT order_id, COUNT(payment_sequential)
FROM dbo.olist_order_payments_dataset
GROUP BY order_id
HAVING COUNT(payment_sequential) > 2

-- order_id, payment_sequential, payment_type, payment_installments, payment_value

SELECT
    order_id,
    COUNT(*) AS payment_count,
	SUM(payment_value) AS total_payment
FROM dbo.olist_order_payments_dataset
GROUP BY order_id;


SELECT TOP 20
    order_id,
    payment_sequential,
    payment_type,
    payment_installments,
    payment_value
FROM dbo.olist_order_payments_dataset
WHERE order_id IN (
    SELECT TOP 5 order_id
    FROM dbo.olist_order_payments_dataset
    GROUP BY order_id
    HAVING COUNT(*) > 1
)
ORDER BY order_id, payment_sequential;




SELECT *
FROM dbo.olist_order_reviews_dataset


SELECT 
    order_id,
    SUM(review_score) AS total_review_score
FROM dbo.olist_order_reviews_dataset
GROUP BY order_id



SELECT 
    oi.order_id,
    COUNT(pro.product_id) AS product_count,
    AVG(pro.product_height_cm) AS avg_product_height_cm,
    AVG(pro.product_description_lenght) AS avg_product_description_length,
    AVG(pro.product_length_cm) AS avg_product_length_cm,
    AVG(pro.product_name_lenght) AS avg_prduct_name_length,
    AVG(pro.product_photos_qty) AS avg_product_photos_qty,
    AVG(pro.product_weight_g) AS avg_product_wight_g,
    AVG(pro.product_width_cm) AS avg_product_width_cm
FROM dbo.olist_order_items_dataset AS oi
LEFT JOIN dbo.olist_products_dataset AS pro
ON oi.product_id = pro.product_id
GROUP BY oi.order_id





SELECT
    COUNT(*) AS total_rows,
    COUNT(DISTINCT order_id) AS distinct_orders
FROM (
    SELECT
        oi.order_id,
        COUNT(DISTINCT oi.product_id) AS product_count,
        AVG(p.product_weight_g) AS avg_product_weight_g,
        AVG(p.product_length_cm) AS avg_product_length_cm,
        AVG(p.product_height_cm) AS avg_product_height_cm,
        AVG(p.product_width_cm) AS avg_product_width_cm,
        AVG(p.product_photos_qty) AS avg_product_photos_qty
    FROM dbo.olist_order_items_dataset AS oi
    LEFT JOIN dbo.olist_products_dataset AS p
        ON oi.product_id = p.product_id
    GROUP BY oi.order_id
) AS product_agg;



SELECT
    COUNT(*) AS total_item_rows,
    COUNT(p.product_id) AS matched_products,
    COUNT(*) - COUNT(p.product_id) AS missing_products
FROM dbo.olist_order_items_dataset AS oi
LEFT JOIN dbo.olist_products_dataset AS p
    ON oi.product_id = p.product_id;


SELECT *
FROM dbo.olist_sellers_dataset


SELECT 
    COUNT(se) AS total_sellers,
    COUNT(DISTINCT seller_id) AS distinct_sellers
FROM dbo.olist_sellers_dataset



SELECT 
    s.seller_id,
    s.seller_city,
    s.seller_state,
    s.seller_zip_code_prefix
FROM dbo.olist_order_items_dataset AS oi
LEFT JOIN dbo.olist_sellers_dataset AS s
ON oi.seller_id = s.seller_id


