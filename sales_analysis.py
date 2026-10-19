"""
Sales Data Analysis Project
Tools: Python, Pandas, Matplotlib
Run: python sales_analysis.py
"""
from pathlib import Path
import pandas as pd
import matplotlib.pyplot as plt

DATA_FILE = Path(__file__).with_name("sales_data.csv")
OUTPUT_DIR = Path(__file__).with_name("outputs")
OUTPUT_DIR.mkdir(exist_ok=True)

# 1. Load data
df = pd.read_csv(DATA_FILE, parse_dates=["Date"])

# 2. Clean data
df.columns = df.columns.str.strip()
df = df.drop_duplicates()
df = df.dropna(subset=["Date", "Region", "Product", "Quantity", "UnitPrice"])
df["Quantity"] = pd.to_numeric(df["Quantity"], errors="coerce")
df["UnitPrice"] = pd.to_numeric(df["UnitPrice"], errors="coerce")
df = df.dropna(subset=["Quantity", "UnitPrice"])
df = df[(df["Quantity"] >= 0) & (df["UnitPrice"] >= 0)]

# 3. Create a revenue column
df["Revenue"] = df["Quantity"] * df["UnitPrice"]
df["Month"] = df["Date"].dt.to_period("M").astype(str)

# 4. Calculate key metrics
total_revenue = df["Revenue"].sum()
total_units = df["Quantity"].sum()
number_of_orders = len(df)
average_revenue_per_record = total_revenue / number_of_orders if number_of_orders else 0

print("\n=== SALES DATA ANALYSIS ===")
print(f"Total revenue: ₹{total_revenue:,.2f}")
print(f"Total units sold: {total_units:,.0f}")
print(f"Number of sales records: {number_of_orders}")
print(f"Average revenue per record: ₹{average_revenue_per_record:,.2f}")

# 5. Summaries
product_sales = df.groupby("Product", as_index=False)["Revenue"].sum()
product_sales = product_sales.sort_values("Revenue", ascending=False)
monthly_sales = df.groupby("Month", as_index=False)["Revenue"].sum()
region_sales = df.groupby("Region", as_index=False)["Revenue"].sum().sort_values("Revenue", ascending=False)
category_sales = df.groupby("Category", as_index=False)["Revenue"].sum().sort_values("Revenue", ascending=False)

print("\nRevenue by product:")
print(product_sales.to_string(index=False))
print("\nRevenue by month:")
print(monthly_sales.to_string(index=False))
print("\nRevenue by region:")
print(region_sales.to_string(index=False))
print("\nRevenue by category:")
print(category_sales.to_string(index=False))

# 6. Export summary tables
product_sales.to_csv(OUTPUT_DIR / "revenue_by_product.csv", index=False)
monthly_sales.to_csv(OUTPUT_DIR / "revenue_by_month.csv", index=False)
region_sales.to_csv(OUTPUT_DIR / "revenue_by_region.csv", index=False)
category_sales.to_csv(OUTPUT_DIR / "revenue_by_category.csv", index=False)
df.to_csv(OUTPUT_DIR / "cleaned_sales_data.csv", index=False)

# 7. Create charts
plt.figure(figsize=(8, 5))
plt.bar(product_sales["Product"], product_sales["Revenue"])
plt.title("Revenue by Product")
plt.xlabel("Product")
plt.ylabel("Revenue (₹)")
plt.tight_layout()
plt.savefig(OUTPUT_DIR / "revenue_by_product.png", dpi=150)
plt.close()

plt.figure(figsize=(8, 5))
plt.plot(monthly_sales["Month"], monthly_sales["Revenue"], marker="o")
plt.title("Monthly Revenue Trend")
plt.xlabel("Month")
plt.ylabel("Revenue (₹)")
plt.xticks(rotation=30)
plt.tight_layout()
plt.savefig(OUTPUT_DIR / "monthly_revenue_trend.png", dpi=150)
plt.close()

plt.figure(figsize=(8, 5))
plt.bar(region_sales["Region"], region_sales["Revenue"])
plt.title("Revenue by Region")
plt.xlabel("Region")
plt.ylabel("Revenue (₹)")
plt.tight_layout()
plt.savefig(OUTPUT_DIR / "revenue_by_region.png", dpi=150)
plt.close()

# 8. Simple written insight
top_product = product_sales.iloc[0]["Product"] if not product_sales.empty else "N/A"
top_month = monthly_sales.loc[monthly_sales["Revenue"].idxmax(), "Month"] if not monthly_sales.empty else "N/A"
top_region = region_sales.iloc[0]["Region"] if not region_sales.empty else "N/A"
insights = f"""SALES ANALYSIS INSIGHTS

Total revenue: ₹{total_revenue:,.2f}
Total units sold: {total_units:,.0f}
Highest-revenue product: {top_product}
Highest-revenue month: {top_month}
Highest-revenue region: {top_region}

Note: This is a small sample dataset created for learning. Results are not real company data.
"""
(OUTPUT_DIR / "insights.txt").write_text(insights, encoding="utf-8")
print(f"\nCompleted. Tables, charts, and insights saved in: {OUTPUT_DIR}")
