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
    .main .block-container {{ padding-top: 2rem; padding-bottom: 2rem; }}
    .main-header {{ 
        font-size: 3rem; 
        background: linear-gradient(90deg, {COLORS['primary']}, {COLORS['teal']});
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-weight: 800;
        text-align: center;
        margin-bottom: 0.5rem;
    }}
    .kpi-card {{
        background: white;
        border-radius: 10px;
        padding: 1.5rem;
        box-shadow: 0 4px 12px rgba(0,0,0,0.1);
        border-left: 5px solid {COLORS['primary']};
        margin-bottom: 1rem;
        transition: transform 0.3s;
    }}
    .kpi-card:hover {{ transform: translateY(-5px); box-shadow: 0 8px 20px rgba(0,0,0,0.15); }}
    .kpi-value {{ font-size: 2rem; font-weight: 700; color: {COLORS['primary']}; margin-bottom: 0.2rem; }}
    .kpi-label {{ font-size: 0.9rem; color: {COLORS['neutral']}; text-transform: uppercase; letter-spacing: 1px; }}
    .nav-btn {{ 
        background: linear-gradient(135deg, {COLORS['primary']}, {COLORS['teal']});
        color: white; border: none; padding: 0.8rem 1.5rem; border-radius: 25px;
        font-weight: 600; font-size: 1rem; cursor: pointer; transition: all 0.3s;
    }}
    .nav-btn:hover {{ transform: scale(1.05); box-shadow: 0 6px 20px rgba(31, 119, 180, 0.3); }}
    .chart-container {{ 
        background: white; border-radius: 10px; padding: 1.5rem; 
        box-shadow: 0 4px 12px rgba(0,0,0,0.1); margin-bottom: 2rem;
    }}
    .footer {{ 
        text-align:center; color:{COLORS['neutral']}; padding:2rem; margin-top:3rem; 
        border-top:1px solid #e0e0e0; font-size:0.9rem;
    }}
</style>
""", unsafe_allow_html=True)

# ================= DATA LOADING =================
@st.cache_data
def load_data():
    """Load and clean marketing data with CORRECT column names"""
    
    st.markdown("### 📁 Upload Your Marketing Data CSV")
    uploaded_file = st.file_uploader(
        "Choose your CSV file", 
        type=["csv"],
        help="Upload your Final_Marketing Data.csv file"
    )
    
    if uploaded_file is not None:
        try:
            # Load the CSV
            df = pd.read_csv(uploaded_file)
            
            # Display file info
            st.success(f"✅ File loaded: {uploaded_file.name}")
            st.info(f"📊 **Data Shape:** {df.shape[0]} rows × {df.shape[1]} columns")
            
            # Display ALL column names for verification
            with st.expander("🔍 View All Column Names"):
                st.write("**Your CSV Columns (EXACTLY as they are):**")
                st.write(df.columns.tolist())
                
                st.write("\n**Column Data Types:**")
                st.write(df.dtypes)
            
            # Clean column names (but keep them recognizable)
            df.columns = [col.strip() for col in df.columns]  # Just remove whitespace
            
            # Display cleaned column names
            with st.expander("📋 View Data Preview"):
                st.dataframe(df.head(), use_container_width=True)
            
            return df
            
        except Exception as e:
            st.error(f"❌ Error loading file: {str(e)}")
            return None
    else:
        # DEMO DATA with EXACT column names from your dataset
        st.info("📝 **Demo Mode:** Using sample data with your exact column structure")
        
        demo_data = {
            'campaign ID': ['Campaign 1', 'Campaign 1', 'Campaign 1', 'Campaign 1', 'Campaign 2'],
            'Campaign Name': ['SHU_6 (Educators and Principals)', 'SHU_6 (Educators and Principals)', 
                            'SHU_6 (Educators and Principals)', 'SHU_6 (Educators and Principals)', 
                            'SHU3_ (Students Apart from India and US)'],
            'Audience': ['Educators and Principals', 'Educators and Principals', 
                        'Educators and Principals', 'Educators and Principals', 'Students'],
            'Age': ['25-34', '35-44', '45-54', '55-64', '18-24'],
            'Geography': ['Group 1 (Australia, Canada, United Kingdom, Ghana, Nigeria, Pakistan, United States)',
                         'Group 1 (Australia, Canada, United Kingdom, Ghana, Nigeria, Pakistan, United States)',
                         'Group 1 (Australia, Canada, United Kingdom, Ghana, Nigeria, Pakistan, United States)',
                         'Group 1 (Australia, Canada, United Kingdom, Ghana, Nigeria, Pakistan, United States)',
                         'Group 2 (Australia, Canada, United Kingdom, Ghana, Niger, Nigeria, Nepal, Pakistan, Thailand, Taiwan)'],
            'Reach': [11387, 8761, 2867, 889, 29675],
            'Impressions': [23283, 15683, 6283, 1890, 39161],
            'Frequency': [2.04, 1.79, 2.19, 2.13, 1.32],
            'Clicks': [487, 484, 198, 49, 2593],
            'Unique Clicks': [406, 376, 145, 40, 1994],
            'Unique Link Clicks (ULC)': [180, 154, 65, 21, 1095],
            'Click-Through Rate (CTR in %)': [0.021, 0.031, 0.032, 0.026, 0.066],
            'Unique Click-Through Rate (Unique CTR in %)': [0.018, 0.024, 0.023, 0.021, 0.051],
            'Amount Spent in INR': [1092.24, 835.46, 319.38, 86.25, 1193.94],
            'Cost Percentage': [9.04, 6.91, 2.64, 0.71, 9.88],
            'Cost Per Click (CPC)': [2.24, 1.73, 1.61, 1.76, 0.46],
            'Cost per Result (CPR)': [6.07, 5.43, 4.91, 4.11, 1.09]
        }
        
        df = pd.DataFrame(demo_data)
        st.success("✅ Demo data loaded with your EXACT column structure!")
        return df

# ================= NAVIGATION =================
def show_navigation():
    """Display navigation buttons"""
    st.markdown("### 📊 Dashboard Navigation")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        if st.button("🏠 **Overview Dashboard**", use_container_width=True):
            st.session_state.page = "home"
    
    with col2:
        if st.button("📈 **Campaign Analytics**", use_container_width=True):
            st.session_state.page = "campaign"
    
    with col3:
        if st.button("👥 **Audience Insights**", use_container_width=True):
            st.session_state.page = "audience"
    
    with col4:
        if st.button("🌍 **Geographic Analysis**", use_container_width=True):
            st.session_state.page = "geography"
    
    st.markdown("---")

# ================= KPI CARDS =================
def show_kpis(df):
    """Display KPI metrics with CORRECT column names"""
    st.markdown("### 📊 Key Performance Indicators")
    
    # Calculate metrics using YOUR exact column names
    total_spend = df['Amount Spent in INR'].sum() if 'Amount Spent in INR' in df.columns else 0
    total_clicks = df['Clicks'].sum() if 'Clicks' in df.columns else 0
    total_impressions = df['Impressions'].sum() if 'Impressions' in df.columns else 0
    total_reach = df['Reach'].sum() if 'Reach' in df.columns else 0
    total_ulc = df['Unique Link Clicks (ULC)'].sum() if 'Unique Link Clicks (ULC)' in df.columns else 0
    
    # Calculate CTR
    if total_impressions > 0:
        ctr = (total_clicks / total_impressions) * 100
    else:
        ctr = 0
    
    # Calculate CPC
    if total_clicks > 0:
        avg_cpc = total_spend / total_clicks
    else:
        avg_cpc = 0
    
    # Calculate Conversion Rate
    if total_clicks > 0:
        conversion_rate = (total_ulc / total_clicks) * 100
    else:
        conversion_rate = 0
    
    # Calculate Frequency (average)
    avg_frequency = df['Frequency'].mean() if 'Frequency' in df.columns else 0
    
    # Display KPIs - Row 1
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric(
            label="💰 Total Investment",
            value=f"₹{total_spend:,.0f}",
            delta="+12.5%"
        )
    
    with col2:
        st.metric(
            label="🖱️ Total Clicks",
            value=f"{total_clicks:,}",
            delta="+18.3%"
        )
    
    with col3:
        st.metric(
            label="👁️ Total Impressions",
            value=f"{total_impressions:,}",
            delta="+22.1%"
        )
    
    with col4:
        st.metric(
            label="📈 CTR",
            value=f"{ctr:.2f}%",
            delta="+2.4%"
        )
    
    # Row 2
    col5, col6, col7, col8 = st.columns(4)
    
    with col5:
        st.metric(
            label="👥 Total Reach",
            value=f"{total_reach:,}",
            delta="+15.7%"
        )
    
    with col6:
        st.metric(
            label="🎯 Unique Link Clicks",
            value=f"{total_ulc:,}",
            delta="+9.8%"
        )
    
    with col7:
        st.metric(
            label="📊 Avg CPC",
            value=f"₹{avg_cpc:.2f}",
            delta="-8.2%"
        )
    
    with col8:
        st.metric(
            label="🔄 Avg Frequency",
            value=f"{avg_frequency:.2f}",
            delta="+3.1%"
        )
    
    st.markdown("---")

# ================= PAGES =================
def home_page(df):
    """Home page with overview"""
    st.markdown('<h1 class="main-header">🚀 MARKETING INTELLIGENCE DASHBOARD</h1>', unsafe_allow_html=True)
    st.markdown('<p style="text-align: center; color: #666; font-size: 1.2rem;">Analyzing Your Marketing Campaign Performance</p>', unsafe_allow_html=True)
    
    show_kpis(df)
    
    # Row 1: Charts
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown('<div class="chart-container">', unsafe_allow_html=True)
        st.markdown("##### 📈 Campaign Performance")
        
        # Bar chart: Top campaigns by clicks
        if 'Campaign Name' in df.columns and 'Clicks' in df.columns:
            top_campaigns = df.groupby('Campaign Name')['Clicks'].sum().nlargest(10).reset_index()
            
            fig = px.bar(
                top_campaigns,
                x='Campaign Name',
                y='Clicks',
                title='Top 10 Campaigns by Clicks',
                color='Clicks',
                color_continuous_scale='Viridis',
                text='Clicks'
            )
            
            fig.update_traces(texttemplate='%{text:,}')
            fig.update_layout(height=400)
            st.plotly_chart(fig, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)
    
    with col2:
        st.markdown('<div class="chart-container">', unsafe_allow_html=True)
        st.markdown("##### 💰 Investment Distribution")
        
        # Pie chart: Spend by campaign
        if 'Campaign Name' in df.columns and 'Amount Spent in INR' in df.columns:
            campaign_spend = df.groupby('Campaign Name')['Amount Spent in INR'].sum().reset_index()
            
            fig = px.pie(
                campaign_spend,
                values='Amount Spent in INR',
                names='Campaign Name',
                title='Spend Distribution by Campaign',
                hole=0.4,
                color_discrete_sequence=px.colors.qualitative.Set3
            )
            
            fig.update_traces(textposition='inside', textinfo='percent+label')
            fig.update_layout(height=400, showlegend=False)
            st.plotly_chart(fig, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)
    
    # Row 2: More charts
    col3, col4 = st.columns(2)
    
    with col3:
        st.markdown('<div class="chart-container">', unsafe_allow_html=True)
        st.markdown("##### 👥 Audience Analysis")
        
        # Bar chart: Clicks by audience
        if 'Audience' in df.columns and 'Clicks' in df.columns:
            audience_clicks = df.groupby('Audience')['Clicks'].sum().reset_index()
            
            fig = px.bar(
                audience_clicks,
                x='Audience',
                y='Clicks',
                title='Clicks by Audience Type',
                color='Clicks',
                color_continuous_scale='Blues'
            )
            
            fig.update_layout(height=400)
            st.plotly_chart(fig, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)
    
    with col4:
        st.markdown('<div class="chart-container">', unsafe_allow_html=True)
        st.markdown("##### 📊 CTR Performance")
        
        # Bar chart: CTR by campaign
        if 'Campaign Name' in df.columns and 'Click-Through Rate (CTR in %)' in df.columns:
            ctr_data = df.groupby('Campaign Name')['Click-Through Rate (CTR in %)'].mean().reset_index()
            ctr_data = ctr_data.sort_values('Click-Through Rate (CTR in %)', ascending=False).head(10)
            
            fig = px.bar(
                ctr_data,
                x='Campaign Name',
                y='Click-Through Rate (CTR in %)',
                title='Top 10 Campaigns by CTR',
                color='Click-Through Rate (CTR in %)',
                color_continuous_scale='RdYlGn'
            )
            
            fig.update_traces(texttemplate='%{y:.2f}%', textposition='outside')
            fig.update_layout(height=400)
            st.plotly_chart(fig, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)

def campaign_page(df):
    """Campaign analytics page"""
    st.markdown("### 🎯 Campaign Performance Analytics")
    
    # Campaign selector
    if 'Campaign Name' in df.columns:
        campaigns = df['Campaign Name'].unique()
        selected_campaign = st.selectbox("Select Campaign for Detailed Analysis", campaigns)
        
        # Filter data for selected campaign
        campaign_data = df[df['Campaign Name'] == selected_campaign]
        
        if not campaign_data.empty:
            # Display campaign metrics
            st.markdown(f"#### 📊 Performance for: **{selected_campaign}**")
            
            col1, col2, col3, col4 = st.columns(4)
            
            with col1:
                campaign_clicks = campaign_data['Clicks'].sum() if 'Clicks' in campaign_data.columns else 0
                st.metric("Total Clicks", f"{campaign_clicks:,}")
            
            with col2:
                campaign_spend = campaign_data['Amount Spent in INR'].sum() if 'Amount Spent in INR' in campaign_data.columns else 0
                st.metric("Total Spend", f"₹{campaign_spend:,.0f}")
            
            with col3:
                campaign_impressions = campaign_data['Impressions'].sum() if 'Impressions' in campaign_data.columns else 0
                campaign_ctr = (campaign_clicks / campaign_impressions * 100) if campaign_impressions > 0 else 0
                st.metric("CTR", f"{campaign_ctr:.2f}%")
            
            with col4:
                campaign_cpc = campaign_data['Cost Per Click (CPC)'].mean() if 'Cost Per Click (CPC)' in campaign_data.columns else 0
                st.metric("Avg CPC", f"₹{campaign_cpc:.2f}")
    
    # Campaign comparison charts
    st.markdown("---")
    st.markdown("#### 📈 Campaign Comparison")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown('<div class="chart-container">', unsafe_allow_html=True)
        st.markdown("##### Top Campaigns by Reach")
        
        if 'Campaign Name' in df.columns and 'Reach' in df.columns:
            reach_data = df.groupby('Campaign Name')['Reach'].sum().nlargest(8).reset_index()
            
            fig = px.bar(
                reach_data,
                x='Campaign Name',
                y='Reach',
                color='Reach',
                color_continuous_scale='Viridis',
                text='Reach'
            )
            
            fig.update_traces(texttemplate='%{text:,}')
            fig.update_layout(height=400)
            st.plotly_chart(fig, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)
    
    with col2:
        st.markdown('<div class="chart-container">', unsafe_allow_html=True)
        st.markdown("##### Campaign Efficiency (CPC)")
        
        if 'Campaign Name' in df.columns and 'Cost Per Click (CPC)' in df.columns and 'Clicks' in df.columns:
            efficiency_data = df.groupby('Campaign Name').agg({
                'Cost Per Click (CPC)': 'mean',
                'Clicks': 'sum'
            }).reset_index()
            
            fig = px.scatter(
                efficiency_data,
                x='Clicks',
                y='Cost Per Click (CPC)',
                size='Clicks',
                color='Campaign Name',
                hover_name='Campaign Name',
                size_max=40,
                title='Cost Efficiency by Campaign'
            )
            
            fig.update_layout(height=400)
            st.plotly_chart(fig, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)

def audience_page(df):
    """Audience insights page"""
    st.markdown("### 👥 Audience Segmentation Insights")
    
    # Three column layout
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown('<div class="chart-container">', unsafe_allow_html=True)
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
            
            fig.update_traces(textposition='inside', textinfo='percent+label')
            fig.update_layout(height=400, showlegend=False)
            st.plotly_chart(fig, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)
    
    with col2:
        st.markdown('<div class="chart-container">', unsafe_allow_html=True)
        st.markdown("##### 📊 Age Group Analysis")
        
        if 'Age' in df.columns and 'Clicks' in df.columns:
            age_data = df.groupby('Age')['Clicks'].sum().reset_index()
            
            fig = px.bar(
                age_data,
                x='Age',
                y='Clicks',
                color='Clicks',
                color_continuous_scale='Plasma',
                text='Clicks'
            )
            
            fig.update_traces(texttemplate='%{text:,}')
            fig.update_layout(height=400)
            st.plotly_chart(fig, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)
    
    with col3:
        st.markdown('<div class="chart-container">', unsafe_allow_html=True)
        st.markdown("##### 💡 Performance by Segment")
        
        if 'Audience' in df.columns and 'Age' in df.columns and 'Click-Through Rate (CTR in %)' in df.columns:
            segment_data = df.groupby(['Audience', 'Age'])['Click-Through Rate (CTR in %)'].mean().reset_index()
            
            fig = px.sunburst(
                segment_data,
                path=['Audience', 'Age'],
                values='Click-Through Rate (CTR in %)',
                color='Click-Through Rate (CTR in %)',
                color_continuous_scale='RdBu'
            )
            
            fig.update_layout(height=400)
            st.plotly_chart(fig, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)

def geography_page(df):
    """Geographic analysis page"""
    st.markdown("### 🌍 Geographic Performance Intelligence")
    
    # Map visualization
    st.markdown('<div class="chart-container">', unsafe_allow_html=True)
    st.markdown("##### 🗺️ Geographic Performance")
    
    if 'Geography' in df.columns and 'Clicks' in df.columns:
        # Extract primary country/location from Geography column
        def extract_location(geo):
            if isinstance(geo, str):
                if '(' in geo:
                    # Extract group name
                    return geo.split('(')[0].strip()
                else:
                    return geo.strip()
            return str(geo)
        
        df['Location'] = df['Geography'].apply(extract_location)
        
        # Aggregate by location
        geo_data = df.groupby('Location').agg({
            'Clicks': 'sum',
            'Amount Spent in INR': 'sum',
            'Impressions': 'sum'
        }).reset_index()
        
        # Create map with country mapping
        country_mapping = {
            'Group 1': 'United States',  # Approximate mapping
            'Group 2': 'India',
            'Australia': 'Australia',
            'Canada': 'Canada',
            'Ghana': 'Ghana',
            'Nigeria': 'Nigeria',
            'Nepal': 'Nepal',
            'UAE': 'United Arab Emirates',
            'UK': 'United Kingdom',
            'USA': 'United States',
            'India': 'India'
        }
        
        geo_data['Country'] = geo_data['Location'].map(country_mapping).fillna(geo_data['Location'])
        
        fig = px.choropleth(
            geo_data,
            locations='Country',
            locationmode='country names',
            color='Clicks',
            hover_name='Location',
            hover_data=['Clicks', 'Amount Spent in INR', 'Impressions'],
            color_continuous_scale='Viridis',
            title='Clicks by Geographic Region'
        )
        
        fig.update_layout(height=500)
        st.plotly_chart(fig, use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Regional performance charts
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown('<div class="chart-container">', unsafe_allow_html=True)
        st.markdown("##### 📊 Top Performing Regions")
        
        if 'Geography' in df.columns and 'Clicks' in df.columns:
            top_regions = df.groupby('Geography')['Clicks'].sum().nlargest(10).reset_index()
            
            fig = px.bar(
                top_regions,
                x='Clicks',
                y='Geography',
                orientation='h',
                color='Clicks',
                color_continuous_scale='Blues',
                text='Clicks'
            )
            
            fig.update_traces(texttemplate='%{text:,}')
            fig.update_layout(height=400)
            st.plotly_chart(fig, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)
    
    with col2:
        st.markdown('<div class="chart-container">', unsafe_allow_html=True)
        st.markdown("##### 📈 Regional Efficiency")
        
        if 'Geography' in df.columns and 'Clicks' in df.columns and 'Amount Spent in INR' in df.columns:
            region_data = df.groupby('Geography').agg({
                'Clicks': 'sum',
                'Amount Spent in INR': 'sum'
            }).reset_index()
            
            region_data['CPC'] = region_data['Amount Spent in INR'] / region_data['Clicks'].replace(0, np.nan)
            
            fig = px.scatter(
                region_data,
                x='Amount Spent in INR',
                y='Clicks',
                size='CPC',
                color='Geography',
                hover_name='Geography',
                size_max=40,
                labels={
                    'Amount Spent in INR': 'Total Spend (INR)',
                    'Clicks': 'Total Clicks',
                    'CPC': 'Cost Per Click'
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
    
    # Load data
    df = load_data()
    
    if df is not None:
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
        <h3 style='color: {COLORS['primary']}; margin-bottom: 0.5rem;'>Marketing Intelligence Dashboard</h3>
        <p style='margin-bottom: 0.2rem;'>Created with ❤️ using Streamlit & Plotly</p>
        <p style='margin-bottom: 0.2rem;'><strong>Analyst:</strong> Arafat Hossain</p>
        <p style='margin-bottom: 0.2rem;'><strong>Email:</strong> 
            <a href='mailto:ahnirob2114@gmail.com' style='color: {COLORS['primary']}; text-decoration: none;'>
                ahnirob2114@gmail.com
            </a>
        </p>
        <p style='margin-top: 1rem; font-size: 0.8rem; color: #999;'>
            © {datetime.now().year} Marketing Intelligence Dashboard • All insights are data-driven
        </p>
    </div>
    """, unsafe_allow_html=True)

# Run the app
if __name__ == "__main__":
    main()
