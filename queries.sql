-- ============================================================
-- DecodeLabs Industrial Training Kit - Batch 2026
-- Project 3: SQL Data Analysis
-- Author: Bhumi Singh
-- Database: orders.db | Table: orders (1,200 rows)
-- ============================================================
-- This file demonstrates SELECT, WHERE, GROUP BY, ORDER BY,
-- and aggregations (COUNT, SUM, AVG) against the cleaned
-- e-commerce orders dataset from Project 1/2.
--
-- Note on execution order: SQL is written
-- SELECT -> FROM -> WHERE -> GROUP BY -> HAVING -> ORDER BY
-- but the ENGINE executes it as
-- FROM -> WHERE -> GROUP BY -> HAVING -> SELECT -> ORDER BY
-- This is why column aliases created in SELECT cannot be
-- referenced inside WHERE (the "Alias Trap") -- but CAN be
-- referenced in ORDER BY, since ORDER BY runs after SELECT.
-- ============================================================


-- ----------------------------------------------------------
-- SECTION 1: BASIC SELECT QUERIES
-- ----------------------------------------------------------

-- 1.1 View the first 10 rows of the dataset
SELECT *
FROM orders
LIMIT 10;

-- 1.2 Select only specific columns (Product, Quantity, TotalPrice)
SELECT OrderID, Product, Quantity, TotalPrice
FROM orders
LIMIT 10;

-- 1.3 Total number of orders in the dataset
SELECT COUNT(*) AS total_orders
FROM orders;


-- ----------------------------------------------------------
-- SECTION 2: WHERE CLAUSE - FILTERING ROWS
-- ----------------------------------------------------------

-- 2.1 Equality filter: orders paid via Credit Card
SELECT OrderID, PaymentMethod, TotalPrice
FROM orders
WHERE PaymentMethod = 'Credit Card'
LIMIT 10;

-- 2.2 Comparison filter: high-value orders above 2000
SELECT OrderID, Product, TotalPrice
FROM orders
WHERE TotalPrice > 2000
ORDER BY TotalPrice DESC;

-- 2.3 Combined filter: Cancelled or Returned orders worth investigating
SELECT OrderID, Product, OrderStatus, TotalPrice
FROM orders
WHERE OrderStatus IN ('Cancelled', 'Returned')
ORDER BY TotalPrice DESC
LIMIT 15;

-- 2.4 Pattern matching: orders that used a coupon code
SELECT OrderID, CouponCode, TotalPrice
FROM orders
WHERE CouponCode != 'No Coupon'
LIMIT 10;

-- 2.5 Date range filter: orders placed in 2024
SELECT OrderID, Date, TotalPrice
FROM orders
WHERE Date >= '2024-01-01' AND Date <= '2024-12-31'
ORDER BY Date
LIMIT 10;


-- ----------------------------------------------------------
-- SECTION 3: GROUP BY - CATEGORICAL BREAKDOWNS
-- ----------------------------------------------------------

-- 3.1 Number of orders per product
SELECT Product, COUNT(*) AS order_count
FROM orders
GROUP BY Product
ORDER BY order_count DESC;

-- 3.2 Number of orders per order status
SELECT OrderStatus, COUNT(*) AS order_count
FROM orders
GROUP BY OrderStatus
ORDER BY order_count DESC;

-- 3.3 Number of orders per referral source
SELECT ReferralSource, COUNT(*) AS order_count
FROM orders
GROUP BY ReferralSource
ORDER BY order_count DESC;


-- ----------------------------------------------------------
-- SECTION 4: AGGREGATIONS - COUNT, SUM, AVG
-- ----------------------------------------------------------

-- 4.1 Total revenue by product (SUM)
SELECT Product,
       COUNT(*) AS num_orders,
       SUM(TotalPrice) AS total_revenue
FROM orders
GROUP BY Product
ORDER BY total_revenue DESC;

-- 4.2 Average order value by payment method (AVG)
SELECT PaymentMethod,
       COUNT(*) AS num_orders,
       ROUND(AVG(TotalPrice), 2) AS avg_order_value
FROM orders
GROUP BY PaymentMethod
ORDER BY avg_order_value DESC;

-- 4.3 Revenue and average order value by referral source
SELECT ReferralSource,
       COUNT(*) AS num_orders,
       SUM(TotalPrice) AS total_revenue,
       ROUND(AVG(TotalPrice), 2) AS avg_order_value
FROM orders
GROUP BY ReferralSource
ORDER BY total_revenue DESC;

-- 4.4 Coupon usage impact: average order value with vs without coupon
SELECT
    CASE WHEN CouponCode = 'No Coupon' THEN 'No Coupon' ELSE 'Used Coupon' END AS coupon_status,
    COUNT(*) AS num_orders,
    ROUND(AVG(TotalPrice), 2) AS avg_order_value
FROM orders
GROUP BY coupon_status;

-- 4.5 Monthly revenue trend (SUM grouped by month)
SELECT substr(Date, 1, 7) AS year_month,
       COUNT(*) AS num_orders,
       SUM(TotalPrice) AS total_revenue
FROM orders
GROUP BY year_month
ORDER BY year_month;


-- ----------------------------------------------------------
-- SECTION 5: HAVING - FILTERING AGGREGATED RESULTS
-- ----------------------------------------------------------

-- 5.1 Products that generated more than 180,000 in total revenue
SELECT Product,
       SUM(TotalPrice) AS total_revenue
FROM orders
GROUP BY Product
HAVING SUM(TotalPrice) > 180000
ORDER BY total_revenue DESC;

-- 5.2 Payment methods used in more than 230 orders
SELECT PaymentMethod,
       COUNT(*) AS num_orders
FROM orders
GROUP BY PaymentMethod
HAVING COUNT(*) > 230
ORDER BY num_orders DESC;


-- ----------------------------------------------------------
-- SECTION 6: ADVANCED / BUSINESS-FOCUSED QUERIES
-- ----------------------------------------------------------

-- 6.1 Top 10 highest-value orders (outlier candidates)
SELECT OrderID, CustomerID, Product, TotalPrice, OrderStatus
FROM orders
ORDER BY TotalPrice DESC
LIMIT 10;

-- 6.2 Percentage of orders that are Cancelled or Returned
SELECT
    ROUND(
        100.0 * SUM(CASE WHEN OrderStatus IN ('Cancelled', 'Returned') THEN 1 ELSE 0 END)
        / COUNT(*), 1
    ) AS pct_cancelled_or_returned
FROM orders;

-- 6.3 Revenue contribution of each product as a percentage of total revenue
SELECT Product,
       SUM(TotalPrice) AS product_revenue,
       ROUND(100.0 * SUM(TotalPrice) / (SELECT SUM(TotalPrice) FROM orders), 2) AS pct_of_total_revenue
FROM orders
GROUP BY Product
ORDER BY product_revenue DESC;

-- 6.4 Customers with more than 1 order (repeat customers)
SELECT CustomerID,
       COUNT(*) AS num_orders,
       SUM(TotalPrice) AS total_spent
FROM orders
GROUP BY CustomerID
HAVING COUNT(*) > 1
ORDER BY total_spent DESC;

-- 6.5 Best-performing product per order status (only Delivered orders, ranked by revenue)
SELECT Product,
       SUM(TotalPrice) AS revenue_from_delivered
FROM orders
WHERE OrderStatus = 'Delivered'
GROUP BY Product
ORDER BY revenue_from_delivered DESC
LIMIT 5;

-- 6.6 Demonstrating the Alias Trap (commented out - this query FAILS):
-- SELECT TotalPrice AS rev FROM orders WHERE rev > 1000;
-- ERROR: 'rev' does not exist yet when WHERE is evaluated
-- (WHERE runs BEFORE SELECT in the engine's execution order)
-- Correct version repeats the expression in WHERE instead of the alias:
SELECT TotalPrice AS rev
FROM orders
WHERE TotalPrice > 1000
ORDER BY rev DESC
LIMIT 10;
-- Note: the alias 'rev' DOES work in ORDER BY, since ORDER BY
-- runs AFTER SELECT in the execution order.
