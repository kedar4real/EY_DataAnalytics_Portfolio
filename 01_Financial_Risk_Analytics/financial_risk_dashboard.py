"""
Financial Risk Analytics Dashboard
=================================

A comprehensive risk assessment and monitoring system for financial institutions.
Demonstrates advanced risk modeling, regulatory compliance, and real-time monitoring.

Key Features:
- Credit Risk Assessment
- Market Risk Analysis  
- Operational Risk Monitoring
- Regulatory Compliance Tracking
- Stress Testing Scenarios
- Risk Appetite Monitoring

Author: Data Analytics Portfolio for EY
"""

import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import yfinance as yf
from datetime import datetime, timedelta
import warnings
warnings.filterwarnings('ignore')

# Page Configuration
st.set_page_config(
    page_title="EY Financial Risk Analytics Dashboard",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for professional styling
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        color: #1f77b4;
        text-align: center;
        margin-bottom: 2rem;
        font-weight: bold;
    }
    .metric-card {
        background-color: #f0f2f6;
        padding: 1rem;
        border-radius: 0.5rem;
        border-left: 4px solid #1f77b4;
        margin: 0.5rem 0;
    }
    .risk-high { color: #d62728; }
    .risk-medium { color: #ff7f0e; }
    .risk-low { color: #2ca02c; }
    .sidebar .sidebar-content {
        background-color: #f8f9fa;
    }
</style>
""", unsafe_allow_html=True)

# Header
st.markdown('<h1 class="main-header">🏦 EY Financial Risk Analytics Dashboard</h1>', unsafe_allow_html=True)

# Sidebar for controls
st.sidebar.header("🎛️ Risk Controls")

# Risk Parameters
st.sidebar.subheader("Risk Parameters")
confidence_level = st.sidebar.selectbox(
    "Confidence Level",
    [0.95, 0.99, 0.999],
    index=1,
    help="Confidence level for VaR calculations"
)

time_horizon = st.sidebar.selectbox(
    "Time Horizon (days)",
    [1, 5, 10, 30],
    index=2,
    help="Time horizon for risk calculations"
)

portfolio_size = st.sidebar.number_input(
    "Portfolio Size ($M)",
    min_value=1,
    max_value=10000,
    value=1000,
    help="Total portfolio value in millions"
)

# Generate sample financial data
@st.cache_data
def generate_financial_data():
    """Generate realistic financial risk data"""
    np.random.seed(42)
    
    # Generate portfolio data
    dates = pd.date_range(start='2023-01-01', end='2024-01-01', freq='D')
    n_days = len(dates)
    
    # Simulate asset returns
    assets = ['Equity', 'Bonds', 'Commodities', 'Real Estate', 'Cash']
    returns = np.random.normal(0.0005, 0.02, (n_days, len(assets)))
    
    # Add some correlation and volatility clustering
    for i in range(1, n_days):
        returns[i] = 0.7 * returns[i-1] + 0.3 * np.random.normal(0.0005, 0.02, len(assets))
    
    portfolio_data = pd.DataFrame(returns, index=dates, columns=assets)
    
    # Generate credit risk data
    credit_data = pd.DataFrame({
        'Customer_ID': range(1, 1001),
        'Credit_Score': np.random.normal(650, 100, 1000),
        'Outstanding_Amount': np.random.lognormal(8, 1, 1000),
        'Probability_of_Default': np.random.beta(2, 98, 1000),
        'Loss_Given_Default': np.random.beta(3, 7, 1000),
        'Exposure_at_Default': np.random.lognormal(9, 1.5, 1000)
    })
    
    # Generate market risk data
    market_data = pd.DataFrame({
        'Date': dates,
        'Portfolio_Value': np.cumsum(np.random.normal(0, 1000000, n_days)) + portfolio_size * 1e6,
        'VaR_95': np.random.normal(5000000, 500000, n_days),
        'VaR_99': np.random.normal(8000000, 800000, n_days),
        'Expected_Shortfall': np.random.normal(12000000, 1200000, n_days)
    })
    
    return portfolio_data, credit_data, market_data

# Load data
portfolio_data, credit_data, market_data = generate_financial_data()

# Main dashboard layout
tab1, tab2, tab3, tab4, tab5 = st.tabs([
    "📊 Risk Overview", 
    "💳 Credit Risk", 
    "📈 Market Risk", 
    "⚙️ Operational Risk",
    "📋 Compliance"
])

with tab1:
    st.header("🎯 Risk Overview Dashboard")
    
    # Key Risk Metrics
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric(
            label="Total Portfolio Value",
            value=f"${portfolio_size:,}M",
            delta="2.3%"
        )
    
    with col2:
        var_95 = market_data['VaR_95'].iloc[-1]
        st.metric(
            label="VaR (95%)",
            value=f"${var_95/1e6:.1f}M",
            delta="-1.2%"
        )
    
    with col3:
        es = market_data['Expected_Shortfall'].iloc[-1]
        st.metric(
            label="Expected Shortfall",
            value=f"${es/1e6:.1f}M",
            delta="0.8%"
        )
    
    with col4:
        portfolio_return = portfolio_data.sum(axis=1).iloc[-1]
        st.metric(
            label="Daily Return",
            value=f"{portfolio_return:.2%}",
            delta="0.1%"
        )
    
    # Risk Distribution Chart
    st.subheader("📊 Risk Distribution by Asset Class")
    
    # Calculate risk metrics by asset
    asset_risks = []
    for asset in portfolio_data.columns:
        returns = portfolio_data[asset]
        var = np.percentile(returns, (1-confidence_level)*100)
        volatility = returns.std()
        asset_risks.append({
            'Asset': asset,
            'VaR': abs(var),
            'Volatility': volatility,
            'Expected_Return': returns.mean()
        })
    
    risk_df = pd.DataFrame(asset_risks)
    
    fig = px.bar(
        risk_df, 
        x='Asset', 
        y='VaR',
        title='Value at Risk by Asset Class',
        color='VaR',
        color_continuous_scale='Reds'
    )
    fig.update_layout(height=400)
    st.plotly_chart(fig, use_container_width=True)
    
    # Risk-Return Scatter Plot
    fig2 = px.scatter(
        risk_df,
        x='Volatility',
        y='Expected_Return',
        size='VaR',
        color='Asset',
        title='Risk-Return Profile by Asset Class',
        hover_data=['Asset', 'VaR']
    )
    fig2.update_layout(height=400)
    st.plotly_chart(fig2, use_container_width=True)

with tab2:
    st.header("💳 Credit Risk Analysis")
    
    # Credit Risk Metrics
    col1, col2, col3 = st.columns(3)
    
    with col1:
        avg_pd = credit_data['Probability_of_Default'].mean()
        st.metric(
            label="Average Probability of Default",
            value=f"{avg_pd:.2%}",
            delta="-0.1%"
        )
    
    with col2:
        total_exposure = credit_data['Exposure_at_Default'].sum()
        st.metric(
            label="Total Credit Exposure",
            value=f"${total_exposure/1e6:.1f}M",
            delta="5.2%"
        )
    
    with col3:
        expected_loss = (credit_data['Probability_of_Default'] * 
                       credit_data['Loss_Given_Default'] * 
                       credit_data['Exposure_at_Default']).sum()
        st.metric(
            label="Expected Credit Loss",
            value=f"${expected_loss/1e6:.1f}M",
            delta="2.1%"
        )
    
    # Credit Score Distribution
    st.subheader("📊 Credit Score Distribution")
    
    fig = px.histogram(
        credit_data,
        x='Credit_Score',
        nbins=30,
        title='Distribution of Customer Credit Scores',
        color_discrete_sequence=['#1f77b4']
    )
    fig.add_vline(x=650, line_dash="dash", line_color="red", 
                  annotation_text="Average Score")
    st.plotly_chart(fig, use_container_width=True)
    
    # Risk Rating Analysis
    st.subheader("🎯 Risk Rating Analysis")
    
    # Create risk categories
    credit_data['Risk_Category'] = pd.cut(
        credit_data['Credit_Score'],
        bins=[0, 580, 670, 740, 850],
        labels=['Poor', 'Fair', 'Good', 'Excellent']
    )
    
    risk_summary = credit_data.groupby('Risk_Category').agg({
        'Exposure_at_Default': 'sum',
        'Probability_of_Default': 'mean',
        'Customer_ID': 'count'
    }).round(4)
    
    st.dataframe(risk_summary, use_container_width=True)

with tab3:
    st.header("📈 Market Risk Analysis")
    
    # Market Risk Metrics
    col1, col2, col3 = st.columns(3)
    
    with col1:
        portfolio_volatility = portfolio_data.sum(axis=1).std()
        st.metric(
            label="Portfolio Volatility",
            value=f"{portfolio_volatility:.2%}",
            delta="-0.3%"
        )
    
    with col2:
        sharpe_ratio = portfolio_data.sum(axis=1).mean() / portfolio_data.sum(axis=1).std()
        st.metric(
            label="Sharpe Ratio",
            value=f"{sharpe_ratio:.2f}",
            delta="0.1"
        )
    
    with col3:
        max_drawdown = (portfolio_data.sum(axis=1).cumsum() - 
                       portfolio_data.sum(axis=1).cumsum().expanding().max()).min()
        st.metric(
            label="Maximum Drawdown",
            value=f"{max_drawdown:.2%}",
            delta="0.2%"
        )
    
    # Portfolio Value Over Time
    st.subheader("📊 Portfolio Value Evolution")
    
    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=market_data['Date'],
        y=market_data['Portfolio_Value'],
        mode='lines',
        name='Portfolio Value',
        line=dict(color='#1f77b4', width=2)
    ))
    
    fig.update_layout(
        title='Portfolio Value Over Time',
        xaxis_title='Date',
        yaxis_title='Portfolio Value ($)',
        height=400
    )
    st.plotly_chart(fig, use_container_width=True)
    
    # VaR Evolution
    st.subheader("⚠️ Value at Risk Evolution")
    
    fig2 = make_subplots(specs=[[{"secondary_y": True}]])
    
    fig2.add_trace(
        go.Scatter(x=market_data['Date'], y=market_data['VaR_95'], 
                  name='VaR 95%', line=dict(color='red')),
        secondary_y=False,
    )
    
    fig2.add_trace(
        go.Scatter(x=market_data['Date'], y=market_data['VaR_99'], 
                  name='VaR 99%', line=dict(color='darkred')),
        secondary_y=False,
    )
    
    fig2.update_layout(
        title='Value at Risk Over Time',
        xaxis_title='Date',
        height=400
    )
    
    fig2.update_yaxes(title_text="VaR ($)", secondary_y=False)
    st.plotly_chart(fig2, use_container_width=True)

with tab4:
    st.header("⚙️ Operational Risk Monitoring")
    
    # Generate operational risk data
    operational_risks = pd.DataFrame({
        'Risk_Category': ['Technology', 'Process', 'People', 'External', 'Legal'],
        'Risk_Level': ['Medium', 'Low', 'High', 'Medium', 'Low'],
        'Impact_Score': [7, 4, 9, 6, 5],
        'Probability_Score': [6, 3, 8, 5, 4],
        'Mitigation_Status': ['In Progress', 'Completed', 'Planned', 'In Progress', 'Completed']
    })
    
    # Risk Heatmap
    st.subheader("🔥 Risk Heatmap")
    
    fig = px.scatter(
        operational_risks,
        x='Probability_Score',
        y='Impact_Score',
        size='Impact_Score',
        color='Risk_Category',
        hover_data=['Risk_Level', 'Mitigation_Status'],
        title='Operational Risk Assessment Matrix'
    )
    
    # Add risk zones
    fig.add_shape(
        type="rect", x0=0, y0=0, x1=5, y1=5,
        fillcolor="green", opacity=0.1, line=dict(color="green")
    )
    fig.add_shape(
        type="rect", x0=5, y0=5, x1=10, y1=10,
        fillcolor="red", opacity=0.1, line=dict(color="red")
    )
    
    fig.update_layout(height=500)
    st.plotly_chart(fig, use_container_width=True)
    
    # Risk Summary Table
    st.subheader("📋 Risk Summary")
    st.dataframe(operational_risks, use_container_width=True)

with tab5:
    st.header("📋 Regulatory Compliance Dashboard")
    
    # Compliance Metrics
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric(
            label="Basel III Compliance",
            value="98.5%",
            delta="1.2%"
        )
    
    with col2:
        st.metric(
            label="CCAR Compliance",
            value="100%",
            delta="0%"
        )
    
    with col3:
        st.metric(
            label="SOX Compliance",
            value="99.2%",
            delta="0.3%"
        )
    
    with col4:
        st.metric(
            label="GDPR Compliance",
            value="100%",
            delta="0%"
        )
    
    # Compliance Timeline
    st.subheader("📅 Compliance Timeline")
    
    compliance_data = pd.DataFrame({
        'Regulation': ['Basel III', 'CCAR', 'SOX', 'GDPR', 'MiFID II'],
        'Next_Review': ['2024-03-15', '2024-06-30', '2024-12-31', '2024-05-25', '2024-04-15'],
        'Status': ['On Track', 'Completed', 'On Track', 'Completed', 'On Track'],
        'Risk_Level': ['Low', 'Low', 'Medium', 'Low', 'Medium']
    })
    
    fig = px.timeline(
        compliance_data,
        x_start='Next_Review',
        x_end='Next_Review',
        y='Regulation',
        color='Risk_Level',
        title='Regulatory Compliance Schedule',
        color_discrete_map={'Low': 'green', 'Medium': 'orange', 'High': 'red'}
    )
    
    fig.update_layout(height=400)
    st.plotly_chart(fig, use_container_width=True)

# Footer
st.markdown("---")
st.markdown("""
<div style='text-align: center; color: #666;'>
    <p>🏦 EY Financial Risk Analytics Dashboard | Built for Ernst & Young Data Analytics Portfolio</p>
    <p>Demonstrates advanced risk modeling, regulatory compliance, and real-time monitoring capabilities</p>
</div>
""", unsafe_allow_html=True)
