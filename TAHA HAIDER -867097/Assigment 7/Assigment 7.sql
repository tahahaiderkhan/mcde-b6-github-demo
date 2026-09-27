/*
    BikeStores - Window Functions Practice
    Questions 7.1 - 7.6
*/

USE BikeStores;
GO

/* ================================================================
   7.1
   Assign a sequential row number to each product ordered by
   list_price descending.
   Then assign a second row number partitioned by category_id.
   ================================================================ */

SELECT
    product_id,
    product_name,
    category_id,
    list_price,

    ROW_NUMBER() OVER (
        ORDER BY list_price DESC
    ) AS overall_row_number,

    ROW_NUMBER() OVER (
        PARTITION BY category_id
        ORDER BY list_price DESC
    ) AS category_row_number

FROM production.products;
GO


/* ================================================================
   7.2
   Return each product with RANK() and DENSE_RANK() by list_price
   descending within its category.

   Products with the same price receive the same rank.
   RANK() leaves gaps after ties, while DENSE_RANK() does not.
   ================================================================ */

SELECT
    product_id,
    product_name,
    category_id,
    list_price,

    RANK() OVER (
        PARTITION BY category_id
        ORDER BY list_price DESC
    ) AS price_rank,

    DENSE_RANK() OVER (
        PARTITION BY category_id
        ORDER BY list_price DESC
    ) AS dense_price_rank

FROM production.products
ORDER BY category_id, list_price DESC;
GO

/*
   To show only products where RANK() and DENSE_RANK() differ:

   SELECT *
   FROM
   (
       SELECT
           product_id,
           product_name,
           category_id,
           list_price,
           RANK() OVER (
               PARTITION BY category_id
               ORDER BY list_price DESC
           ) AS price_rank,
           DENSE_RANK() OVER (
               PARTITION BY category_id
               ORDER BY list_price DESC
           ) AS dense_price_rank
       FROM production.products
   ) AS ranked_products
   WHERE price_rank <> dense_price_rank;
*/


/* ================================================================
   7.3
   Month-over-month revenue change for each store using LAG().

   Revenue = quantity * list_price * (1 - discount)
   ================================================================ */

WITH monthly_revenue AS
(
    SELECT
        o.store_id,
        DATEFROMPARTS(
            YEAR(o.order_date),
            MONTH(o.order_date),
            1
        ) AS revenue_month,
        SUM(
            oi.quantity * oi.list_price * (1 - oi.discount)
        ) AS current_month_revenue
    FROM sales.orders AS o
    INNER JOIN sales.order_items AS oi
        ON o.order_id = oi.order_id
    GROUP BY
        o.store_id,
        DATEFROMPARTS(
            YEAR(o.order_date),
            MONTH(o.order_date),
            1
        )
)
SELECT
    store_id,
    revenue_month,
    current_month_revenue,

    LAG(current_month_revenue) OVER (
        PARTITION BY store_id
        ORDER BY revenue_month
    ) AS previous_month_revenue,

    current_month_revenue
        - LAG(current_month_revenue) OVER (
            PARTITION BY store_id
            ORDER BY revenue_month
        ) AS revenue_difference

FROM monthly_revenue
ORDER BY store_id, revenue_month;
GO


/* ================================================================
   7.4
   Divide all products into five price bands using NTILE(5).
   ================================================================ */

SELECT
    product_name,
    list_price,

    NTILE(5) OVER (
        ORDER BY list_price DESC
    ) AS price_band

FROM production.products
ORDER BY price_band, list_price DESC;
GO


/* ================================================================
   7.5
   Each order with a running total of revenue ordered by order_date.

   Revenue = SUM(quantity * list_price * (1 - discount))
   ================================================================ */

WITH order_revenue AS
(
    SELECT
        o.order_id,
        o.order_date,
        SUM(
            oi.quantity * oi.list_price * (1 - oi.discount)
        ) AS order_revenue
    FROM sales.orders AS o
    INNER JOIN sales.order_items AS oi
        ON o.order_id = oi.order_id
    GROUP BY
        o.order_id,
        o.order_date
)
SELECT
    order_id,
    order_date,
    order_revenue,

    SUM(order_revenue) OVER (
        ORDER BY order_date, order_id
        ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW
    ) AS running_total_revenue

FROM order_revenue
ORDER BY order_date, order_id;
GO


/* ================================================================
   7.6 - THINK ABOUT IT

   Question:
   Why does LAST_VALUE() require
   RANGE BETWEEN UNBOUNDED PRECEDING AND UNBOUNDED FOLLOWING
   to return the actual last value in the partition, while
   FIRST_VALUE() works correctly with the default frame?

   Answer:

   When ORDER BY is specified in a SQL Server window function and
   no explicit frame is provided, the default frame is effectively:

       RANGE BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW

   FIRST_VALUE() asks for the first value in the current window frame.
   Because the frame starts at UNBOUNDED PRECEDING, the first row of
   the partition is already included, so FIRST_VALUE() can return the
   actual first value of the partition.

   LAST_VALUE() asks for the last value in the CURRENT window frame.
   With the default frame ending at CURRENT ROW, the last value is
   therefore the value from the current row, NOT the final row of the
   entire partition.

   To make LAST_VALUE() look through the entire partition, extend the
   frame to the final row:

       RANGE BETWEEN UNBOUNDED PRECEDING AND UNBOUNDED FOLLOWING

   Example:

       LAST_VALUE(product_name) OVER (
           PARTITION BY category_id
           ORDER BY list_price
           RANGE BETWEEN UNBOUNDED PRECEDING AND UNBOUNDED FOLLOWING
       ) AS most_expensive_product

   In short:

       FIRST_VALUE()
       -> default frame starts at the first row
       -> first row is visible
       -> works as expected

       LAST_VALUE()
       -> default frame ends at the current row
       -> final partition row is NOT necessarily visible
       -> must extend frame to UNBOUNDED FOLLOWING
*/

/* End of 7.1 - 7.6 */
