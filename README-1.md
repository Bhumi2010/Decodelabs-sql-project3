# Project 3: SQL Data Analysis
### DecodeLabs Industrial Training Kit — Batch 2026

**Author:** Bhumi Singh
**Dataset:** Same cleaned E-commerce Orders dataset from Projects 1 & 2 (1,200 records)
**Database:** SQLite (`orders.db`)

---

## 📌 What This Project Is

This is the third milestone in the DecodeLabs Data Analytics internship track.
After cleaning the data (Project 1) and exploring it visually with Python (Project 2),
Project 3 moves into **SQL** — writing structured queries to filter, group, and
aggregate the same dataset to answer specific business questions directly from a
relational database.

---

## 📂 What's in This Folder

| File | What it is |
|------|-------------|
| `load_database.py` | Loads `dataset.xlsx` into a SQLite database (`orders.db`) |
| `queries.sql` | All 21 SQL queries, organized by topic and commented |
| `run_queries.py` | Executes every query in `queries.sql` and saves results + charts |
| `generate_report_pdf.py` | Builds the polished PDF insights report |
| `orders.db` | The SQLite database itself (queryable directly with any SQL client) |
| `dataset.xlsx` | The cleaned input dataset |
| `outputs/Project3_SQL_Insights_Report.pdf` | Final designed report with queries, results, and insights |
| `outputs/Project3_SQL_Results.txt` | Raw output of every single query |
| `outputs/chart1...chart3 (.png)` | Charts built directly from SQL query results |

---

## 🔍 What the Queries Cover

1. **Basic SELECT** — viewing and projecting columns
2. **WHERE filtering** — equality, comparison, range, IN, pattern-based filters
3. **GROUP BY** — breaking the dataset into categorical buckets (product, status, referral source)
4. **Aggregations** — COUNT, SUM, AVG across products, payment methods, and time
5. **HAVING** — filtering on aggregated results (e.g. products earning over a revenue threshold)
6. **Business queries** — revenue % contribution, repeat customers, top outlier orders, the "Alias Trap" demonstration

---

## 💡 Key Findings (Plain-English Summary)

- **Chair** and **Printer** are virtually tied for the top revenue-generating product.
- **41.4% of all orders** are Cancelled or Returned — calculated independently via SQL, matching the Project 2 Python finding.
- **Credit Card** orders have the highest average value; **Debit Card** the lowest — a ~12.6% spread.
- Revenue is spread fairly evenly across all 7 products (12–15.5% each) — low concentration risk.
- Only **11 customers** placed more than one order — repeat purchase rate is low.
- Coupon usage is associated with slightly *higher* average order value, not lower.

---

## 🧠 A Core SQL Concept Demonstrated: The "Alias Trap"

SQL is **written** as `SELECT → FROM → WHERE → GROUP BY → ORDER BY`, but the
database engine actually **executes** it as:

```
FROM/JOIN → WHERE → GROUP BY → HAVING → SELECT → ORDER BY
```

This means a column alias created in `SELECT` (like `TotalPrice AS rev`) doesn't
exist yet when `WHERE` runs — so this fails:

```sql
SELECT TotalPrice AS rev FROM orders WHERE rev > 1000;  -- ERROR
```

But the same alias works fine in `ORDER BY`, since `ORDER BY` runs after `SELECT`:

```sql
SELECT TotalPrice AS rev
FROM orders
WHERE TotalPrice > 1000   -- repeat the actual expression here
ORDER BY rev DESC;         -- alias works fine here
```

---

## 🛠 How to Reproduce This

```bash
pip install pandas matplotlib seaborn openpyxl reportlab
python load_database.py        # builds orders.db from dataset.xlsx
python run_queries.py          # runs all 21 queries, saves results + charts
python generate_report_pdf.py  # builds the final PDF report
```

You can also open `orders.db` directly in any SQLite client (e.g. DB Browser for
SQLite) and run the queries in `queries.sql` manually.

---

## 🧭 Why This Matters

This project demonstrates core SQL fundamentals expected of a junior data analyst:
filtering rows precisely, aggregating data into business-ready summaries, understanding
*how* the database actually processes a query (not just how to type one), and using
HAVING to ask questions about grouped data rather than raw rows.

---

*Submitted as part of the DecodeLabs Industrial Training Kit, Batch 2026.*
