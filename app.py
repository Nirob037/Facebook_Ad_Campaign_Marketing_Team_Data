import streamlit as st
import pandas as pd
import plotly.express as px

# ================= PAGE CONFIG =================
st.set_page_config(
    page_title="Marketing Performance Dashboard",
    page_icon="📊",
    layout="wide"
)

# ================= LOAD DATA =================
@st.cache_data
def load_data():
    return pd.read_csv("Final_Marketing Team Data.csv")

df = load_data()

# Ensure numeric columns
numeric_cols = [
    'Reach','Impressions','Frequency','Clicks','Unique Clicks',
    'Unique Link Clicks (ULC)','Click-Through Rate (CTR in %)',
    'Unique Click-Through Rate (Unique CTR in %)',
    'Amount Spent in INR','Cost Percentage',
    'Cost Per Click (CPC)','Cost per Result (CPR)'
]

for col in numeric_cols:
    df[col] = pd.to_numeric(df[col], errors='coerce')

# ================= CUSTOM CSS =================
st.markdown("""
<style>
.kpi-box {
    background-color: white;
    padding: 20px;
    border-radius: 12px;
    box-shadow: 0 6px 16px rgba(0,0,0,0.08);
    text-align: center;
}
.kpi-title {
    font-size: 14px;
    color: #6c757d;
}
.kpi-value {
    font-size: 28px;
    font-weight: 700;
    color: #1f77b4;
}
.section-title {
    font-size: 22px;
    font-weight: 700;
    margin: 20px 0 10px 0;
}
</style>
""", unsafe_allow_html=True)

# ================= TITLE =================
st.markdown(
    "<h1 style='text-align:center;'>📊 Marketing Performance Dashboard</h1>",
    unsafe_allow_html=True
)

# ================= KPI CALCULATIONS =================
total_spend = df['Amount Spent in INR'].sum()
total_clicks = df['Clicks'].sum()
total_impressions = df['Impressions'].sum()
total_reach = df['Reach'].sum()
avg_ctr = df['Click-Through Rate (CTR in %)'].mean()
avg_cpc = df['Cost Per Click (CPC)'].mean()

# ================= KPI CARDS =================
k1, k2, k3, k4, k5, k6 = st.columns(6)

kpis = [
    ("Total Spend", f"₹{total_spend:,.0f}"),
    ("Total Clicks", f"{total_clicks:,}"),
    ("Impressions", f"{total_impressions:,}"),
    ("Reach", f"{total_reach:,}"),
    ("Avg CTR", f"{avg_ctr:.2f}%"),
    ("Avg CPC", f"₹{avg_cpc:.2f}")
]

for col, (title, value) in zip([k1,k2,k3,k4,k5,k6], kpis):
    col.markdown(f"""
    <div class='kpi-box'>
        <div class='kpi-title'>{title}</div>
        <div class='kpi-value'>{value}</div>
    </div>
    """, unsafe_allow_html=True)

# ================= CAMPAIGN PERFORMANCE =================
st.markdown("<div class='section-title'>Campaign Performance</div>", unsafe_allow_html=True)

c1, c2 = st.columns(2)

campaign_clicks = (
    df.groupby("Campaign Name")["Clicks"]
    .sum()
    .sort_values(ascending=False)
    .reset_index()
)

fig1 = px.bar(
    campaign_clicks,
    x="Clicks",
    y="Campaign Name",
    orientation="h",
    title="Clicks by Campaign",
    text="Clicks"
)
fig1.update_layout(yaxis={'categoryorder':'total ascending'})
c1.plotly_chart(fig1, use_container_width=True)

campaign_spend = (
    df.groupby("Campaign Name")["Amount Spent in INR"]
    .sum()
    .reset_index()
)

fig2 = px.pie(
    campaign_spend,
    names="Campaign Name",
    values="Amount Spent in INR",
    hole=0.4,
    title="Spend Distribution by Campaign"
)
c2.plotly_chart(fig2, use_container_width=True)

# ================= AUDIENCE ANALYSIS =================
st.markdown("<div class='section-title'>Audience Insights</div>", unsafe_allow_html=True)

a1, a2 = st.columns(2)

age_clicks = (
    df.groupby("Age")["Clicks"]
    .sum()
    .sort_values(ascending=False)
    .reset_index()
)

fig3 = px.bar(
    age_clicks,
    x="Age",
    y="Clicks",
    title="Clicks by Age Group",
    text="Clicks"
)
a1.plotly_chart(fig3, use_container_width=True)

audience_ctr = (
    df.groupby("Audience")["Click-Through Rate (CTR in %)"]
    .mean()
    .reset_index()
)

fig4 = px.bar(
    audience_ctr,
    x="Audience",
    y="Click-Through Rate (CTR in %)",
    title="Average CTR by Audience",
    text_auto=".2f"
)
a2.plotly_chart(fig4, use_container_width=True)

# ================= GEOGRAPHY =================
st.markdown("<div class='section-title'>Geographic Performance</div>", unsafe_allow_html=True)

df["Country"] = df["Geography"].str.extract(r"\((.*?)\)").fillna("Unknown")

geo = (
    df.groupby("Country")["Clicks"]
    .sum()
    .reset_index()
)

fig5 = px.choropleth(
    geo,
    locations="Country",
    locationmode="country names",
    color="Clicks",
    color_continuous_scale="Blues",
    title="Clicks by Geography"
)

st.plotly_chart(fig5, use_container_width=True)

# ================= FOOTER =================
st.markdown("---")
st.markdown(
    "<p style='text-align:center;'>Created by <strong>Arafat Hossain</strong></p>",
    unsafe_allow_html=True
)
