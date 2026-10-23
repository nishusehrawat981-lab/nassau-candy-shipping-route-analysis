# Factory-to-Customer Shipping Route Efficiency Analysis

**Repository name:** `nassau-candy-shipping-route-analysis`

## Project overview
This beginner-friendly data analytics project explores factory-to-customer shipping performance for a candy distributor. It examines shipping cost, transit time, on-time delivery, delays, damage reports, shipping modes, distances, and origin warehouses.

## Dataset
`Nassau_Candy_Shipping_Route_Data.csv`

- 300 shipment records
- One row per shipment
- Includes dates, origin/destination, shipping mode, distance, weight, expected and actual transit time, cost, on-time status, damage status, and delay hours.
- **Important:** This is a synthetic practice dataset created for the project because no original company dataset was attached. It does not represent verified Nassau Candy company operations or actual company performance.

## Questions explored
1. What is the average and median shipping cost?
2. What percentage of shipments arrive on time?
3. Which shipping modes have lower average costs?
4. How do shipping modes compare on transit time and on-time delivery?
5. How many shipments are reported damaged?
6. Which origin warehouses may need further route review?

## Methodology
1. Load and inspect the CSV.
2. Check missing values and duplicate shipment IDs.
3. Calculate summary statistics and KPIs.
4. Group shipments by shipping mode and origin warehouse.
5. Compare cost, transit time, on-time delivery, and damage rates.
6. Translate findings into practical recommendations.

## Key performance indicators
- Total shipments
- Average and median shipping cost
- On-time delivery rate
- Average actual transit hours
- Delayed shipment count and average delay hours
- Shipment damage rate

## Tools
- Python
- pandas
- NumPy
- CSV / spreadsheet software

## How to use
Open the CSV in Excel or Google Sheets. For Python analysis, install pandas and numpy, then load the file:

```python
import pandas as pd

df = pd.read_csv("Nassau_Candy_Shipping_Route_Data.csv")
print(df.head())
print(df.describe(include="all"))
print(df.groupby("Shipping_Mode")["Shipping_Cost_USD"].mean())
```

## Repository description
Analyze shipping route efficiency for a candy distributor using shipment cost, transit time, delivery reliability, delays, and damage indicators. Includes a synthetic CSV dataset and a project report.

## Author
Nishu Sehrawat
