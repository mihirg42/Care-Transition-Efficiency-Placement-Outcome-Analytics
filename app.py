import streamlit as st
import pandas as pd
import numpy as np

st.set_page_config(layout="wide")

st.title("Care Transition Efficiency & Placement Analytics")

df = pd.read_csv("HHS_Unaccompanied_Alien_Children_Program.csv")
df["Date"] = pd.to_datetime(df["Date"])
df = df.dropna(how='all')
df['Children in HHS Care'] = df['Children in HHS Care'].str.replace(',', '', regex=False).astype(float)

# KPIs
df["Transfer Efficiency Ratio"] = (
    df["Children transferred out of CBP custody"] /
    (df["Children in CBP custody"] + df["Children transferred out of CBP custody"])
)

df["Discharge Effectiveness Index"] = (
    df["Children discharged from HHS Care"] /
    df["Children in HHS Care"]
)

df["Pipeline Throughput"] = (
    df["Children discharged from HHS Care"] /
    df["Children apprehended and placed in CBP custody"]
)


Transfer_Efficiency_Ratio = (
    df["Children transferred out of CBP custody"].sum() /
    (df["Children in CBP custody"].sum() + df["Children transferred out of CBP custody"].sum())
)

Discharge_Effectiveness_Index = (
    df["Children discharged from HHS Care"].sum() /
    df["Children in HHS Care"].sum()
)

Pipeline_Throughput = (
    df["Children discharged from HHS Care"].sum() /
    df["Children apprehended and placed in CBP custody"].sum()
)

# Sidebar Filters
st.sidebar.header("Filters")
start = st.sidebar.date_input("Start Date", df["Date"].min())
end = st.sidebar.date_input("End Date", df["Date"].max())

filtered = df[(df["Date"] >= pd.to_datetime(start)) &
              (df["Date"] <= pd.to_datetime(end))]

# KPI Cards
col1, col2, col3 = st.columns(3)

col1.metric("Avg Transfer Efficiency",
            round(Transfer_Efficiency_Ratio.mean(), 3))

col2.metric("Avg Discharge Effectiveness",
            round(Discharge_Effectiveness_Index.mean(), 3))

col3.metric("Avg Throughput",
            round(Pipeline_Throughput, 3))

# Charts
st.subheader("Transfer Efficiency Trend")
st.line_chart(filtered.set_index("Date")["Transfer Efficiency Ratio"])

st.subheader("Discharge Effectiveness Trend")
st.line_chart(filtered.set_index("Date")["Discharge Effectiveness Index"])

st.subheader("Pipeline Throughput")
st.line_chart(filtered.set_index("Date")["Pipeline Throughput"])
