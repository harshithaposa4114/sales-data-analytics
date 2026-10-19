-- Sales Data Analysis: SQL practice
-- Assumed table name: sales
-- Columns: Date, Region, Product, Category, Quantity, UnitPrice

-- 1. Total revenue
SELECT SUM(Quantity * UnitPrice) AS total_revenue
FROM sales;

-- 2. Revenue by product
SELECT Product, SUM(Quantity * UnitPrice) AS revenue
FROM sales
GROUP BY Product
ORDER BY revenue DESC;

-- 3. Revenue by region
SELECT Region, SUM(Quantity * UnitPrice) AS revenue
FROM sales
GROUP BY Region
ORDER BY revenue DESC;

-- 4. Revenue by month (syntax shown for MySQL)
SELECT DATE_FORMAT(Date, '%Y-%m') AS sales_month,
       SUM(Quantity * UnitPrice) AS revenue
FROM sales
GROUP BY DATE_FORMAT(Date, '%Y-%m')
ORDER BY sales_month;

-- 5. Best-selling products by units
SELECT Product, SUM(Quantity) AS units_sold
FROM sales
GROUP BY Product
ORDER BY units_sold DESC;
