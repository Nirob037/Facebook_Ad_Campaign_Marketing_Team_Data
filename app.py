import streamlit as st
import pandas as pd
import plotly.express as px

# ------------------ PAGE CONFIG ------------------
st.set_page_config(
    page_title="Marketing Performance Dashboard",
    page_icon="📊",
    layout="wide"
)

# ------------------ LOAD DATA ------------------
@st.cache_data
def load_data(file):
    df = pd.read_csv(file)

    pct_cols = [
        "Click-Through Rate (CTR in %)",
        "Unique Click-Through Rate (Unique CTR in %)"
    ]
    for col in pct_cols:
        df[col] = (
            df[col].astype(str)
            .str.replace("%", "", regex=False)
            .astype(float)
        )

    num_cols = [
        "Reach","Impressions","Clicks","Unique Clicks",
        "Amount Spent in INR","Cost Per Click (CPC)"
    ]
    for col in num_cols:
        df[col] = pd.to_numeric(df[col], errors="coerce")

    return df

uploaded_file = st.file_uploader("Upload Facebook Ad Campaign CSV", type="csv")
if not uploaded_file:
    st.stop()

df = load_data(uploaded_file)

# ------------------ SIDEBAR ------------------
st.sidebar.title("📍 Navigation")

page = st.sidebar.radio(
    "Go to",
    ["Home", "Campaign Performance", "Audience Insights", "Geographic Analysis"]
)

# Filters
st.sidebar.markdown("### Filters")
campaign = st.sidebar.multiselect(
    "Campaign",
    df["Campaign Name"].unique(),
    default=df["Campaign Name"].unique()
)

df = df[df["Campaign Name"].isin(campaign)]

# ------------------ KPI CARDS ------------------
def kpi_card(title, value):
    st.markdown(
        f"""
        <div style="
            background-color:#111;
            padding:20px;
            border-radius:12px;
            text-align:center;
            box-shadow:0 4px 10px rgba(0,0,0,0.3)">
            <h4 style="color:#bbb;">{title}</h4>
            <h2 style="color:white;">{value}</h2>
        </div>
        """,
        unsafe_allow_html=True
    )

# ================== HOME ==================
if page == "Home":
    st.title("📊 Marketing Overview")

    col1, col2, col3, col4 = st.columns(4)

    col1 = col1.container()
    with col1:
        kpi_card("Total Spend", f"₹{df['Amount Spent in INR'].sum():,.0f}")

    col2 = col2.container()
    with col2:
        kpi_card("Impressions", f"{df['Impressions'].sum():,}")

    col3 = col3.container()
    with col3:
        kpi_card("Clicks", f"{df['Clicks'].sum():,}")

    col4 = col4.container()
    with col4:
        kpi_card("Avg CTR", f"{df['Click-Through Rate (CTR in %)'].mean():.2f}%")

    st.markdown("---")

    trend = df.groupby("Date")["Clicks"].sum().reset_index()
    fig = px.line(
        trend,
        x="Date",
        y="Clicks",
        title="Clicks Trend Over Time",
        markers=True
    )
    st.plotly_chart(fig, use_container_width=True)

# ================== CAMPAIGN ==================
elif page == "Campaign Performance":
    st.title("🎯 Campaign Performance")

    col1, col2 = st.columns(2)

    spend_campaign = df.groupby("Campaign Name")["Amount Spent in INR"].sum().reset_index()
    fig1 = px.bar(
        spend_campaign,
        x="Campaign Name",
        y="Amount Spent in INR",
        title="Spend by Campaign",
        text_auto=True
    )

    ctr_campaign = df.groupby("Campaign Name")["Click-Through Rate (CTR in %)"].mean().reset_index()
    fig2 = px.bar(
        ctr_campaign,
        x="Campaign Name",
        y="Click-Through Rate (CTR in %)",
        title="Average CTR by Campaign",
        text_auto=".2f"
    )

    col1.plotly_chart(fig1, use_container_width=True)
    col2.plotly_chart(fig2, use_container_width=True)

# ================== AUDIENCE ==================
elif page == "Audience Insights":
    st.title("👥 Audience Insights")

    col1, col2 = st.columns(2)

    age_clicks = df.groupby("Age")["Clicks"].sum().reset_index()
    fig1 = px.bar(
        age_clicks,
        x="Age",
        y="Clicks",
        title="Clicks by Age Group"
    )

    gender_spend = df.groupby("Gender")["Amount Spent in INR"].sum().reset_index()
    fig2 = px.pie(
        gender_spend,
        names="Gender",
        values="Amount Spent in INR",
        title="Spend Share by Gender",
        hole=0.4
    )

    col1.plotly_chart(fig1, use_container_width=True)
    col2.plotly_chart(fig2, use_container_width=True)

# ================== GEOGRAPHY ==================
elif page == "Geographic Analysis":
    st.title("🌍 Geographic Performance")

    def extract_countries(x):
        if "(" in x:
            return x.split("(")[1].replace(")", "").split(",")
        return [x]

    rows = []
    for _, r in df.iterrows():
        for c in extract_countries(r["Geography"]):
            rows.append({
                "Country": c.strip(),
                "Clicks": r["Clicks"]
            })

    geo_df = pd.DataFrame(rows)
    geo_sum = geo_df.groupby("Country", as_index=False).sum()

    fig = px.choropleth(
        geo_sum,
        locations="Country",
        locationmode="country names",
        color="Clicks",
        title="Clicks by Country",
        color_continuous_scale="Blues"
    )

    st.plotly_chart(fig, use_container_width=True)
