import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(
    page_title="Nassau Candy Shipping Analysis",
    page_icon="📦",
    layout="wide"
)

st.title("📦 Factory-to-Customer Shipping Route Efficiency")
st.subheader("Nassau Candy Distributor | Data Analytics Project")
st.write("Prepared by Nishu Sehrawat")

st.info(
    "This project uses synthetic practice data for demonstration, "
    "not verified data from Nassau Candy."
)

@st.cache_data
def load_data():
    return pd.read_csv("Nassau_Candy_Shipping_Route_Data.csv")

try:
    df = load_data()
except Exception as e:
    st.error("Could not load the CSV file. Make sure the dataset is in the repository.")
    st.stop()

# Convert columns to the correct types
for col in ["Ship_Date", "Delivery_Date"]:
    if col in df.columns:
        df[col] = pd.to_datetime(df[col], errors="coerce")

for col in ["On_Time_Delivery", "Shipment_Damaged"]:
    if col in df.columns:
        df[col] = df[col].astype(str).str.lower().map(
            {"true": True, "false": False, "1": True, "0": False}
        )

# Sidebar filters
st.sidebar.header("Filter Shipments")

if "Shipping_Mode" in df.columns:
    modes = sorted(df["Shipping_Mode"].dropna().unique())
    selected_modes = st.sidebar.multiselect(
        "Shipping mode", modes, default=modes
    )
    df = df[df["Shipping_Mode"].isin(selected_modes)]

if "Origin_Warehouse" in df.columns:
    warehouses = sorted(df["Origin_Warehouse"].dropna().unique())
    selected_warehouses = st.sidebar.multiselect(
        "Origin warehouse", warehouses, default=warehouses
    )
    df = df[df["Origin_Warehouse"].isin(selected_warehouses)]

# Key performance indicators
st.header("📊 Key Performance Indicators")

total_shipments = len(df)
average_cost = df["Shipping_Cost_USD"].mean() if total_shipments else 0
average_transit = df["Actual_Transit_Hours"].mean() if total_shipments else 0

if "On_Time_Delivery" in df.columns and total_shipments:
    on_time_rate = df["On_Time_Delivery"].mean() * 100
else:
    on_time_rate = 0

if "Shipment_Damaged" in df.columns and total_shipments:
    damage_rate = df["Shipment_Damaged"].mean() * 100
else:
    damage_rate = 0

c1, c2, c3, c4 = st.columns(4)
c1.metric("Total Shipments", f"{total_shipments:,}")
c2.metric("Average Shipping Cost", f"${average_cost:,.2f}")
c3.metric("Average Transit Time", f"{average_transit:.1f} hours")
c4.metric("On-Time Delivery", f"{on_time_rate:.1f}%")

st.metric("Damaged Shipment Rate", f"{damage_rate:.1f}%")

# Shipping cost by mode
st.header("🚚 Shipping Mode Analysis")

if "Shipping_Mode" in df.columns:
    mode_summary = df.groupby("Shipping_Mode", as_index=False).agg(
        Shipments=("Shipment_ID", "count"),
        Average_Cost=("Shipping_Cost_USD", "mean"),
        Average_Transit=("Actual_Transit_Hours", "mean")
    )

    fig = px.bar(
        mode_summary,
        x="Shipping_Mode",
        y="Average_Cost",
        color="Shipping_Mode",
        title="Average Shipping Cost by Mode",
        labels={"Average_Cost": "Average Cost (USD)"}
    )
    st.plotly_chart(fig, use_container_width=True)

    fig2 = px.bar(
        mode_summary,
        x="Shipping_Mode",
        y="Average_Transit",
        color="Shipping_Mode",
        title="Average Transit Time by Shipping Mode",
        labels={"Average_Transit": "Transit Time (Hours)"}
    )
    st.plotly_chart(fig2, use_container_width=True)

# Delivery performance
st.header("⏱️ Delivery Performance")

if "On_Time_Delivery" in df.columns and "Shipping_Mode" in df.columns:
    delivery_summary = df.groupby("Shipping_Mode", as_index=False).agg(
        On_Time_Rate=("On_Time_Delivery", "mean")
    )
    delivery_summary["On_Time_Rate"] *= 100

    fig3 = px.bar(
        delivery_summary,
        x="Shipping_Mode",
        y="On_Time_Rate",
        color="Shipping_Mode",
        title="On-Time Delivery Rate by Shipping Mode",
        labels={"On_Time_Rate": "On-Time Delivery (%)"}
    )
    st.plotly_chart(fig3, use_container_width=True)

# Distance and cost
st.header("📍 Route and Cost Analysis")

if "Distance_Miles" in df.columns:
    fig4 = px.scatter(
        df,
        x="Distance_Miles",
        y="Shipping_Cost_USD",
        color="Shipping_Mode" if "Shipping_Mode" in df.columns else None,
        hover_data=["Destination_City"] if "Destination_City" in df.columns else None,
        title="Shipping Cost vs Distance"
    )
    st.plotly_chart(fig4, use_container_width=True)

# Destination summary
if "Destination_City" in df.columns:
    st.subheader("Shipping Performance by Destination")
    destination_summary = df.groupby("Destination_City", as_index=False).agg(
        Shipments=("Shipping_Cost_USD", "count"),
        Average_Cost=("Shipping_Cost_USD", "mean"),
        Average_Transit=("Actual_Transit_Hours", "mean")
    ).sort_values("Average_Cost", ascending=False)

    st.dataframe(destination_summary, use_container_width=True)

# Raw data
with st.expander("View shipment data"):
    st.dataframe(df, use_container_width=True)

st.success("Dashboard loaded successfully!")
st.caption("Created by Nishu Sehrawat | Data Analytics Project")
