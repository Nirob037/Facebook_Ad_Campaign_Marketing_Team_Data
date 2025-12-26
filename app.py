import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
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
def load_data():
    st.markdown("### 📁 Upload Your Marketing Data CSV")
    uploaded_file = st.file_uploader(
        "Choose CSV file", type=["csv"]
    )
    
    if uploaded_file:
        df = pd.read_csv(uploaded_file)
    else:
        st.info("📝 Using demo data (your sample dataset)")
        demo_data = {
            'campaign ID': ['Campaign 1','Campaign 1','Campaign 1','Campaign 1','Campaign 2'],
            'Campaign Name': ['SHU_6 (Educators and Principals)']*4 + ['SHU3_ (Students Apart from India and US)'],
            'Audience': ['Educators and Principals']*4 + ['Students'],
            'Age': ['25-34','35-44','45-54','55-64','18-24'],
            'Geography': [
                'Group 1 (Australia, Canada, United Kingdom, Ghana, Nigeria, Pakistan, United States)',
                'Group 1 (Australia, Canada, United Kingdom, Ghana, Nigeria, Pakistan, United States)',
                'Group 1 (Australia, Canada, United Kingdom, Ghana, Nigeria, Pakistan, United States)',
                'Group 1 (Australia, Canada, United Kingdom, Ghana, Nigeria, Pakistan, United States)',
                'Group 2 (Australia, Canada, United Kingdom, Ghana, Niger, Nigeria, Nepal, Pakistan, Thailand, Taiwan)'
            ],
            'Reach':[11387,8761,2867,889,29675],
            'Impressions':[23283,15683,6283,1890,39161],
            'Frequency':[2.0447,1.7901,2.1915,2.126,1.3197],
            'Clicks':[487,484,198,49,2593],
            'Unique Clicks':[406,376,145,40,1994],
            'Unique Link Clicks (ULC)':[180,154,65,21,1095],
            'Click-Through Rate (CTR in %)':[2.09,3.09,3.15,2.59,6.62],
            'Unique Click-Through Rate (Unique CTR in %)':[0.77,0.98,1.03,1.11,2.8],
            'Amount Spent in INR':[1092.24,835.46,319.38,86.25,1193.94],
            'Cost Percentage':[9.03,6.91,2.64,0.71,9.88],
            'Cost Per Click (CPC)':[2.2428,1.7262,1.613,1.7602,0.4604],
            'Cost per Result (CPR)':[6.068,5.4251,4.9135,4.1071,1.0904]
        }
        df = pd.DataFrame(demo_data)
    
    # Make sure numeric columns are numeric
    numeric_cols = ['Reach','Impressions','Frequency','Clicks','Unique Clicks',
                    'Unique Link Clicks (ULC)','Click-Through Rate (CTR in %)',
                    'Unique Click-Through Rate (Unique CTR in %)','Amount Spent in INR',
                    'Cost Percentage','Cost Per Click (CPC)','Cost per Result (CPR)']
    for col in numeric_cols:
        if col in df.columns:
            df[col] = pd.to_numeric(df[col], errors='coerce')
    
    return df

# ================= KPI CARDS =================
def show_kpis(df):
    total_spend = df['Amount Spent in INR'].sum()
    total_clicks = df['Clicks'].sum()
    total_impressions = df['Impressions'].sum()
    total_reach = df['Reach'].sum()
    total_ulc = df['Unique Link Clicks (ULC)'].sum()
    
    ctr = (total_clicks / total_impressions) * 100 if total_impressions>0 else 0
    avg_cpc = total_spend / total_clicks if total_clicks>0 else 0
    conversion_rate = (total_ulc / total_clicks) * 100 if total_clicks>0 else 0
    avg_frequency = df['Frequency'].mean()
    
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("💰 Total Spend", f"₹{total_spend:,.0f}")
    col2.metric("🖱️ Total Clicks", f"{total_clicks:,}")
    col3.metric("👁️ Total Impressions", f"{total_impressions:,}")
    col4.metric("📈 CTR", f"{ctr:.2f}%")
    
    col5, col6, col7, col8 = st.columns(4)
    col5.metric("👥 Total Reach", f"{total_reach:,}")
    col6.metric("🎯 Unique Link Clicks", f"{total_ulc:,}")
    col7.metric("📊 Avg CPC", f"₹{avg_cpc:.2f}")
    col8.metric("🔄 Avg Frequency", f"{avg_frequency:.2f}")
    st.markdown("---")

# ================= PAGES =================
def home_page(df):
    st.markdown('<h1 class="main-header">🚀 Marketing Intelligence Dashboard</h1>', unsafe_allow_html=True)
    show_kpis(df)
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("##### 📈 Top Campaigns by Clicks")
        top_campaigns = df.groupby('Campaign Name')['Clicks'].sum().nlargest(10).reset_index()
        fig = px.bar(top_campaigns, x='Campaign Name', y='Clicks', text='Clicks', color='Clicks')
        fig.update_traces(texttemplate='%{text:,}', textposition='outside')
        fig.update_layout(height=400)
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        st.markdown("##### 💰 Spend by Campaign")
        spend_campaigns = df.groupby('Campaign Name')['Amount Spent in INR'].sum().reset_index()
        fig = px.pie(spend_campaigns, names='Campaign Name', values='Amount Spent in INR', hole=0.4)
        st.plotly_chart(fig, use_container_width=True)
    
    col3, col4 = st.columns(2)
    with col3:
        st.markdown("##### 👥 Clicks by Audience")
        audience_clicks = df.groupby('Audience')['Clicks'].sum().reset_index()
        fig = px.bar(audience_clicks, x='Audience', y='Clicks', color='Clicks', text='Clicks')
        fig.update_traces(texttemplate='%{text:,}', textposition='outside')
        st.plotly_chart(fig, use_container_width=True)
    
    with col4:
        st.markdown("##### 📊 CTR by Campaign")
        ctr_data = df.groupby('Campaign Name')['Click-Through Rate (CTR in %)'].mean().reset_index()
        ctr_data = ctr_data.sort_values('Click-Through Rate (CTR in %)', ascending=False).head(10)
        fig = px.bar(ctr_data, x='Campaign Name', y='Click-Through Rate (CTR in %)', color='Click-Through Rate (CTR in %)')
        fig.update_traces(texttemplate='%{y:.2f}%', textposition='outside')
        st.plotly_chart(fig, use_container_width=True)

def campaign_page(df):
    st.markdown("### 🎯 Campaign Performance Analytics")
    selected_campaign = st.selectbox("Select Campaign", df['Campaign Name'].unique())
    campaign_data = df[df['Campaign Name'] == selected_campaign]
    
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Total Clicks", f"{campaign_data['Clicks'].sum():,}")
    col2.metric("Total Spend", f"₹{campaign_data['Amount Spent in INR'].sum():,.0f}")
    impressions = campaign_data['Impressions'].sum()
    clicks = campaign_data['Clicks'].sum()
    ctr = clicks/impressions*100 if impressions>0 else 0
    col3.metric("CTR", f"{ctr:.2f}%")
    col4.metric("Avg CPC", f"₹{campaign_data['Cost Per Click (CPC)'].mean():.2f}")

def audience_page(df):
    st.markdown("### 👥 Audience Insights")
    audience_dist = df['Audience'].value_counts().reset_index()
    audience_dist.columns = ['Audience','Count']
    fig = px.pie(audience_dist, names='Audience', values='Count', hole=0.4)
    st.plotly_chart(fig, use_container_width=True)
    
    age_data = df.groupby('Age')['Clicks'].sum().reset_index()
    fig2 = px.bar(age_data, x='Age', y='Clicks', color='Clicks', text='Clicks')
    fig2.update_traces(texttemplate='%{text:,}', textposition='outside')
    st.plotly_chart(fig2, use_container_width=True)

def geography_page(df):
    st.markdown("### 🌍 Geographic Analysis")
    
    def extract_location(geo):
        if '(' in geo:
            return geo.split('(')[0].strip()
        return geo.strip()
    
    df['Location'] = df['Geography'].apply(extract_location)
    geo_data = df.groupby('Location').agg({'Clicks':'sum','Amount Spent in INR':'sum'}).reset_index()
    
    fig = px.choropleth(
        geo_data, locations='Location', locationmode='country names',
        color='Clicks', hover_name='Location', color_continuous_scale='Viridis'
    )
    st.plotly_chart(fig, use_container_width=True)

# ================= NAVIGATION =================
def navigation():
    st.sidebar.title("Navigation")
    page = st.sidebar.radio("Go to", ["Overview", "Campaign Analytics", "Audience Insights", "Geography"])
    return page

# ================= MAIN =================
df = load_data()
page = navigation()

if page == "Overview":
    home_page(df)
elif page == "Campaign Analytics":
    campaign_page(df)
elif page == "Audience Insights":
    audience_page(df)
elif page == "Geography":
    geography_page(df)

# ================= FOOTER =================
st.markdown("---")
st.markdown(f"""
<div class='footer'>
<p>Created with ❤️ using Streamlit & Plotly</p>
<p><strong>Analyst:</strong> Arafat Hossain</p>
<p><strong>Email:</strong> ahnirob2114@gmail.com</p>
<p>© {datetime.now().year} Marketing Intelligence Dashboard</p>
</div>
""", unsafe_allow_html=True)
