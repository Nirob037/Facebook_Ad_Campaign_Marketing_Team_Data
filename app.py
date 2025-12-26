import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime

# ================= PAGE CONFIG =================
st.set_page_config(
    page_title="Marketing Intelligence Dashboard",
    page_icon="🚀",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# ================= COLOR PALETTE =================
COLORS = {
    "primary": "#1F77B4",
    "secondary": "#2CA02C",
    "accent": "#FF7F0E",
    "neutral": "#7F7F7F",
    "teal": "#17BECF"
}

# ================= CUSTOM CSS =================
st.markdown(
    f"""
    <style>
        .main-header {{
            font-size: 3rem;
            font-weight: 800;
            text-align: center;
            background: linear-gradient(90deg, {COLORS['primary']}, {COLORS['teal']});
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
        }}
        .sub-header {{
            font-size: 1.4rem;
            font-weight: 600;
            color: {COLORS['primary']};
            margin-top: 2rem;
            border-bottom: 2px solid {COLORS['primary']};
            padding-bottom: 0.3rem;
        }}
        .chart-box {{
            background: white;
            padding: 1.2rem;
            border-radius: 10px;
            box-shadow: 0 4px 10px rgba(0,0,0,0.08);
            margin-bottom: 1.5rem;
        }}
        .footer {{
            text-align: center;
            color: {COLORS['neutral']};
            margin-top: 3rem;
            font-size: 0.85rem;
        }}
    </style>
    """,
    unsafe_allow_html=True
)

# ================= TITLE =================
st.markdown('<h1 class="main-header">🚀 Marketing Intelligence Dashboard</h1>', unsafe_allow_html=True)
st.markdown(
    '<p style="text-align:center;color:#666;font-size:1.1rem;">Data-driven insights for smarter decisions</p>',
    unsafe_allow_html=True
)
st.markdown("---")

# ================= DATA LOADING =================
def load_data():
    uploaded_file = st.file_uploader("📤 Upload your marketing CSV file", type=["csv"])

    if uploaded_file is not None:
        df = pd.read_csv(uploaded_file)
        st.success(f"Loaded {len(df)} rows successfully")
        return df

    # Demo data
    st.info("Using demo data. Upload a CSV to analyze real data.")
    demo = {
        "campaign_name": [f"Campaign {i}" for i in range(1, 11)],
        "audience": ["Students", "Professionals"] * 5,
        "age_group": ["18-24", "25-34", "35-44", "18-24", "25-34"] * 2,
        "country": ["USA", "UK", "India", "Canada", "Australia"] * 2,
        "clicks": np.random.randint(200, 1500, 10),
        "impressions": np.random.randint(2000, 15000, 10),
        "amount_spent_inr": np.random.randint(5000, 60000, 10),
        "conversions": np.random.randint(20, 200, 10),
    }
    return pd.DataFrame(demo)

# ================= NAVIGATION =================
def navigation():
    cols = st.columns(4)

    if "page" not in st.session_state:
        st.session_state.page = "overview"

    with cols[0]:
        if st.button("📊 Overview"):
            st.session_state.page = "overview"

    with cols[1]:
        if st.button("🎯 Campaigns"):
            st.session_state.page = "campaigns"

    with cols[2]:
        if st.button("👥 Audience"):
            st.session_state.page = "audience"

    with cols[3]:
        if st.button("🌍 Geography"):
            st.session_state.page = "geo"

    st.markdown("---")

# ================= KPI SECTION =================
def show_kpis(df):
    col1, col2, col3, col4 = st.columns(4)

    total_spend = df["amount_spent_inr"].sum()
    total_clicks = df["clicks"].sum()
    total_impressions = df["impressions"].sum()
    ctr = (total_clicks / total_impressions) * 100 if total_impressions > 0 else 0

    col1.metric("💰 Total Spend", f"₹{total_spend:,.0f}")
    col2.metric("🖱 Total Clicks", f"{total_clicks:,}")
    col3.metric("👁 Impressions", f"{total_impressions:,}")
    col4.metric("📈 CTR", f"{ctr:.2f}%")

# ================= OVERVIEW PAGE =================
def overview_page(df):
    show_kpis(df)

    col1, col2 = st.columns(2)

    with col1:
        st.markdown('<div class="chart-box">', unsafe_allow_html=True)
        fig = px.bar(
            df.groupby("campaign_name")["clicks"].sum().reset_index(),
            x="campaign_name",
            y="clicks",
            title="Campaign Engagements",
            color="clicks",
            color_continuous_scale="Blues"
        )
        st.plotly_chart(fig, use_container_width=True)
        st.markdown("</div>", unsafe_allow_html=True)

    with col2:
        st.markdown('<div class="chart-box">', unsafe_allow_html=True)
        fig = px.pie(
            df,
            values="amount_spent_inr",
            names="audience",
            hole=0.45,
            title="Spend by Audience"
        )
        st.plotly_chart(fig, use_container_width=True)
        st.markdown("</div>", unsafe_allow_html=True)

# ================= CAMPAIGN PAGE =================
def campaign_page(df):
    st.markdown('<div class="sub-header">Campaign Performance</div>', unsafe_allow_html=True)

    campaign = st.selectbox("Select Campaign", df["campaign_name"].unique())
    data = df[df["campaign_name"] == campaign]

    col1, col2 = st.columns(2)

    with col1:
        fig = px.bar(
            data,
            x="age_group",
            y="clicks",
            color="clicks",
            title="Clicks by Age Group"
        )
        st.plotly_chart(fig, use_container_width=True)

    with col2:
        fig = px.scatter(
            data,
            x="amount_spent_inr",
            y="clicks",
            size="conversions",
            color="audience",
            title="Spend vs Clicks"
        )
        st.plotly_chart(fig, use_container_width=True)

# ================= AUDIENCE PAGE =================
def audience_page(df):
    st.markdown('<div class="sub-header">Audience Insights</div>', unsafe_allow_html=True)

    fig = px.sunburst(
        df,
        path=["audience", "age_group"],
        values="clicks",
        title="Audience Segmentation"
    )
    st.plotly_chart(fig, use_container_width=True)

# ================= GEO PAGE =================
def geo_page(df):
    st.markdown('<div class="sub-header">Geographic Performance</div>', unsafe_allow_html=True)

    fig = px.choropleth(
        df.groupby("country")["clicks"].sum().reset_index(),
        locations="country",
        locationmode="country names",
        color="clicks",
        title="Global Engagement Heatmap",
        color_continuous_scale="Viridis"
    )
    st.plotly_chart(fig, use_container_width=True)

# ================= MAIN APP =================
def main():
    df = load_data()
    navigation()

    if st.session_state.page == "overview":
        overview_page(df)
    elif st.session_state.page == "campaigns":
        campaign_page(df)
    elif st.session_state.page == "audience":
        audience_page(df)
    elif st.session_state.page == "geo":
        geo_page(df)

    st.markdown(
        f"""
        <div class="footer">
            <p>Created by <strong>Arafat Hossain</strong></p>
            <p>© {datetime.now().year} Marketing Intelligence Dashboard</p>
        </div>
        """,
        unsafe_allow_html=True
    )

if __name__ == "__main__":
    main()
