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
    layout="wide"
)

# ================= SIMPLE DATA LOADING =================
@st.cache_data
def load_data():
    """Load the CSV file directly"""
    return pd.read_csv("Final_Marketing Team Data.csv")

try:
    df = load_data()
    st.success(f"✅ Data loaded: {len(df)} rows, {len(df.columns)} columns")
    
    # Display all column names for verification
    with st.expander("🔍 Show Column Names"):
        st.write(df.columns.tolist())
        
except Exception as e:
    st.error(f"❌ Error loading file: {str(e)}")
    st.info("""
    **Troubleshooting:**
    1. Ensure 'Final_Marketing Team Data.csv' is in the same folder as app.py
    2. Check the file name matches exactly
    3. Verify the file is in CSV format
    """)
    st.stop()

# ================= COLOR PALETTE =================
COLORS = {
    'primary': '#1F77B4',      # Blue
    'secondary': '#2CA02C',    # Green
    'accent': '#FF7F0E',       # Orange
    'warning': '#D62728',      # Red
    'teal': '#17BECF',         # Teal
    'purple': '#9467BD'        # Purple
}

# ================= TITLE =================
st.markdown(f"""
<h1 style="
    font-size: 3rem; 
    background: linear-gradient(90deg, {COLORS['primary']}, {COLORS['teal']});
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    font-weight: 800;
    text-align: center;
    margin-bottom: 0.5rem;
">🚀 MARKETING INTELLIGENCE DASHBOARD</h1>
<p style="text-align: center; color: #666; font-size: 1.2rem;">
    Analyzing: <strong>Final_Marketing Team Data.csv</strong>
</p>
""", unsafe_allow_html=True)

st.markdown("---")

# ================= NAVIGATION =================
st.markdown("### 📊 Navigation")

# Initialize session state for page navigation
if 'page' not in st.session_state:
    st.session_state.page = 'overview'

# Navigation buttons in columns
col1, col2, col3, col4 = st.columns(4)

with col1:
    if st.button("🏠 **Overview**", use_container_width=True):
        st.session_state.page = 'overview'

with col2:
    if st.button("📈 **Campaigns**", use_container_width=True):
        st.session_state.page = 'campaigns'

with col3:
    if st.button("👥 **Audience**", use_container_width=True):
        st.session_state.page = 'audience'

with col4:
    if st.button("🌍 **Geography**", use_container_width=True):
        st.session_state.page = 'geography'

st.markdown("---")

# ================= KPI METRICS =================
def show_kpis():
    """Display key metrics"""
    st.markdown("### 📊 Key Performance Indicators")
    
    # Calculate metrics
    total_spend = df['Amount Spent in INR'].sum()
    total_clicks = df['Clicks'].sum()
    total_impressions = df['Impressions'].sum()
    total_ulc = df['Unique Link Clicks (ULC)'].sum()
    
    # Calculate rates
    ctr = (total_clicks / total_impressions * 100) if total_impressions > 0 else 0
    avg_cpc = (total_spend / total_clicks) if total_clicks > 0 else 0
    conversion_rate = (total_ulc / total_clicks * 100) if total_clicks > 0 else 0
    
    # Row 1 of KPIs
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("💰 Total Spend", f"₹{total_spend:,.0f}")
    
    with col2:
        st.metric("🖱️ Total Clicks", f"{total_clicks:,}")
    
    with col3:
        st.metric("👁️ Impressions", f"{total_impressions:,}")
    
    with col4:
        st.metric("📈 CTR", f"{ctr:.2f}%")
    
    # Row 2 of KPIs
    col5, col6, col7, col8 = st.columns(4)
    
    with col5:
        st.metric("🎯 Conversions", f"{total_ulc:,}")
    
    with col6:
        st.metric("💸 Avg CPC", f"₹{avg_cpc:.2f}")
    
    with col7:
        st.metric("📊 Conv. Rate", f"{conversion_rate:.1f}%")
    
    with col8:
        campaigns = df['campaign ID'].nunique()
        st.metric("🚀 Campaigns", f"{campaigns}")
    
    st.markdown("---")

# ================= PAGE 1: OVERVIEW =================
def show_overview():
    """Overview dashboard page"""
    show_kpis()
    
    # Row 1: Two charts
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("##### 📊 Top Campaigns by Clicks")
        # Bar chart
        if 'Campaign Name' in df.columns and 'Clicks' in df.columns:
            campaign_clicks = df.groupby('Campaign Name')['Clicks'].sum().reset_index()
            campaign_clicks = campaign_clicks.sort_values('Clicks', ascending=False).head(10)
            
            fig = px.bar(
                campaign_clicks,
                x='Campaign Name',
                y='Clicks',
                color='Clicks',
                color_continuous_scale='Viridis'
            )
            st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        st.markdown("##### 💰 Spend Distribution")
        # Pie chart
        if 'Campaign Name' in df.columns and 'Amount Spent in INR' in df.columns:
            campaign_spend = df.groupby('Campaign Name')['Amount Spent in INR'].sum().reset_index()
            
            fig = px.pie(
                campaign_spend,
                values='Amount Spent in INR',
                names='Campaign Name',
                hole=0.4,
                color_discrete_sequence=px.colors.qualitative.Set3
            )
            st.plotly_chart(fig, use_container_width=True)
    
    # Row 2: Two more charts
    col3, col4 = st.columns(2)
    
    with col3:
        st.markdown("##### 👥 Audience Performance")
        if 'Audience' in df.columns and 'Clicks' in df.columns:
            audience_clicks = df.groupby('Audience')['Clicks'].sum().reset_index()
            
            fig = px.bar(
                audience_clicks,
                x='Audience',
                y='Clicks',
                color='Clicks',
                color_continuous_scale='Blues'
            )
            st.plotly_chart(fig, use_container_width=True)
    
    with col4:
        st.markdown("##### 📈 CTR Performance")
        if 'Campaign Name' in df.columns and 'Click-Through Rate (CTR in %)' in df.columns:
            ctr_data = df.groupby('Campaign Name')['Click-Through Rate (CTR in %)'].mean().reset_index()
            ctr_data = ctr_data.sort_values('Click-Through Rate (CTR in %)', ascending=False).head(10)
            
            fig = px.bar(
                ctr_data,
                x='Campaign Name',
                y='Click-Through Rate (CTR in %)',
                color='Click-Through Rate (CTR in %)',
                color_continuous_scale='RdYlGn'
            )
            fig.update_traces(texttemplate='%{y:.2f}%', textposition='outside')
            st.plotly_chart(fig, use_container_width=True)

# ================= PAGE 2: CAMPAIGN ANALYTICS =================
def show_campaigns():
    """Campaign analytics page"""
    st.markdown("### 📈 Campaign Analytics")
    
    # Campaign selector
    if 'Campaign Name' in df.columns:
        selected_campaign = st.selectbox("Select Campaign", df['Campaign Name'].unique())
        campaign_data = df[df['Campaign Name'] == selected_campaign]
        
        if not campaign_data.empty:
            # Campaign metrics
            col1, col2, col3, col4 = st.columns(4)
            
            with col1:
                st.metric("Clicks", f"{campaign_data['Clicks'].sum():,}")
            
            with col2:
                st.metric("Spend", f"₹{campaign_data['Amount Spent in INR'].sum():,.0f}")
            
            with col3:
                campaign_ctr = campaign_data['Click-Through Rate (CTR in %)'].mean()
                st.metric("CTR", f"{campaign_ctr:.2f}%")
            
            with col4:
                campaign_cpc = campaign_data['Cost Per Click (CPC)'].mean()
                st.metric("Avg CPC", f"₹{campaign_cpc:.2f}")
    
    # Campaign comparison chart
    st.markdown("---")
    st.markdown("##### 📊 Campaign Comparison")
    
    if 'Campaign Name' in df.columns and 'Clicks' in df.columns:
        campaign_comparison = df.groupby('Campaign Name').agg({
            'Clicks': 'sum',
            'Amount Spent in INR': 'sum',
            'Click-Through Rate (CTR in %)': 'mean'
        }).reset_index()
        
        fig = px.scatter(
            campaign_comparison,
            x='Amount Spent in INR',
            y='Clicks',
            size='Click-Through Rate (CTR in %)',
            color='Campaign Name',
            hover_name='Campaign Name',
            size_max=40
        )
        
        st.plotly_chart(fig, use_container_width=True)

# ================= PAGE 3: AUDIENCE INSIGHTS =================
def show_audience():
    """Audience insights page"""
    st.markdown("### 👥 Audience Insights")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("##### 🎯 Audience Distribution")
        if 'Audience' in df.columns:
            audience_dist = df['Audience'].value_counts().reset_index()
            audience_dist.columns = ['Audience', 'Count']
            
            fig = px.pie(
                audience_dist,
                values='Count',
                names='Audience',
                hole=0.4,
                color_discrete_sequence=[COLORS['primary'], COLORS['secondary']]
            )
            st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        st.markdown("##### 📊 Age Group Analysis")
        if 'Age' in df.columns and 'Clicks' in df.columns:
            age_clicks = df.groupby('Age')['Clicks'].sum().reset_index()
            
            fig = px.bar(
                age_clicks,
                x='Age',
                y='Clicks',
                color='Clicks',
                color_continuous_scale='Plasma'
            )
            st.plotly_chart(fig, use_container_width=True)
    
    # Audience efficiency
    st.markdown("---")
    st.markdown("##### 💡 Audience Efficiency")
    
    if 'Audience' in df.columns and 'Cost Per Click (CPC)' in df.columns and 'Click-Through Rate (CTR in %)' in df.columns:
        audience_efficiency = df.groupby('Audience').agg({
            'Cost Per Click (CPC)': 'mean',
            'Click-Through Rate (CTR in %)': 'mean',
            'Clicks': 'sum'
        }).reset_index()
        
        fig = px.scatter(
            audience_efficiency,
            x='Cost Per Click (CPC)',
            y='Click-Through Rate (CTR in %)',
            size='Clicks',
            color='Audience',
            hover_name='Audience'
        )
        st.plotly_chart(fig, use_container_width=True)

# ================= PAGE 4: GEOGRAPHIC ANALYSIS =================
def show_geography():
    """Geographic analysis page"""
    st.markdown("### 🌍 Geographic Analysis")
    
    # Extract country from Geography column
    def extract_country(geo):
        if isinstance(geo, str):
            # Clean the string
            geo = str(geo).strip()
            # If it's a group, extract group name
            if 'Group' in geo:
                return geo.split('(')[0].strip()
            else:
                # Check for country names
                countries = ['Australia', 'Canada', 'United Kingdom', 'Ghana', 
                           'Nigeria', 'Pakistan', 'United States', 'Nepal', 
                           'Thailand', 'Taiwan', 'India', 'UAE']
                for country in countries:
                    if country in geo:
                        return country
                return geo
        return "Unknown"
    
    df['Country'] = df['Geography'].apply(extract_country)
    
    # Map chart
    st.markdown("##### 🗺️ Geographic Performance")
    
    if 'Country' in df.columns and 'Clicks' in df.columns:
        geo_data = df.groupby('Country').agg({
            'Clicks': 'sum',
            'Amount Spent in INR': 'sum',
            'Click-Through Rate (CTR in %)': 'mean'
        }).reset_index()
        
        # Create a simple mapping for countries
        country_mapping = {
            'United States': 'USA',
            'United Kingdom': 'UK',
            'Australia': 'Australia',
            'Canada': 'Canada',
            'India': 'India',
            'Nigeria': 'Nigeria',
            'Ghana': 'Ghana',
            'Nepal': 'Nepal',
            'UAE': 'United Arab Emirates',
            'Group 1': 'USA',  # Approximate
            'Group 2': 'India'  # Approximate
        }
        
        geo_data['Country_Code'] = geo_data['Country'].map(country_mapping).fillna(geo_data['Country'])
        
        fig = px.choropleth(
            geo_data,
            locations='Country_Code',
            locationmode='country names',
            color='Clicks',
            hover_name='Country',
            hover_data=['Amount Spent in INR', 'Click-Through Rate (CTR in %)'],
            color_continuous_scale='Viridis'
        )
        
        st.plotly_chart(fig, use_container_width=True)
    
    # Top countries bar chart
    st.markdown("##### 📊 Top Performing Countries")
    
    if 'Country' in df.columns and 'Clicks' in df.columns:
        top_countries = df.groupby('Country')['Clicks'].sum().nlargest(10).reset_index()
        
        fig = px.bar(
            top_countries,
            x='Country',
            y='Clicks',
            color='Clicks',
            color_continuous_scale='Plasma'
        )
        st.plotly_chart(fig, use_container_width=True)

# ================= MAIN APP =================
# Show the selected page
if st.session_state.page == 'overview':
    show_overview()
elif st.session_state.page == 'campaigns':
    show_campaigns()
elif st.session_state.page == 'audience':
    show_audience()
elif st.session_state.page == 'geography':
    show_geography()

# ================= FOOTER =================
st.markdown("---")
st.markdown(f"""
<div style="
    text-align: center; 
    color: {COLORS['primary']}; 
    padding: 2rem; 
    margin-top: 3rem; 
    border-top: 1px solid #e0e0e0;
">
    <h3>Marketing Intelligence Dashboard</h3>
    <p>Created by: <strong>Arafat Hossain</strong></p>
    <p>Email: <a href="mailto:ahnirob2114@gmail.com" style="color: {COLORS['teal']};">
        ahnirob2114@gmail.com
    </a></p>
    <p style="font-size: 0.9rem; color: #999; margin-top: 1rem;">
        © {datetime.now().year} | Data Source: Final_Marketing Team Data.csv
    </p>
</div>
""", unsafe_allow_html=True)
