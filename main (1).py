import sqlite3
import pandas as pd

# Connect to the database
conn = sqlite3.connect('data.sqlite')

# CodeGrade step1
df_boston = pd.read_sql("""
SELECT e.firstName, e.lastName, e.jobTitle
FROM employees AS e
JOIN offices AS o
    ON e.officeCode = o.officeCode
WHERE o.city = 'Boston';
""", conn)

# CodeGrade step2
df_zero_emp = pd.read_sql("""
SELECT o.officeCode, o.city, COUNT(e.employeeNumber) AS num_employees
FROM offices AS o
LEFT JOIN employees AS e
    ON o.officeCode = e.officeCode
GROUP BY o.officeCode, o.city
HAVING COUNT(e.employeeNumber) = 0;
""", conn)

# CodeGrade step3
df_employee = pd.read_sql("""
SELECT e.firstName, e.lastName, o.city, o.state
FROM employees AS e
LEFT JOIN offices AS o
    ON e.officeCode = o.officeCode
ORDER BY e.firstName, e.lastName;
""", conn)

# CodeGrade step4
df_contacts = pd.read_sql("""
SELECT c.contactFirstName, c.contactLastName, c.phone, c.salesRepEmployeeNumber
FROM customers AS c
LEFT JOIN orders AS o
    ON c.customerNumber = o.customerNumber
WHERE o.orderNumber IS NULL
ORDER BY c.contactLastName;
""", conn)

# CodeGrade step5
df_payment = pd.read_sql("""
SELECT c.contactFirstName, c.contactLastName, p.paymentDate, CAST(p.amount AS REAL) AS amount
FROM customers AS c
JOIN payments AS p
    ON c.customerNumber = p.customerNumber
ORDER BY CAST(p.amount AS REAL) DESC;
""", conn)

# CodeGrade step6
df_credit = pd.read_sql("""
SELECT e.employeeNumber, e.firstName, e.lastName, COUNT(c.customerNumber) AS number_customers
FROM employees AS e
JOIN customers AS c
    ON e.employeeNumber = c.salesRepEmployeeNumber
GROUP BY e.employeeNumber, e.firstName, e.lastName
HAVING AVG(CAST(c.creditLimit AS REAL)) > 90000
ORDER BY number_customers DESC;
""", conn)

# CodeGrade step7
df_product_sold = pd.read_sql("""
SELECT p.productName, COUNT(od.orderNumber) AS numorders, SUM(CAST(od.quantityOrdered AS INTEGER)) AS totalunits
FROM products AS p
JOIN orderdetails AS od
    ON p.productCode = od.productCode
GROUP BY p.productName
ORDER BY totalunits DESC;
""", conn)

# CodeGrade step8
df_total_customers = pd.read_sql("""
SELECT p.productName, p.productCode, COUNT(DISTINCT o.customerNumber) AS numpurchasers
FROM products AS p
JOIN orderdetails AS od
    ON p.productCode = od.productCode
JOIN orders AS o
    ON od.orderNumber = o.orderNumber
GROUP BY p.productName, p.productCode
ORDER BY numpurchasers DESC;
""", conn)

# CodeGrade step9
df_customers = pd.read_sql("""
SELECT o.officeCode, o.city, COUNT(DISTINCT c.customerNumber) AS n_customers
FROM offices AS o
LEFT JOIN employees AS e
    ON o.officeCode = e.officeCode
LEFT JOIN customers AS c
    ON e.employeeNumber = c.salesRepEmployeeNumber
GROUP BY o.officeCode, o.city
ORDER BY n_customers DESC;
""", conn)

# CodeGrade step10
df_under_20 = pd.read_sql("""
SELECT DISTINCT e.employeeNumber, e.firstName, e.lastName, off.city, off.officeCode
FROM employees AS e
JOIN offices AS off
    ON e.officeCode = off.officeCode
JOIN customers AS c
    ON e.employeeNumber = c.salesRepEmployeeNumber
JOIN orders AS o
    ON c.customerNumber = o.customerNumber
JOIN orderdetails AS od
    ON o.orderNumber = od.orderNumber
WHERE od.productCode IN (
    SELECT od2.productCode
    FROM orderdetails AS od2
    JOIN orders AS o2
        ON od2.orderNumber = o2.orderNumber
    GROUP BY od2.productCode
    HAVING COUNT(DISTINCT o2.customerNumber) < 20
)
ORDER BY e.lastName;
""", conn)

conn.close()
