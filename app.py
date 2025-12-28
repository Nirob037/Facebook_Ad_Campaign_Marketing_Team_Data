import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime

# ================= PAGE CONFIG =================
st.set_page_config(
    page_title="Marketing Performance Dashboard",
    page_icon="🚀",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ================= COLOR PALETTE =================
COLORS = {
    'primary': '#1F77B4',      # Blue
    'secondary': '#2CA02C',    # Green
    'accent': '#FF7F0E',       # Orange
    'warning': '#D62728',      # Red
    'neutral': '#7F7F7F',      # Gray
    'teal': '#17BECF',         # Teal
    'purple': '#9467BD',       # Purple
    'pink': '#E377C2'          # Pink
}

# ================= CSS STYLING =================
st.markdown(f"""
<style>
    .main .block-container {{ 
        padding-top: 2rem; 
        padding-bottom: 2rem; 
    }}
    
    /* Main Header with Gradient */
    .main-header {{
        font-size: 3rem;
        background: linear-gradient(90deg, {COLORS['primary']}, {COLORS['teal']});
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-weight: 800;
        text-align: center;
        margin-bottom: 0.5rem;
    }}
    
    /* Section Headers */
    .section-header {{
        font-size: 1.5rem;
        color: {COLORS['primary']};
        font-weight: 600;
        margin-top: 2rem;
        margin-bottom: 1rem;
        border-bottom: 2px solid {COLORS['primary']};
        padding-bottom: 0.5rem;
    }}
    
    /* KPI Cards */
    .kpi-card {{
        background: white;
        border-radius: 10px;
        padding: 1.5rem;
        box-shadow: 0 4px 12px rgba(0,0,0,0.1);
        border-left: 5px solid {COLORS['primary']};
        margin-bottom: 1rem;
        transition: all 0.3s ease;
    }}
    
    .kpi-card:hover {{
        transform: translateY(-5px);
        box-shadow: 0 8px 25px rgba(0,0,0,0.15);
    }}
    
    .kpi-value {{
        font-size: 2rem;
        font-weight: 700;
        color: {COLORS['primary']};
        margin-bottom: 0.2rem;
    }}
    
    .kpi-label {{
        font-size: 0.9rem;
        color: {COLORS['neutral']};
        text-transform: uppercase;
        letter-spacing: 1px;
    }}
    
    /* Navigation Buttons */
    .nav-btn {{
        background: linear-gradient(135deg, {COLORS['primary']}, {COLORS['teal']});
        color: white;
        border: none;
        padding: 1rem 2rem;
        border-radius: 25px;
        font-weight: 600;
        font-size: 1rem;
        cursor: pointer;
        transition: all 0.3s;
        width: 100%;
        margin-bottom: 1rem;
    }}
    
    .nav-btn:hover {{
        transform: scale(1.05);
        box-shadow: 0 6px 20px rgba(31, 119, 180, 0.3);
    }}
    
    .nav-btn.active {{
        background: linear-gradient(135deg, {COLORS['accent']}, {COLORS['warning']});
    }}
    
    /* Chart Containers */
    .chart-container {{
        background: white;
        border-radius: 10px;
        padding: 1.5rem;
        box-shadow: 0 4px 12px rgba(0,0,0,0.1);
        margin-bottom: 2rem;
    }}
    
    /* Footer */
    .footer {{
        text-align: center;
        color: {COLORS['neutral']};
        padding: 2rem;
        margin-top: 3rem;
        border-top: 1px solid #e0e0e0;
        font-size: 0.9rem;
    }}
    
    .creator-name {{
        color: {COLORS['primary']};
        font-weight: 600;
        font-size: 1.1rem;
    }}
    
    .creator-email {{
        color: {COLORS['teal']};
        text-decoration: none;
    }}
    
    .creator-email:hover {{
        text-decoration: underline;
    }}
    
    /* Status Indicators */
    .status-success {{
        color: {COLORS['secondary']};
        font-weight: 600;
    }}
    
    .status-warning {{
        color: {COLORS['warning']};
        font-weight: 600;
    }}
</style>
""", unsafe_allow_html=True)

# ================= LOAD DATA =================
@st.cache_data
def load_data():
    return pd.read_csv("Final_Marketing Team Data.csv")

df = load_data()

        
        # Clean numeric columns
        numeric_columns = [
            'Reach', 'Impressions', 'Frequency', 'Clicks', 'Unique Clicks',
            'Unique Link Clicks (ULC)', 'Click-Through Rate (CTR in %)',
            'Unique Click-Through Rate (Unique CTR in %)', 'Amount Spent in INR',
            'Cost Percentage', 'Cost Per Click (CPC)', 'Cost per Result (CPR)'
        ]
        
        for col in numeric_columns:
            if col in df.columns:
                # Remove commas and percentage signs
                df[col] = df[col].astype(str).str.replace(',', '').str.replace('%', '')
                # Convert to numeric
                df[col] = pd.to_numeric(df[col], errors='coerce').fillna(0)
        
        return df
        
    except Exception as e:
        st.error(f"❌ **Error loading from GitHub:** {str(e)}")
        st.info("""
        **🛠️ Troubleshooting:**
        1. Check if file exists at: `https://github.com/Nirob037/Marketing-Campaign-Analytics/blob/main/Final_Marketing%20Team%20Data.csv`
        2. Ensure the file is in your GitHub repository
        3. Try the file upload option below
        """)
        return None

def load_data():
    """Main data loading function with GitHub + upload fallback"""
    
    st.markdown("### 📁 Data Source Selection")
    
    # Create tabs for different loading methods
    tab1, tab2 = st.tabs(["🌐 **Load from GitHub**", "📤 **Upload New File**"])
    
    with tab1:
        st.markdown("""
        **Automatically load from your GitHub repository:**
        - File: `Final_Marketing Team Data.csv`
        - Source: Your Marketing-Campaign-Analytics repository
        """)
        
        if st.button("🚀 **Load Data from GitHub**", type="primary", use_container_width=True):
            df = load_data_from_github()
            if df is not None:
                st.session_state['df'] = df
                st.session_state['data_source'] = 'github'
                st.rerun()
    
    with tab2:
        st.markdown("**Upload a new CSV file for analysis:**")
        uploaded_file = st.file_uploader(
            "Choose a CSV file",
            type=['csv'],
            help="Upload your marketing data CSV file"
        )
        
        if uploaded_file is not None:
            try:
                df = pd.read_csv(uploaded_file)
                st.success(f"✅ **File uploaded:** {uploaded_file.name}")
                
                # Clean numeric columns
                numeric_columns = [
                    'Reach', 'Impressions', 'Frequency', 'Clicks', 'Unique Clicks',
                    'Unique Link Clicks (ULC)', 'Click-Through Rate (CTR in %)',
                    'Unique Click-Through Rate (Unique CTR in %)', 'Amount Spent in INR',
                    'Cost Percentage', 'Cost Per Click (CPC)', 'Cost per Result (CPR)'
                ]
                
                for col in numeric_columns:
                    if col in df.columns:
                        df[col] = df[col].astype(str).str.replace(',', '').str.replace('%', '')
                        df[col] = pd.to_numeric(df[col], errors='coerce').fillna(0)
                
                st.session_state['df'] = df
                st.session_state['data_source'] = 'upload'
                st.rerun()
                
            except Exception as e:
                st.error(f"Error loading uploaded file: {str(e)}")
    
    # Return stored data if available
    return st.session_state.get('df', None)

# ================= NAVIGATION =================
def show_navigation():
    """Display navigation buttons"""
    st.markdown("### 📊 Dashboard Navigation")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        if st.button("🏠 **Overview Dashboard**", use_container_width=True,
                    type="primary" if st.session_state.get('page', 'home') == 'home' else "secondary"):
            st.session_state.page = 'home'
    
    with col2:
        if st.button("📈 **Campaign Analytics**", use_container_width=True,
                    type="primary" if st.session_state.get('page', 'home') == 'campaign' else "secondary"):
            st.session_state.page = 'campaign'
    
    with col3:
        if st.button("👥 **Audience Insights**", use_container_width=True,
                    type="primary" if st.session_state.get('page', 'home') == 'audience' else "secondary"):
            st.session_state.page = 'audience'
    
    with col4:
        if st.button("🌍 **Geographic Analysis**", use_container_width=True,
                    type="primary" if st.session_state.get('page', 'home') == 'geography' else "secondary"):
            st.session_state.page = 'geography'
    
    st.markdown("---")

# ================= KPI METRICS =================
def show_kpis(df):
    """Display KPI metrics"""
    st.markdown("### 📊 Key Performance Indicators")
    
    # Calculate metrics
    total_spend = df['Amount Spent in INR'].sum()
    total_clicks = df['Clicks'].sum()
    total_impressions = df['Impressions'].sum()
    total_reach = df['Reach'].sum()
    total_ulc = df['Unique Link Clicks (ULC)'].sum()
    
    # Calculate rates
    ctr = (total_clicks / total_impressions * 100) if total_impressions > 0 else 0
    avg_cpc = (total_spend / total_clicks) if total_clicks > 0 else 0
    conversion_rate = (total_ulc / total_clicks * 100) if total_clicks > 0 else 0
    avg_frequency = df['Frequency'].mean()
    
    # Row 1
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric(
            "💰 Total Investment",
            f"₹{total_spend:,.0f}",
            f"₹{total_spend/len(df):,.0f} avg/campaign"
        )
    
    with col2:
        st.metric(
            "🖱️ Total Clicks",
            f"{total_clicks:,}",
            f"{ctr:.2f}% CTR"
        )
    
    with col3:
        st.metric(
            "👁️ Total Impressions",
            f"{total_impressions:,}",
            f"{total_reach:,} Reach"
        )
    
    with col4:
        st.metric(
            "🎯 Conversions",
            f"{total_ulc:,}",
            f"{conversion_rate:.1f}% rate"
        )
    
    # Row 2
    col5, col6, col7, col8 = st.columns(4)
    
    with col5:
        st.metric(
            "📊 Avg CPC",
            f"₹{avg_cpc:.2f}",
            f"₹{df['Cost Per Click (CPC)'].mean():.2f} direct"
        )
    
    with col6:
        st.metric(
            "🔄 Avg Frequency",
            f"{avg_frequency:.2f}",
            f"{df['Frequency'].median():.2f} median"
        )
    
    with col7:
        st.metric(
            "📈 Avg CTR",
            f"{ctr:.2f}%",
            f"{df['Click-Through Rate (CTR in %)'].mean():.2f}% direct"
        )
    
    with col8:
        campaigns = df['campaign ID'].nunique()
        st.metric(
            "🚀 Active Campaigns",
            f"{campaigns}",
            f"{len(df)} segments"
        )
    
    st.markdown("---")

# ================= HOME PAGE =================
def home_page(df):
    """Home page with overview"""
    st.markdown('<h1 class="main-header">📈 MARKETING TEAM DATA INTELLIGENCE</h1>', unsafe_allow_html=True)
    st.markdown('<p style="text-align: center; color: #666; font-size: 1.2rem;">Data-Driven Insights • Campaign Performance • ROI Optimization</p>', unsafe_allow_html=True)
    
    show_kpis(df)
    
    # Row 1: Main Charts
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown('<div class="chart-container">', unsafe_allow_html=True)
        st.markdown("##### 📊 Top Campaigns by Performance")
        
        # Create performance score
        df['Performance Score'] = (
            df['Click-Through Rate (CTR in %)'] * 0.4 +
            (1 / (df['Cost Per Click (CPC)'] + 0.001)) * 0.3 +
            df['Unique Link Clicks (ULC)'] * 0.3
        )
        
        top_campaigns = df.nlargest(10, 'Performance Score')[['Campaign Name', 'Clicks', 'Click-Through Rate (CTR in %)', 'Cost Per Click (CPC)']]
        
        fig = go.Figure(data=[
            go.Bar(name='Clicks', x=top_campaigns['Campaign Name'], y=top_campaigns['Clicks'], marker_color=COLORS['primary']),
            go.Bar(name='CTR %', x=top_campaigns['Campaign Name'], y=top_campaigns['Click-Through Rate (CTR in %)']*1000, 
                  marker_color=COLORS['secondary'], yaxis='y2')
        ])
        
        fig.update_layout(
            barmode='group',
            yaxis2=dict(
                title='CTR (scaled)',
                overlaying='y',
                side='right'
            ),
            height=400,
            showlegend=True
        )
        
        st.plotly_chart(fig, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)
    
    with col2:
        st.markdown('<div class="chart-container">', unsafe_allow_html=True)
        st.markdown("##### 💰 Investment Distribution")
        
        spend_by_campaign = df.groupby('Campaign Name')['Amount Spent in INR'].sum().nlargest(8).reset_index()
        
        fig = px.pie(
            spend_by_campaign,
            values='Amount Spent in INR',
            names='Campaign Name',
            hole=0.5,
            color_discrete_sequence=px.colors.qualitative.Set3
        )
        
        fig.update_traces(
            textposition='inside',
            textinfo='percent+label',
            marker=dict(line=dict(color='white', width=2))
        )
        
        fig.update_layout(height=400, showlegend=False)
        st.plotly_chart(fig, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)
    
    # Row 2: More Charts
    col3, col4 = st.columns(2)
    
    with col3:
        st.markdown('<div class="chart-container">', unsafe_allow_html=True)
        st.markdown("##### 👥 Audience Analysis")
        
        audience_performance = df.groupby('Audience').agg({
            'Clicks': 'sum',
            'Amount Spent in INR': 'sum',
            'Click-Through Rate (CTR in %)': 'mean'
        }).reset_index()
        
        fig = px.scatter(
            audience_performance,
            x='Amount Spent in INR',
            y='Clicks',
            size='Click-Through Rate (CTR in %)',
            color='Audience',
            hover_name='Audience',
            size_max=60,
            labels={
                'Amount Spent in INR': 'Total Spend (INR)',
                'Clicks': 'Total Clicks',
                'Click-Through Rate (CTR in %)': 'Avg CTR'
            }
        )
        
        fig.update_layout(height=400)
        st.plotly_chart(fig, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)
    
    with col4:
        st.markdown('<div class="chart-container">', unsafe_allow_html=True)
        st.markdown("##### 📈 Efficiency Metrics")
        
        metrics_df = pd.DataFrame({
            'Metric': ['CPC', 'CTR', 'CPR', 'Frequency'],
            'Value': [
                df['Cost Per Click (CPC)'].mean(),
                df['Click-Through Rate (CTR in %)'].mean(),
                df['Cost per Result (CPR)'].mean(),
                df['Frequency'].mean()
            ],
            'Target': [1.5, 0.05, 10, 2.0]
        })
        
        fig = go.Figure()
        
        fig.add_trace(go.Bar(
            x=metrics_df['Metric'],
            y=metrics_df['Value'],
            name='Current',
            marker_color=COLORS['primary']
        ))
        
        fig.add_trace(go.Scatter(
            x=metrics_df['Metric'],
            y=metrics_df['Target'],
            name='Target',
            mode='markers+lines',
            marker=dict(color=COLORS['warning'], size=10),
            line=dict(color=COLORS['warning'], dash='dash')
        ))
        
        fig.update_layout(
            height=400,
            yaxis_title='Value',
            hovermode='x unified'
        )
        
        st.plotly_chart(fig, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)

# ================= CAMPAIGN PAGE =================
def campaign_page(df):
    """Campaign analytics page"""
    st.markdown("### 🎯 Campaign Performance Analytics")
    
    # Campaign selector
    campaigns = df['Campaign Name'].unique()
    selected_campaign = st.selectbox("Select Campaign for Detailed Analysis", campaigns)
    
    campaign_data = df[df['Campaign Name'] == selected_campaign]
    
    if not campaign_data.empty:
        # Campaign metrics
        st.markdown(f"#### 📊 Performance Analysis: **{selected_campaign}**")
        
        cols = st.columns(5)
        metrics = [
            ('Clicks', 'Clicks', f"{campaign_data['Clicks'].sum():,}"),
            ('Spend', 'Amount Spent in INR', f"₹{campaign_data['Amount Spent in INR'].sum():,.0f}"),
            ('CTR', 'Click-Through Rate (CTR in %)', f"{campaign_data['Click-Through Rate (CTR in %)'].mean():.3f}%"),
            ('CPC', 'Cost Per Click (CPC)', f"₹{campaign_data['Cost Per Click (CPC)'].mean():.2f}"),
            ('Conversions', 'Unique Link Clicks (ULC)', f"{campaign_data['Unique Link Clicks (ULC)'].sum():,}")
        ]
        
        for idx, (label, col, value) in enumerate(metrics):
            with cols[idx]:
                st.metric(label, value)
    
    # Campaign comparison charts
    st.markdown("---")
    st.markdown("#### 📈 Campaign Comparison")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown('<div class="chart-container">', unsafe_allow_html=True)
        st.markdown("##### Top Campaigns by ROI Efficiency")
        
        # Calculate ROI (simplified)
        df['ROI_Score'] = (df['Unique Link Clicks (ULC)'] / df['Amount Spent in INR']).replace([np.inf, -np.inf], 0)
        top_roi = df.nlargest(10, 'ROI_Score')[['Campaign Name', 'ROI_Score', 'Amount Spent in INR', 'Unique Link Clicks (ULC)']]
        
        fig = px.bar(
            top_roi,
            x='Campaign Name',
            y='ROI_Score',
            color='Amount Spent in INR',
            color_continuous_scale='Viridis',
            hover_data=['Amount Spent in INR', 'Unique Link Clicks (ULC)'],
            title='ROI Efficiency (Conversions per INR spent)'
        )
        
        fig.update_layout(height=500)
        st.plotly_chart(fig, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)
    
    with col2:
        st.markdown('<div class="chart-container">', unsafe_allow_html=True)
        st.markdown("##### Campaign Performance Matrix")
        
        scatter_data = df.groupby('Campaign Name').agg({
            'Clicks': 'sum',
            'Amount Spent in INR': 'sum',
            'Click-Through Rate (CTR in %)': 'mean'
        }).reset_index()
        
        fig = px.scatter(
            scatter_data,
            x='Amount Spent in INR',
            y='Clicks',
            size='Click-Through Rate (CTR in %)',
            color='Campaign Name',
            hover_name='Campaign Name',
            size_max=50,
            labels={
                'Amount Spent in INR': 'Total Investment (INR)',
                'Clicks': 'Total Engagement',
                'Click-Through Rate (CTR in %)': 'Avg CTR'
            }
        )
        
        fig.update_layout(height=500)
        st.plotly_chart(fig, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)

# ================= AUDIENCE PAGE =================
def audience_page(df):
    """Audience insights page"""
    st.markdown("### 👥 Audience Segmentation Insights")
    
    # Three column layout
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown('<div class="chart-container">', unsafe_allow_html=True)
        st.markdown("##### 🎯 Audience Distribution")
        
        audience_dist = df['Audience'].value_counts().reset_index()
        audience_dist.columns = ['Audience', 'Count']
        
        fig = px.pie(
            audience_dist,
            values='Count',
            names='Audience',
            hole=0.4,
            color_discrete_sequence=[COLORS['primary'], COLORS['secondary']]
        )
        
        fig.update_traces(
            textposition='inside',
            textinfo='percent+label',
            marker=dict(line=dict(color='white', width=2))
        )
        
        fig.update_layout(height=400, showlegend=False)
        st.plotly_chart(fig, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)
    
    with col2:
        st.markdown('<div class="chart-container">', unsafe_allow_html=True)
        st.markdown("##### 📊 Age Group Performance")
        
        age_performance = df.groupby('Age').agg({
            'Clicks': 'sum',
            'Amount Spent in INR': 'sum',
            'Click-Through Rate (CTR in %)': 'mean'
        }).reset_index()
        
        fig = px.bar(
            age_performance,
            x='Age',
            y='Clicks',
            color='Click-Through Rate (CTR in %)',
            color_continuous_scale='Plasma',
            text='Clicks',
            hover_data=['Amount Spent in INR', 'Click-Through Rate (CTR in %)'],
            title='Clicks by Age Group'
        )
        
        fig.update_traces(texttemplate='%{text:,}')
        fig.update_layout(height=400)
        st.plotly_chart(fig, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)
    
    with col3:
        st.markdown('<div class="chart-container">', unsafe_allow_html=True)
        st.markdown("##### 💡 Audience Efficiency")
        
        audience_efficiency = df.groupby('Audience').agg({
            'Cost Per Click (CPC)': 'mean',
            'Click-Through Rate (CTR in %)': 'mean',
            'Unique Link Clicks (ULC)': 'sum'
        }).reset_index()
        
        fig = px.scatter(
            audience_efficiency,
            x='Cost Per Click (CPC)',
            y='Click-Through Rate (CTR in %)',
            size='Unique Link Clicks (ULC)',
            color='Audience',
            hover_name='Audience',
            size_max=40,
            labels={
                'Cost Per Click (CPC)': 'Avg Cost per Click (INR)',
                'Click-Through Rate (CTR in %)': 'Avg CTR (%)',
                'Unique Link Clicks (ULC)': 'Total Conversions'
            }
        )
        
        fig.update_layout(height=400)
        st.plotly_chart(fig, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)

# ================= GEOGRAPHY PAGE =================
def geography_page(df):
    """Geographic analysis page"""
    st.markdown("### 🌍 Geographic Performance Intelligence")
    
    # Extract country from Geography column
    def extract_country(geo):
        if isinstance(geo, str):
            # Clean the geography string
            geo = str(geo).strip()
            # If it contains "Group", extract the group name
            if 'Group' in geo:
                return geo.split('(')[0].strip()
            else:
                # Extract country name
                for country in ['Australia', 'Canada', 'United Kingdom', 'Ghana', 'Nigeria', 
                               'Pakistan', 'United States', 'Nepal', 'Thailand', 'Taiwan', 
                               'India', 'UAE', 'UK', 'USA']:
                    if country in geo:
                        return country
                return geo
        return "Unknown"
    
    df['Country'] = df['Geography'].apply(extract_country)
    
    # Map visualization
    st.markdown('<div class="chart-container">', unsafe_allow_html=True)
    st.markdown("##### 🗺️ Global Performance Map")
    
    geo_data = df.groupby('Country').agg({
        'Clicks': 'sum',
        'Amount Spent in INR': 'sum',
        'Click-Through Rate (CTR in %)': 'mean'
    }).reset_index()
    
    # Country mapping for Plotly
    country_mapping = {
        'United States': 'USA',
        'United Kingdom': 'United Kingdom',
        'Australia': 'Australia',
        'Canada': 'Canada',
        'India': 'India',
        'Nigeria': 'Nigeria',
        'Ghana': 'Ghana',
        'Nepal': 'Nepal',
        'UAE': 'United Arab Emirates',
        'Pakistan': 'Pakistan',
        'Group 1': 'United States',  # Approximate
        'Group 2': 'India'           # Approximate
    }
    
    geo_data['Country_Code'] = geo_data['Country'].map(country_mapping).fillna(geo_data['Country'])
    
    fig = px.choropleth(
        geo_data,
        locations='Country_Code',
        locationmode='country names',
        color='Clicks',
        hover_name='Country',
        hover_data=['Amount Spent in INR', 'Click-Through Rate (CTR in %)'],
        color_continuous_scale='Viridis',
        title='Global Click Distribution'
    )
    
    fig.update_layout(height=500)
    st.plotly_chart(fig, use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Regional performance charts
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown('<div class="chart-container">', unsafe_allow_html=True)
        st.markdown("##### 📊 Top Performing Countries")
        
        top_countries = geo_data.nlargest(10, 'Clicks')
        
        fig = px.bar(
            top_countries,
            x='Country',
            y='Clicks',
            color='Click-Through Rate (CTR in %)',
            color_continuous_scale='Plasma',
            text='Clicks',
            hover_data=['Amount Spent in INR']
        )
        
        fig.update_traces(texttemplate='%{text:,}')
        fig.update_layout(height=400)
        st.plotly_chart(fig, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)
    
    with col2:
        st.markdown('<div class="chart-container">', unsafe_allow_html=True)
        st.markdown("##### 📈 Geographic Efficiency")
        
        fig = px.scatter(
            geo_data,
            x='Amount Spent in INR',
            y='Clicks',
            size='Click-Through Rate (CTR in %)',
            color='Country',
            hover_name='Country',
            size_max=40,
            labels={
                'Amount Spent in INR': 'Total Investment (INR)',
                'Clicks': 'Total Engagement',
                'Click-Through Rate (CTR in %)': 'Avg CTR'
            }
        )
        
        fig.update_layout(height=400)
        st.plotly_chart(fig, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)

# ================= MAIN APP =================
def main():
    # Initialize session state
    if 'page' not in st.session_state:
        st.session_state.page = 'home'
    if 'df' not in st.session_state:
        st.session_state.df = None
    
    # Title and data loading
    st.markdown('<h1 class="main-header">🚀MARKETING DATA DASHBOARD</h1>', unsafe_allow_html=True)
    st.markdown("---")
    
    # Load data if not already loaded
    if st.session_state.df is None:
        df = load_data()
        if df is not None:
            st.session_state.df = df
            st.rerun()
    else:
        df = st.session_state.df
    
    # Display dashboard if data is loaded
    if df is not None:
        # Data source info
        source = st.session_state.get('data_source', 'github')
        if source == 'github':
            st.success("📊 **Data Source:** Loaded from your GitHub repository")
        else:
            st.info("📊 **Data Source:** Uploaded file")
        
        # Show navigation
        show_navigation()
        
        # Show selected page
        if st.session_state.page == 'home':
            home_page(df)
        elif st.session_state.page == 'campaign':
            campaign_page(df)
        elif st.session_state.page == 'audience':
            audience_page(df)
        elif st.session_state.page == 'geography':
            geography_page(df)
    
    # ================= FOOTER =================
    st.markdown("---")
    st.markdown(f"""
    <div class='footer'>
        <h3 style='color: {COLORS['primary']}; margin-bottom: 0.5rem;'>Marketing Intelligence Platform</h3>
        <p style='margin-bottom: 0.2rem;'>Advanced analytics for <strong>Final_Marketing Team Data</strong></p>
        <p style='margin-bottom: 0.2rem;'><span class='creator-name'>Analyst: Arafat Hossain</span></p>
        <p style='margin-bottom: 0.2rem;'><strong>Email:</strong> 
            <a href='mailto:ahnirob2114@gmail.com' class='creator-email'>ahnirob2114@gmail.com</a>
        </p>
        <p style='margin-top: 1rem; font-size: 0.8rem; color: #999;'>
            © {datetime.now().year} Marketing Data Dashboard • All insights are data-driven
        </p>
    </div>
    """, unsafe_allow_html=True)

# Run the app
if __name__ == "__main__":
    main()
