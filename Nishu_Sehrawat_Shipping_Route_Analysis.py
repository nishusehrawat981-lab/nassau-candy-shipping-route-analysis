"""
Factory-to-Customer Shipping Route Efficiency Analysis
Author: Nishu Sehrawat

Run in Colab: use the .ipynb notebook for upload prompts and step-by-step sections.
Run locally: put the CSV in the same folder as this script, then run:
    python Nishu_Sehrawat_Shipping_Route_Analysis.py

NOTE: The attached dataset is synthetic practice data, not verified company data.
"""
from pathlib import Path
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

sns.set_theme(style="whitegrid")
CSV_PATH = Path("Nassau_Candy_Shipping_Route_Data.csv")
OUTPUT_DIR = Path("shipping_analysis_outputs")
OUTPUT_DIR.mkdir(exist_ok=True)

df = pd.read_csv(CSV_PATH)
for col in ["Ship_Date", "Delivery_Date"]:
    df[col] = pd.to_datetime(df[col], errors="coerce")
for col in ["Distance_Miles", "Weight_kg", "Expected_Transit_Hours", "Actual_Transit_Hours", "Shipping_Cost_USD", "Delay_Hours"]:
    df[col] = pd.to_numeric(df[col], errors="coerce")
df = df.drop_duplicates(subset="Shipment_ID").copy()
df["Is_Delayed"] = df["Delay_Hours"] > 0

kpi_summary = pd.DataFrame({
    "KPI": ["Total shipments", "Average shipping cost (USD)", "Median shipping cost (USD)",
            "Average actual transit time (hours)", "On-time delivery rate (%)",
            "Delayed shipments", "Damaged shipments", "Shipment damage rate (%)"],
    "Value": [len(df), round(df["Shipping_Cost_USD"].mean(), 2),
              round(df["Shipping_Cost_USD"].median(), 2), round(df["Actual_Transit_Hours"].mean(), 2),
              round(df["On_Time_Delivery"].eq("Yes").mean()*100, 2), int(df["Is_Delayed"].sum()),
              int(df["Shipment_Damaged"].eq("Yes").sum()), round(df["Shipment_Damaged"].eq("Yes").mean()*100, 2)]
})
mode_summary = df.groupby("Shipping_Mode").agg(
    Shipments=("Shipment_ID", "count"),
    Average_Cost_USD=("Shipping_Cost_USD", "mean"),
    Average_Transit_Hours=("Actual_Transit_Hours", "mean"),
    On_Time_Rate_Percent=("On_Time_Delivery", lambda x: (x == "Yes").mean()*100),
    Damage_Rate_Percent=("Shipment_Damaged", lambda x: (x == "Yes").mean()*100)
).round(2).reset_index()

warehouse_summary = df.groupby("Origin_Warehouse").agg(
    Shipments=("Shipment_ID", "count"),
    Average_Cost_USD=("Shipping_Cost_USD", "mean"),
    On_Time_Rate_Percent=("On_Time_Delivery", lambda x: (x == "Yes").mean()*100),
    Average_Transit_Hours=("Actual_Transit_Hours", "mean")
).round(2).reset_index()

destination_summary = df.groupby("Destination_City").agg(
    Shipments=("Shipment_ID", "count"),
    Average_Cost_USD=("Shipping_Cost_USD", "mean"),
    On_Time_Rate_Percent=("On_Time_Delivery", lambda x: (x == "Yes").mean()*100)
).round(2).reset_index()

print("\\nOVERALL KPIs")
print(kpi_summary.to_string(index=False))
print("\\nSHIPPING MODE SUMMARY")
print(mode_summary.to_string(index=False))
print("\\nWAREHOUSE SUMMARY")
print(warehouse_summary.to_string(index=False))
print("\\nDESTINATION SUMMARY")
print(destination_summary.to_string(index=False))

kpi_summary.to_csv(OUTPUT_DIR / "overall_kpis.csv", index=False)
mode_summary.to_csv(OUTPUT_DIR / "shipping_mode_summary.csv", index=False)
warehouse_summary.to_csv(OUTPUT_DIR / "warehouse_summary.csv", index=False)
destination_summary.to_csv(OUTPUT_DIR / "destination_summary.csv", index=False)

plt.figure(figsize=(9, 5))
sns.barplot(data=df, x="Shipping_Mode", y="Shipping_Cost_USD", errorbar=None)
plt.title("Average Shipping Cost by Shipping Mode")
plt.xlabel("Shipping Mode")
plt.ylabel("Average Shipping Cost (USD)")
plt.tight_layout()
plt.savefig(OUTPUT_DIR / "average_cost_by_mode.png", dpi=150)
plt.show()

plt.figure(figsize=(9, 5))
sns.barplot(data=mode_summary, x="Shipping_Mode", y="On_Time_Rate_Percent", errorbar=None)
plt.title("On-Time Delivery Rate by Shipping Mode")
plt.xlabel("Shipping Mode")
plt.ylabel("On-Time Delivery (%)")
plt.tight_layout()
plt.savefig(OUTPUT_DIR / "on_time_rate_by_mode.png", dpi=150)
plt.show()

print("\\nAnalysis outputs saved to:", OUTPUT_DIR.resolve())
