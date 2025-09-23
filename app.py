"""
EY Data Analytics Portfolio - Main Application
============================================

A comprehensive portfolio showcasing advanced data analytics capabilities 
tailored for Ernst & Young consulting roles.

Author: Data Analytics Portfolio for EY
"""

import streamlit as st
import webbrowser

# Page Configuration
st.set_page_config(
    page_title="EY Data Analytics Portfolio",
    page_icon="🎯",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
<style>
    .main-header {
        font-size: 3rem;
        color: #1f77b4;
        text-align: center;
        margin-bottom: 2rem;
        font-weight: bold;
    }
    .sub-header {
        font-size: 1.5rem;
        color: #666;
        text-align: center;
        margin-bottom: 3rem;
    }
    .dashboard-card {
        background-color: #f0f2f6;
        padding: 1.5rem;
        border-radius: 10px;
        margin: 1rem 0;
        border-left: 5px solid #1f77b4;
    }
    .tech-stack {
        background-color: #e8f4f8;
        padding: 0.5rem;
        border-radius: 5px;
        margin: 0.5rem 0;
    }
</style>
""", unsafe_allow_html=True)

# Header
st.markdown('<h1 class="main-header">🎯 EY Data Analytics Portfolio</h1>', unsafe_allow_html=True)
st.markdown('<p class="sub-header">Advanced Analytics Solutions for Business Intelligence & Risk Management</p>', unsafe_allow_html=True)

# Introduction
st.markdown("""
## 👋 Welcome to My Data Analytics Portfolio

This portfolio demonstrates comprehensive expertise in data analytics, machine learning, and business intelligence solutions specifically tailored for **Ernst & Young** consulting roles. Each dashboard showcases real-world business scenarios and advanced analytical capabilities.
""")

# Portfolio Overview
col1, col2 = st.columns([2, 1])

with col1:
    st.markdown("""
    ## 📊 Portfolio Highlights
    
    - **4 Interactive Dashboards** covering key business domains
    - **Advanced Analytics** with ML models and statistical insights
    - **Professional Visualizations** using Plotly and modern UI/UX
    - **Real-time Data Processing** and dynamic filtering
    - **Regulatory Compliance** focus for financial services
    - **Business Impact** metrics and actionable insights
    """)

with col2:
    st.markdown("""
    ## 🛠️ Technical Stack
    
    **Programming**: Python  
    **Frameworks**: Streamlit, Dash  
    **Analytics**: Pandas, NumPy, SciPy  
    **ML Libraries**: Scikit-learn, XGBoost  
    **Visualization**: Plotly, Matplotlib  
    **Data Sources**: APIs, CSV, Real-time feeds  
    """)

# Dashboard Cards
st.markdown("## 🚀 Interactive Dashboards")

# Dashboard 1: Financial Risk Analytics
st.markdown("""
<div class="dashboard-card">
    <h3>📊 Financial Risk Analytics Dashboard</h3>
    <p><strong>Business Domain:</strong> Financial Services & Risk Management</p>
    <p><strong>Key Features:</strong></p>
    <ul>
        <li>Credit Risk Assessment with ML models</li>
        <li>Market Risk Analysis (VaR, volatility)</li>
        <li>Regulatory Compliance Monitoring (Basel III, CCAR)</li>
        <li>Operational Risk Tracking</li>
        <li>Real-time Risk Alerts</li>
    </ul>
    <div class="tech-stack">
        <strong>Technologies:</strong> Streamlit, Plotly, yfinance, Pandas, NumPy
    </div>
</div>
""", unsafe_allow_html=True)

if st.button("🔗 Launch Financial Risk Dashboard", key="financial"):
    st.markdown("**Dashboard Link:** Run `streamlit run 01_Financial_Risk_Analytics/financial_risk_dashboard.py`")

# Dashboard 2: Supply Chain Optimization
st.markdown("""
<div class="dashboard-card">
    <h3>🚛 Supply Chain Optimization Analytics</h3>
    <p><strong>Business Domain:</strong> Operations & Supply Chain Management</p>
    <p><strong>Key Features:</strong></p>
    <ul>
        <li>Demand Forecasting with ML algorithms</li>
        <li>Inventory Optimization models</li>
        <li>Route Planning & Logistics optimization</li>
        <li>Supplier Performance Analytics</li>
        <li>Cost Reduction Analysis</li>
    </ul>
    <div class="tech-stack">
        <strong>Technologies:</strong> Dash, Plotly, Scikit-learn, Optimization algorithms
    </div>
</div>
""", unsafe_allow_html=True)

if st.button("🔗 Launch Supply Chain Dashboard", key="supply"):
    st.markdown("**Dashboard Link:** Run `python 02_Supply_Chain_Optimization/supply_chain_dashboard.py`")

# Dashboard 3: Customer Analytics
st.markdown("""
<div class="dashboard-card">
    <h3>👥 Customer Analytics & Segmentation</h3>
    <p><strong>Business Domain:</strong> Marketing & Customer Intelligence</p>
    <p><strong>Key Features:</strong></p>
    <ul>
        <li>Customer Segmentation using ML clustering</li>
        <li>Churn Prediction models</li>
        <li>Customer Lifetime Value (CLV) analysis</li>
        <li>Campaign Performance optimization</li>
        <li>Behavioral Analytics</li>
    </ul>
    <div class="tech-stack">
        <strong>Technologies:</strong> Streamlit, Scikit-learn, Clustering algorithms, Plotly
    </div>
</div>
""", unsafe_allow_html=True)

if st.button("🔗 Launch Customer Analytics Dashboard", key="customer"):
    st.markdown("**Dashboard Link:** Run `streamlit run 03_Customer_Analytics/customer_analytics_dashboard.py`")

# Dashboard 4: ESG Analytics
st.markdown("""
<div class="dashboard-card">
    <h3>🌱 ESG Analytics Dashboard</h3>
    <p><strong>Business Domain:</strong> Sustainability & ESG Reporting</p>
    <p><strong>Key Features:</strong></p>
    <ul>
        <li>Environmental impact metrics</li>
        <li>Social responsibility tracking</li>
        <li>Governance compliance monitoring</li>
        <li>Sustainability KPIs dashboard</li>
        <li>ESG scoring and benchmarking</li>
    </ul>
    <div class="tech-stack">
        <strong>Technologies:</strong> Streamlit, Plotly, Pandas, Environmental data APIs
    </div>
</div>
""", unsafe_allow_html=True)

if st.button("🔗 Launch ESG Analytics Dashboard", key="esg"):
    st.markdown("**Dashboard Link:** Run `streamlit run 04_ESG_Analytics/esg_dashboard.py`")

# Business Impact Section
st.markdown("## 💼 Business Impact & Value Proposition")

col1, col2, col3 = st.columns(3)

with col1:
    st.metric(
        label="Risk Reduction",
        value="25-40%",
        delta="Through predictive analytics"
    )

with col2:
    st.metric(
        label="Cost Optimization",
        value="15-25%",
        delta="Supply chain efficiency"
    )

with col3:
    st.metric(
        label="Customer Retention",
        value="20-35%",
        delta="Advanced segmentation"
    )

# Technical Capabilities
st.markdown("## 🔧 Technical Capabilities Demonstrated")

capabilities = {
    "Machine Learning": ["Supervised Learning", "Unsupervised Learning", "Ensemble Methods", "Time Series Forecasting"],
    "Data Engineering": ["Data Pipeline Design", "ETL Processes", "Real-time Processing", "API Integration"],
    "Visualization": ["Interactive Dashboards", "Real-time Charts", "KPI Monitoring", "Executive Reporting"],
    "Business Intelligence": ["Risk Analytics", "Performance Metrics", "Trend Analysis", "Predictive Insights"]
}

col1, col2 = st.columns(2)
for i, (category, skills) in enumerate(capabilities.items()):
    with col1 if i % 2 == 0 else col2:
        st.markdown(f"**{category}**")
        for skill in skills:
            st.markdown(f"• {skill}")

# Contact & Deployment
st.markdown("---")
st.markdown("## 🚀 Deployment & Usage")

st.markdown("""
### Local Development
```bash
# Clone the repository
git clone https://github.com/YOUR_USERNAME/EY_DataAnalytics_Portfolio.git

# Install dependencies
pip install -r requirements.txt

# Run individual dashboards
streamlit run 01_Financial_Risk_Analytics/financial_risk_dashboard.py
```

### Live Deployment
This portfolio is deployed on **Streamlit Community Cloud** for easy access and demonstration.
""")

# Footer
st.markdown("---")
st.markdown("""
<div style='text-align: center; color: #666;'>
    <p>🏢 <strong>EY Data Analytics Portfolio</strong> | Demonstrating Advanced Analytics Capabilities</p>
    <p>Built with ❤️ using Python, Streamlit, and modern data science tools</p>
</div>
""", unsafe_allow_html=True)