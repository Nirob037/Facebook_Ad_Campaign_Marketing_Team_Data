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
    'primary': '#1F77B4',
    'secondary': '#2CA02C',
    'accent': '#FF7F0E',
    'warning': '#D62728',
    'neutral': '#7F7F7F',
    'teal': '#17BECF',
    'purple': '#9467BD',
    'pink': '#E377C2'
}

# ================= CSS STYLING =================
st.markdown(f"""
<style>
    .main .block-container {{ padding-top: 2rem; padding-bottom: 2rem; }}
    .main-header {{ font-size: 3rem; font-weight: 800; text-align: center; margin-bottom: 0.5rem; }}
    .kpi-card {{
        background: white; border-radius: 10px; padding: 1.5rem; box-shadow: 0 4px 12px rgba(0,0,0,0.1);
        border-left: 5px solid {COLORS['primary']}; margin-bottom: 1rem;
    }}
    .kpi-value {{ font-size: 2rem; font-weight: 700; color: {COLORS['primary']}; }}
    .nav-button {{
        background: linear-gradient(135deg, {COLORS['primary']}, {COLORS['teal']});
        color: white; border: none; padding: 0.8rem; border-radius: 20px;
        font-weight: 600; font-size: 1rem; cursor: pointer; width: 100%; margin-bottom: 0.5rem;
    }}
    .chart-container {{
        background: white; border-radius: 10px; padding: 1rem; box-shadow: 0 4px 12px rgba(0,0,0,0.1); margin-bottom: 2rem;
    }}
    .footer {{ text-align:center; color:{COLORS['neutral']}; padding:2rem; margin-top:3rem; border-top:1px solid #e0e0e0; font-size:0.9rem; }}
</style>
""", unsafe_allow_html=True)

# ================= DATA LOADING =================
@st.cache_data
def load_data():
    uploaded_file = st.file_uploader("📤 Upload your marketing CSV file", type=["csv"])
    if uploaded_file is not None:
        df = pd.read_csv(uploaded_file)
        
        # Normalize column names to lowercase & underscore
        df.columns = [c.strip().lower().replace(" ", "_") for c in df.columns]
        
        # List of numeric columns
        numeric_cols = [
            "reach", "impressions", "clicks", "unique_clicks", "unique_link_clicks_(ulc)",
            "click-through_rate_(ctr_in_%)", "unique_click-through_rate_(unique_ctr_in_%)",
            "amount_spent_in_inr", "cost_percentage", "cost_per_click_(cpc)", "cost_per_result_(cpr)"
        ]
        
        # Clean numeric columns
        for col in numeric_cols:
            if col in df.columns:
                df[col] = df[col].astype(str).str.replace(",", "").str.replace("%", "")
                df[col] = pd.to_numeric(df[col], errors="coerce").fillna(0)
                
        return df
    else:
        st.info("📝 Upload your CSV for real analysis or use demo data")
        demo_data = {
            'campaign_id': [f'Campaign_{i}' for i in range(1, 11)],
            'campaign_name': [f'SHU_Campaign_{i}' for i in range(1, 11)],
            'audience': ['Students','Educators']*5,
            'age': ['18-24','25-34','35-44','18-24','25-34']*2,
            'geography': ['USA','UK','India','Australia','Canada']*2,
            'clicks': np.random.randint(100,1000,10),
            'impressions': np.random.randint(1000,10000,10),
            'amount_spent_in_inr': np.random.randint(1000,50000,10),
            'conversions': np.random.randint(10,100,10)
        }
        return pd.DataFrame(demo_data)

# ================= NAVIGATION =================
def show_navigation():
    st.markdown("### Navigation")
    pages = ["Home", "Campaign Analytics", "Audience Insights", "Geography"]
    for page in pages:
        if st.button(page, key=page):
            st.session_state["page"] = page
            st.experimental_rerun()

# ================= KPI CARDS =================
def show_kpis(df):
    col1, col2, col3, col4 = st.columns(4)
    total_spend = df["amount_spent_in_inr"].sum() if "amount_spent_in_inr" in df.columns else 0
    total_clicks = df["clicks"].sum() if "clicks" in df.columns else 0
    total_impressions = df["impressions"].sum() if "impressions" in df.columns else 0
    ctr = (total_clicks/total_impressions*100) if total_impressions>0 else 0
    avg_cpc = (total_spend/total_clicks) if total_clicks>0 else 0
    roi = (total_clicks*10/total_spend*100) if total_spend>0 else 0
    
    with col1: st.markdown(f"<div class='kpi-card'>💰<div class='kpi-value'>₹{total_spend:,.0f}</div>Total Spend</div>", unsafe_allow_html=True)
    with col2: st.markdown(f"<div class='kpi-card'>🖱️<div class='kpi-value'>{total_clicks:,}</div>Total Clicks</div>", unsafe_allow_html=True)
    with col3: st.markdown(f"<div class='kpi-card'>👁️<div class='kpi-value'>{total_impressions:,}</div>Impressions</div>", unsafe_allow_html=True)
    with col4: st.markdown(f"<div class='kpi-card'>📈<div class='kpi-value'>{ctr:.2f}%</div>CTR</div>", unsafe_allow_html=True)

# ================= PAGES =================
def home_page(df):
    st.markdown('<h1 class="main-header">🚀 Marketing Intelligence Dashboard</h1>', unsafe_allow_html=True)
    show_kpis(df)
    
    st.markdown("### Monthly Trend")
    months = ['Jan','Feb','Mar','Apr','May','Jun']
    clicks_trend = np.random.randint(500,2000,6)
    spend_trend = np.random.randint(10000,50000,6)
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=months,y=clicks_trend,name="Clicks",line=dict(color=COLORS['primary'],width=3)))
    fig.add_trace(go.Scatter(x=months,y=spend_trend/100,name="Investment (scaled)",line=dict(color=COLORS['accent'],width=3,dash='dash'),yaxis='y2'))
    fig.update_layout(hovermode='x unified', yaxis2=dict(title='Investment', overlaying='y', side='right'), height=400)
    st.plotly_chart(fig, use_container_width=True)
    
    st.markdown("### Top Campaigns by Clicks")
    if "campaign_name" in df.columns and "clicks" in df.columns:
        top_campaigns = df.groupby("campaign_name")["clicks"].sum().sort_values(ascending=False).reset_index()
        fig = px.bar(top_campaigns.head(10), x="clicks", y="campaign_name", orientation="h", color="clicks", color_continuous_scale="Blues", text="clicks")
        fig.update_layout(yaxis={"categoryorder":"total ascending"}, height=400)
        st.plotly_chart(fig, use_container_width=True)

def campaign_page(df):
    st.markdown("### Campaign Analytics")
    if "campaign_name" in df.columns:
        selected_campaign = st.selectbox("Select Campaign", df["campaign_name"].unique())
        campaign_data = df[df["campaign_name"]==selected_campaign]
        st.write(campaign_data)

def audience_page(df):
    st.markdown("### Audience Insights")
    if "audience" in df.columns and "clicks" in df.columns:
        audience_data = df.groupby("audience")["clicks"].sum().reset_index()
        fig = px.pie(audience_data, values="clicks", names="audience", hole=0.4, color_discrete_sequence=[COLORS['primary'], COLORS['secondary'], COLORS['accent']])
        st.plotly_chart(fig, use_container_width=True)

def geography_page(df):
    st.markdown("### Geographic Intelligence")
    if "geography" in df.columns and "clicks" in df.columns:
        geo_data = df.groupby("geography")["clicks"].sum().reset_index()
        fig = px.choropleth(geo_data, locations="geography", locationmode="country names", color="clicks", hover_name="geography", color_continuous_scale="Viridis")
        st.plotly_chart(fig, use_container_width=True)

# ================= MAIN =================
def main():
    if "page" not in st.session_state: st.session_state["page"] = "Home"
    df = load_data()
    if df is not None:
        show_navigation()
        if st.session_state["page"]=="Home": home_page(df)
        elif st.session_state["page"]=="Campaign Analytics": campaign_page(df)
        elif st.session_state["page"]=="Audience Insights": audience_page(df)
        elif st.session_state["page"]=="Geography": geography_page(df)
    
    st.markdown(f"<div class='footer'>© {datetime.now().year} | Author: Arafat Hossain</div>", unsafe_allow_html=True)

if __name__=="__main__":
    main()
