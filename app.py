import streamlit as st
import pandas as pd
import plotly.express as px

# -------------------------------------------------
# Page Config
# -------------------------------------------------
st.set_page_config(
    page_title="Facebook Ads Performance Dashboard",
    layout="wide",
    initial_sidebar_state="expanded"
)

# -------------------------------------------------
# Column Cleaner
# -------------------------------------------------
def clean_columns(df):
    df.columns = (
        df.columns.str.strip()
        .str.lower()
        .str.replace(" ", "_")
        .str.replace("(", "")
        .str.replace(")", "")
        .str.replace("%", "percent")
    )
    return df

# -------------------------------------------------
# KPI Cards
# -------------------------------------------------
def kpi_card(title, value, icon):
    st.markdown(
        f"""
        <div style="
            background:#ffffff;
            padding:18px;
            border-radius:14px;
            box-shadow:0 4px 12px rgba(0,0,0,0.08);
            text-align:center">
            <div style="font-size:28px">{icon}</div>
            <div style="font-size:14px;color:#6b7280">{title}</div>
            <div style="font-size:24px;font-weight:700">{value}</div>
        </div>
        """,
        unsafe_allow_html=True
    )

# -------------------------------------------------
# Header
# -------------------------------------------------
def header():
    st.markdown(
        """
        <h1 style="text-align:center;">
        📊 Facebook Ad Campaign Performance Dashboard
        </h1>
        <p style="text-align:center;color:gray;">
        Marketing analytics & performance insights
        </p>
        """,
        unsafe_allow_html=True
    )

# -------------------------------------------------
# Sidebar Navigation
# -------------------------------------------------
st.sidebar.title("📌 Navigation")
page = st.sidebar.radio(
    "Go to",
    ["🏠 Home", "📈 Campaign Analysis", "🌍 Geographic Insights"]
)

st.sidebar.markdown("---")
st.sidebar.markdown(
    """
    **Author:** Arafat Hossain  
    📧 ahnirob2114@gmail.com
    """
)

# -------------------------------------------------
# File Upload
# -------------------------------------------------
uploaded_file = st.sidebar.file_uploader("Upload CSV File", type=["csv"])

if uploaded_file is None:
    header()
    st.info("Upload your Facebook Ads CSV file from the sidebar to begin.")
    st.stop()

df = pd.read_csv(uploaded_file)
df = clean_columns(df)

# -------------------------------------------------
# Sidebar Filters (Slicers)
# -------------------------------------------------
st.sidebar.markdown("### 🎛 Filters")

campaign_filter = st.sidebar.multiselect(
    "Campaign",
    options=df["campaign_name"].unique(),
    default=df["campaign_name"].unique()
)

age_filter = st.sidebar.multiselect(
    "Age Group",
    options=df["age"].unique(),
    default=df["age"].unique()
)

geo_filter = st.sidebar.multiselect(
    "Geography",
    options=df["geography"].unique(),
    default=df["geography"].unique()
)

filtered_df = df[
    (df["campaign_name"].isin(campaign_filter)) &
    (df["age"].isin(age_filter)) &
    (df["geography"].isin(geo_filter))
]

# -------------------------------------------------
# HOME PAGE
# -------------------------------------------------
if page == "🏠 Home":
    header()

    # KPI Row
    k1, k2, k3, k4 = st.columns(4)

    with k1:
        kpi_card("Total Spend (INR)", f"{filtered_df['amount_spent_in_inr'].sum():,.0f}", "💰")
    with k2:
        kpi_card("Total Reach", f"{filtered_df['reach'].sum():,.0f}", "👥")
    with k3:
        kpi_card("Total Clicks", f"{filtered_df['clicks'].sum():,.0f}", "🖱️")
    with k4:
        kpi_card(
            "Avg CTR (%)",
            f"{filtered_df['click-through_rate_ctr_in_percent'].mean():.2f}",
            "📈"
        )

    st.markdown("---")

    left, right = st.columns([1, 3])

    # Insight Panel
    with left:
        st.markdown("### 🔍 Key Insights")
        st.write("""
        • Overview of campaign performance  
        • Spend vs engagement efficiency  
        • Audience responsiveness  
        • High-level decision support  
        """)

    # Main Chart
    with right:
        spend_campaign = (
            filtered_df.groupby("campaign_name", as_index=False)
            ["amount_spent_in_inr"].sum()
            .sort_values(by="amount_spent_in_inr", ascending=False)
        )

        fig = px.bar(
            spend_campaign,
            x="campaign_name",
            y="amount_spent_in_inr",
            title="Total Spend by Campaign",
        )
        st.plotly_chart(fig, use_container_width=True)

# -------------------------------------------------
# CAMPAIGN ANALYSIS PAGE
# -------------------------------------------------
elif page == "📈 Campaign Analysis":
    header()

    left, right = st.columns([1, 3])

    with left:
        st.markdown("### 📊 Analysis Notes")
        st.write("""
        • Campaign efficiency comparison  
        • Click performance ranking  
        • Audience behavior by age  
        """)

    with right:
        clicks_campaign = (
            filtered_df.groupby("campaign_name", as_index=False)
            ["clicks"].sum()
            .sort_values(by="clicks", ascending=False)
        )

        fig1 = px.bar(
            clicks_campaign,
            x="campaign_name",
            y="clicks",
            title="Total Clicks by Campaign (Descending)"
        )
        st.plotly_chart(fig1, use_container_width=True)

        ctr_age = (
            filtered_df.groupby("age", as_index=False)
            ["click-through_rate_ctr_in_percent"].mean()
            .sort_values(by="click-through_rate_ctr_in_percent")
        )

        fig2 = px.bar(
            ctr_age,
            x="age",
            y="click-through_rate_ctr_in_percent",
            title="Average CTR by Age Group"
        )
        st.plotly_chart(fig2, use_container_width=True)

# -------------------------------------------------
# GEOGRAPHIC PAGE
# -------------------------------------------------
elif page == "🌍 Geographic Insights":
    header()

    left, right = st.columns([1, 3])

    with left:
        st.markdown("### 🌐 Geographic Insights")
        st.write("""
        • Regional engagement strength  
        • Spend distribution by geography  
        • Market penetration analysis  
        """)

    with right:
        geo_data = (
            filtered_df.groupby("geography", as_index=False)
            ["amount_spent_in_inr"].sum()
        )

        fig = px.choropleth(
            geo_data,
            locations="geography",
            locationmode="country names",
            color="amount_spent_in_inr",
            title="Ad Spend by Geography",
            color_continuous_scale="Blues"
        )
        st.plotly_chart(fig, use_container_width=True)
