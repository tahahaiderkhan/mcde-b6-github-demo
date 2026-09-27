-- BikeStores SQL Practice: CTEs
-- Questions 6.1 - 6.6

USE BikeStores;
GO

/* =========================================================
   6.1 - Rewrite derived table query as a CTE
   ========================================================= */

WITH store_counts AS
(
    SELECT
        store_id,
        COUNT(*) AS order_count
    FROM sales.orders
    GROUP BY store_id
)
SELECT
    AVG(order_count) AS avg_orders
FROM store_counts;
GO


/* =========================================================
   6.2 - High-value products + Mountain Bikes
   ========================================================= */

WITH cte_high_value_products AS
(
    SELECT
        product_id,
        product_name,
        category_id,
        list_price
    FROM production.products
    WHERE list_price > 2000
)
SELECT
    p.product_id,
    p.product_name,
    p.list_price,
    c.category_name
FROM cte_high_value_products AS p
JOIN production.categories AS c
    ON p.category_id = c.category_id
WHERE c.category_name = 'Mountain Bikes';
GO


/* =========================================================
   6.3 - Two CTEs: orders and revenue per customer
   ========================================================= */

WITH customer_orders AS
(
    SELECT
        customer_id,
        COUNT(*) AS order_count
    FROM sales.orders
    GROUP BY customer_id
),
customer_revenue AS
(
    SELECT
        o.customer_id,
        SUM(oi.quantity * oi.list_price * (1 - oi.discount)) AS total_revenue
    FROM sales.orders AS o
    JOIN sales.order_items AS oi
        ON o.order_id = oi.order_id
    GROUP BY o.customer_id
)
SELECT
    co.customer_id,
    co.order_count,
    cr.total_revenue
FROM customer_orders AS co
JOIN customer_revenue AS cr
    ON co.customer_id = cr.customer_id;
GO


/* =========================================================
   6.4 - Recursive CTE: numbers 1 to 10 and their squares
   ========================================================= */

WITH numbers AS
(
    -- Anchor member
    SELECT
        1 AS n

    UNION ALL

    -- Recursive member
    SELECT
        n + 1
    FROM numbers
    WHERE n < 10
)
SELECT
    n,
    n * n AS square
FROM numbers
OPTION (MAXRECURSION 10);
GO


/* =========================================================
   6.5 - Recursive CTE: employee org chart
   Shows:
   - employee
   - manager first name
   - level
   ========================================================= */

WITH org_chart AS
(
    -- Top-level managers
    SELECT
        s.staff_id,
        s.first_name AS employee_first_name,
        s.last_name AS employee_last_name,
        s.manager_id,
        CAST(NULL AS VARCHAR(50)) AS manager_first_name,
        0 AS level
    FROM sales.staffs AS s
    WHERE s.manager_id IS NULL

    UNION ALL

    -- Direct / indirect reports
    SELECT
        s.staff_id,
        s.first_name AS employee_first_name,
        s.last_name AS employee_last_name,
        s.manager_id,
        oc.employee_first_name AS manager_first_name,
        oc.level + 1 AS level
    FROM sales.staffs AS s
    JOIN org_chart AS oc
        ON s.manager_id = oc.staff_id
)
SELECT
    staff_id,
    employee_first_name,
    employee_last_name,
    manager_first_name,
    level
FROM org_chart
ORDER BY level, staff_id
OPTION (MAXRECURSION 100);
GO


/* =========================================================
   6.6 - Think About It
   =========================================================

   A CTE is NOT automatically materialized.

   Example:

   WITH cte AS
   (
       SELECT ...
   )
   SELECT ...
   FROM cte AS a
   JOIN cte AS b
       ON ...;

   The fact that the CTE is written only once does NOT guarantee
   that SQL Server computes it once and stores/reuses the result.

   SQL Server's optimizer decides how the query is executed.
   A CTE is mainly a query-writing / readability feature.

   If the result genuinely needs to be computed once and reused,
   materialize it explicitly, for example in a temporary table:

   SELECT ...
   INTO #my_result
   FROM ...;

   Then reuse it:

   SELECT ...
   FROM #my_result AS a
   JOIN #my_result AS b
       ON ...;

   Another option is a table variable for appropriate small/use-case
   scenarios, but a temporary table is commonly used when you need
   to materialize and reuse an intermediate result.
*/
