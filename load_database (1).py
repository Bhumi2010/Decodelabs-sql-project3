"""
DecodeLabs Industrial Training Kit - Batch 2026
Project 3: SQL Data Analysis

This script loads the cleaned e-commerce dataset (from Project 1/2) into a
SQLite database (orders.db), creating a single `orders` table that all
SQL queries in this project run against.
"""

import pandas as pd
import sqlite3

INPUT_FILE = "dataset.xlsx"
DB_FILE = "orders.db"

df = pd.read_excel(INPUT_FILE)

# Ensure correct types
df["Date"] = pd.to_datetime(df["Date"]).dt.strftime("%Y-%m-%d")
df["Quantity"] = df["Quantity"].astype(int)
df["ItemsInCart"] = df["ItemsInCart"].astype(int)
df["UnitPrice"] = df["UnitPrice"].astype(float)
df["TotalPrice"] = df["TotalPrice"].astype(float)

conn = sqlite3.connect(DB_FILE)
df.to_sql("orders", conn, if_exists="replace", index=False)

# Quick sanity check
cur = conn.cursor()
cur.execute("SELECT COUNT(*) FROM orders;")
print("Rows loaded into 'orders' table:", cur.fetchone()[0])

cur.execute("PRAGMA table_info(orders);")
print("\nSchema:")
for col in cur.fetchall():
    print(f"  {col[1]} ({col[2]})")

conn.close()
print(f"\nDatabase saved to {DB_FILE}")
