import streamlit as st
import pandas as pd
import plotly.express as px
from datetime import datetime

# ================= PAGE CONFIG =================
st.set_page_config(
    page_title="Marketing Intelligence Dashboard",
    page_icon="🚀",
    layout="wide"
)

# ================= HEADER =================
st.markdown(
    """
    <h1 style='text-align:center;'>🚀 Marketing Intelligence Dashboard</h1>
    <p style='text-align:center;color:gray;'>Facebook Ad Campaign Performance</p>
    """,
    unsafe_allow_html=True
)

# ================= DATA LOADING =================
@st.cache_data
def load_data(file):
    df = pd.read_csv(file)

    # Clean percentage columns
    pct_cols = [
        "Click-Through Rate (CTR in %)",
        "Unique Click-Through Rate (Unique CTR in %)"
    ]
    for col in pct_cols:
        df[col] = (
            df[col]
            .astype(str)
            .str.replace("%", "", regex=False)
            .astype(float)
        )

    # Ensure numeric columns
    numeric_cols = [
        "Reach", "Impressions", "Frequency", "Clicks",
        "Unique Clicks", "Unique Link Clicks (ULC)",
        "Amount Spent in INR", "Cost Percentage",
        "Cost Per Click (CPC)", "Cost per Result (CPR)"
    ]
    for col in numeric_cols:
        df[col] = pd.to_numeric(df[col], errors="coerce")

    return df

uploaded_file = st.file_uploader("Upload marketing CSV file", type=["csv"])

if not uploaded_file:
    st.warning("Please upload your CSV file to view the dashboard.")
    st.stop()

df = load_data(uploaded_file)

# ================= SIDEBAR FILTERS =================
st.sidebar.header("Filters")

campaign_filter = st.sidebar.multiselect(
    "Campaign",
    options=df["Campaign Name"].unique(),
    default=df["Campaign Name"].unique()
)

audience_filter = st.sidebar.multiselect(
    "Audience",
    options=df["Audience"].unique(),
    default=df["Audience"].unique()
)

df = df[
    (df["Campaign Name"].isin(campaign_filter)) &
    (df["Audience"].isin(audience_filter))
]

# ================= KPI SECTION =================
col1, col2, col3, col4 = st.columns(4)

total_spend = df["Amount Spent in INR"].sum()
total_clicks = df["Clicks"].sum()
total_impressions = df["Impressions"].sum()
avg_ctr = df["Click-Through Rate (CTR in %)"].mean()

col1.metric("💰 Total Spend", f"₹{total_spend:,.0f}")
col2.metric("🖱️ Total Clicks", f"{total_clicks:,}")
col3.metric("👁️ Impressions", f"{total_impressions:,}")
col4.metric("📈 Avg CTR", f"{avg_ctr:.2f}%")

st.markdown("---")

# ================= CHARTS =================
c1, c2 = st.columns(2)

with c1:
    spend_campaign = (
        df.groupby("Campaign Name")["Amount Spent in INR"]
        .sum()
        .sort_values(ascending=False)
        .reset_index()
    )
    fig = px.bar(
        spend_campaign,
        x="Campaign Name",
        y="Amount Spent in INR",
        title="Spend by Campaign",
        text_auto=".2s"
    )
    st.plotly_chart(fig, use_container_width=True)

with c2:
    clicks_age = (
        df.groupby("Age")["Clicks"]
        .sum()
        .sort_values(ascending=False)
        .reset_index()
    )
    fig = px.bar(
        clicks_age,
        x="Age",
        y="Clicks",
        title="Clicks by Age Group",
        text_auto=True
    )
    st.plotly_chart(fig, use_container_width=True)

# ================= GEOGRAPHY =================
st.markdown("### 🌍 Geographic Performance")

def explode_countries(row):
    geo = row["Geography"]
    if "(" in geo:
        countries = geo.split("(")[1].replace(")", "").split(",")
        return [c.strip() for c in countries]
    return [geo]

geo_rows = []
for _, r in df.iterrows():
    for c in explode_countries(r):
        geo_rows.append({
            "Country": c,
            "Clicks": r["Clicks"],
            "Spend": r["Amount Spent in INR"]
        })

geo_df = pd.DataFrame(geo_rows)

geo_summary = geo_df.groupby("Country", as_index=False).sum()

fig = px.choropleth(
    geo_summary,
    locations="Country",
    locationmode="country names",
    color="Clicks",
    title="Clicks by Country",
    color_continuous_scale="Blues"
)
st.plotly_chart(fig, use_container_width=True)

# ================= FOOTER =================
st.markdown("---")
st.markdown(
    f"""
    <div style='text-align:center;color:gray;'>
        <p>Created by <strong>Arafat Hossain</strong></p>
        <p>{datetime.now().year}</p>
    </div>
    """,
    unsafe_allow_html=True
)
