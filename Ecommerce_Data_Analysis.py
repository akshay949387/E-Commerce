import sqlite3
import pandas as pd
import matplotlib.pyplot as plt

conn = sqlite3.connect("ecommerce.db")
cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS transactions (
    TransactionID INTEGER PRIMARY KEY,
    CustomerID INTEGER,
    ProductCategory TEXT,
    Amount REAL,
    TransactionDate TEXT
)
""")

sample_data = [
    (1, 101, "Electronics", 1200, "2023-01-05"),
    (2, 102, "Clothing", 80, "2023-01-05"),
    (3, 103, "Groceries", 40, "2023-01-06"),
    (4, 101, "Electronics", 700, "2023-01-10"),
    (5, 104, "Clothing", 150, "2023-01-12"),
    (6, 102, "Groceries", 50, "2023-01-13"),
    (7, 105, "Electronics", 500, "2023-01-15"),
    (8, 101, "Clothing", 200, "2023-01-16"),
    (9, 106, "Groceries", 60, "2023-01-16"),
    (10, 104, "Electronics", 950, "2023-01-17"),
]
cursor.executemany("INSERT INTO transactions VALUES (?, ?, ?, ?, ?)", sample_data)
conn.commit()

query1 = """
SELECT ProductCategory, SUM(Amount) as TotalRevenue
FROM transactions
GROUP BY ProductCategory
ORDER BY TotalRevenue DESC
"""
df_category = pd.read_sql(query1, conn)

query2 = """
SELECT TransactionDate, SUM(Amount) as DailySales
FROM transactions
GROUP BY TransactionDate
ORDER BY TransactionDate
"""
df_sales = pd.read_sql(query2, conn)

query3 = """
SELECT CustomerID, SUM(Amount) as TotalSpent, COUNT(*) as Transactions
FROM transactions
GROUP BY CustomerID
ORDER BY TotalSpent DESC
"""
df_customers = pd.read_sql(query3, conn)

print("\nRevenue by Category:\n", df_category)
print("\nDaily Sales:\n", df_sales)
print("\nCustomer Spend:\n", df_customers)

plt.figure(figsize=(6,4))
plt.bar(df_category["ProductCategory"], df_category["TotalRevenue"])
plt.title("Revenue by Product Category")
plt.xlabel("Category")
plt.ylabel("Revenue ($)")
plt.show()

plt.figure(figsize=(8,4))
plt.plot(df_sales["TransactionDate"], df_sales["DailySales"], marker="o")
plt.title("Daily Sales Trend")
plt.xlabel("Date")
plt.ylabel("Sales ($)")
plt.xticks(rotation=45)
plt.show()

plt.figure(figsize=(6,4))
plt.bar(df_customers["CustomerID"].astype(str), df_customers["TotalSpent"])
plt.title("Top Customers by Spend")
plt.xlabel("Customer ID")
plt.ylabel("Total Spend ($)")
plt.show()

conn.close()
