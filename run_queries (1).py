"""
DecodeLabs Industrial Training Kit - Batch 2026
Project 3: SQL Data Analysis

Runs every query in queries.sql against orders.db, prints results,
and saves a combined results report (outputs/Project3_SQL_Results.txt)
plus 2 summary charts built from key query outputs.
"""

import sqlite3
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import re
import os

sns.set_theme(style="whitegrid")
DB_FILE = "orders.db"
SQL_FILE = "queries.sql"
OUTPUT_DIR = "outputs"
os.makedirs(OUTPUT_DIR, exist_ok=True)

conn = sqlite3.connect(DB_FILE)

# ------------------------------------------------------------
# Parse queries.sql into individual labeled queries
# ------------------------------------------------------------
with open(SQL_FILE, "r") as f:
    sql_text = f.read()

# Split on numbered comment headers like "-- 1.1 Some description"
pattern = r"-- (\d+\.\d+) (.+?)\n(.*?)(?=(?:-- \d+\.\d+ )|\Z)"
matches = re.findall(pattern, sql_text, flags=re.DOTALL)

results_log = []
results_log.append("=" * 70)
results_log.append("PROJECT 3: SQL DATA ANALYSIS - QUERY RESULTS")
results_log.append("=" * 70)
results_log.append(f"\nDatabase: {DB_FILE} | Table: orders | Total rows: 1,200\n")

key_outputs = {}  # store dataframes we'll chart later

for qid, desc, body in matches:
    # Skip the commented-out failing query block (6.6 contains explanatory text + 2 queries)
    sql_stmt = body.strip()
    # Remove trailing comment-only lines, keep runnable SQL up to first semicolon block
    # For simplicity, run each full statement block (it may contain multiple ; separated statements)
    statements_raw = [s.strip() for s in sql_stmt.split(";") if s.strip()]
    statements = []
    for s in statements_raw:
        # Strip comment-only lines from within the statement
        code_lines = [line for line in s.split("\n") if not line.strip().startswith("--")]
        cleaned = "\n".join(code_lines).strip()
        if cleaned:
            statements.append(cleaned)

    results_log.append("-" * 70)
    results_log.append(f"Query {qid}: {desc.strip()}")
    results_log.append("-" * 70)

    for clean_stmt in statements:
        try:
            df = pd.read_sql_query(clean_stmt + ";", conn)
            results_log.append(df.to_string(index=False, max_rows=20))
            results_log.append("")
            key_outputs[qid] = df
        except Exception as e:
            results_log.append(f"[Skipped - {e}]")
            results_log.append("")

# Save full results log
with open(f"{OUTPUT_DIR}/Project3_SQL_Results.txt", "w") as f:
    f.write("\n".join(results_log))

print("\n".join(results_log[:80]))
print("\n... (full output saved to outputs/Project3_SQL_Results.txt)")

# ------------------------------------------------------------
# CHART 1: Total Revenue by Product (from Query 4.1)
# ------------------------------------------------------------
if "4.1" in key_outputs:
    df = key_outputs["4.1"].sort_values("total_revenue")
    plt.figure(figsize=(9, 5.5))
    colors = ["#1f4e79" if i == len(df) - 1 else "#4682B4" for i in range(len(df))]
    plt.barh(df["Product"], df["total_revenue"], color=colors)
    plt.title("SQL Query Result: Total Revenue by Product (SUM + GROUP BY)")
    plt.xlabel("Total Revenue")
    for i, v in enumerate(df["total_revenue"]):
        plt.text(v + 2000, i, f"{v:,.0f}", va="center", fontsize=9)
    plt.tight_layout()
    plt.savefig(f"{OUTPUT_DIR}/chart1_revenue_by_product.png", dpi=150)
    plt.close()

# ------------------------------------------------------------
# CHART 2: Avg Order Value by Payment Method (from Query 4.2)
# ------------------------------------------------------------
if "4.2" in key_outputs:
    df = key_outputs["4.2"].sort_values("avg_order_value")
    plt.figure(figsize=(8, 5))
    plt.barh(df["PaymentMethod"], df["avg_order_value"], color="#5F9EA0")
    plt.title("SQL Query Result: Average Order Value by Payment Method (AVG + GROUP BY)")
    plt.xlabel("Average Order Value")
    for i, v in enumerate(df["avg_order_value"]):
        plt.text(v + 5, i, f"{v:,.2f}", va="center", fontsize=9)
    plt.tight_layout()
    plt.savefig(f"{OUTPUT_DIR}/chart2_avg_order_value_payment.png", dpi=150)
    plt.close()

# ------------------------------------------------------------
# CHART 3: Monthly Revenue Trend (from Query 4.5)
# ------------------------------------------------------------
if "4.5" in key_outputs:
    df = key_outputs["4.5"]
    plt.figure(figsize=(11, 5))
    plt.plot(df["year_month"], df["total_revenue"], marker="o", color="#4682B4")
    plt.title("SQL Query Result: Monthly Revenue Trend (SUM + GROUP BY)")
    plt.xlabel("Month")
    plt.ylabel("Total Revenue")
    plt.xticks(rotation=90, fontsize=7)
    plt.tight_layout()
    plt.savefig(f"{OUTPUT_DIR}/chart3_monthly_revenue.png", dpi=150)
    plt.close()

conn.close()
print("\nCharts saved to outputs/ folder.")
