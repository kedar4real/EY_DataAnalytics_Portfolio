"""
ESG Analytics Dashboard
======================

Comprehensive ESG analytics featuring carbon footprint analysis, social impact measurement,
governance compliance tracking, and sustainability reporting for responsible business practices.

Key Features:
- Carbon Footprint Analysis
- Social Impact Measurement
- Governance Compliance Tracking
- Sustainability Reporting
- ESG Score Calculation
- Benchmarking & Trends

Author: Data Analytics Portfolio for EY
"""

import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from datetime import datetime, timedelta
import warnings
warnings.filterwarnings('ignore')

# Page Configuration
st.set_page_config(
    page_title="EY ESG Analytics Dashboard",
    page_icon="🌱",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
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
    .esg-excellent { color: #2ca02c; }
    .esg-good { color: #ff7f0e; }
    .esg-poor { color: #d62728; }
    .carbon-reduction { color: #2ca02c; }
    .carbon-increase { color: #d62728; }
</style>
""", unsafe_allow_html=True)

# Header
st.markdown('<h1 class="main-header">🌱 EY ESG Analytics Dashboard</h1>', unsafe_allow_html=True)

# Generate sample ESG data
@st.cache_data
def generate_esg_data():
    """Generate realistic ESG analytics data"""
    np.random.seed(42)
    
    # Generate environmental data
    dates = pd.date_range(start='2023-01-01', end='2024-01-01', freq='M')
    environmental_data = pd.DataFrame({
        'Date': dates,
        'Carbon_Emissions_Tonnes': np.random.normal(5000, 500, len(dates)),
        'Energy_Consumption_MWh': np.random.normal(15000, 2000, len(dates)),
        'Water_Usage_Litres': np.random.normal(100000, 15000, len(dates)),
        'Waste_Generated_Tonnes': np.random.normal(200, 30, len(dates)),
        'Renewable_Energy_Percentage': np.random.normal(35, 5, len(dates)),
        'Recycling_Rate': np.random.normal(75, 8, len(dates))
    })
    
    # Generate social data
    social_data = pd.DataFrame({
        'Metric': ['Employee_Satisfaction', 'Diversity_Index', 'Safety_Incidents', 
                 'Training_Hours', 'Community_Investment', 'Supplier_Diversity'],
        'Current_Value': [4.2, 0.78, 12, 45, 2500000, 0.65],
        'Target_Value': [4.5, 0.85, 8, 50, 3000000, 0.75],
        'Unit': ['Score (1-5)', 'Index (0-1)', 'Count', 'Hours/Employee', 'USD', 'Percentage']
    })
    
    # Generate governance data
    governance_data = pd.DataFrame({
        'Category': ['Board_Diversity', 'Executive_Compensation', 'Audit_Independence', 
                    'Risk_Management', 'Transparency_Score', 'Compliance_Rate'],
        'Score': [85, 78, 92, 88, 90, 95],
        'Industry_Average': [72, 75, 85, 82, 78, 88],
        'Best_Practice': [90, 85, 95, 90, 95, 98]
    })
    
    # Generate ESG scores by category
    esg_scores = pd.DataFrame({
        'Category': ['Environmental', 'Social', 'Governance', 'Overall'],
        'Current_Score': [78, 82, 88, 83],
        'Previous_Score': [75, 80, 85, 80],
        'Industry_Average': [72, 75, 82, 76],
        'Target_Score': [85, 88, 92, 88]
    })
    
    return environmental_data, social_data, governance_data, esg_scores

# Load data
env_data, social_data, gov_data, esg_scores = generate_esg_data()

# Sidebar controls
st.sidebar.header("🎛️ ESG Controls")

# Time period selection
st.sidebar.subheader("Time Period")
time_period = st.sidebar.selectbox(
    "Select Analysis Period",
    ["Last 6 Months", "Last Year", "Last 2 Years", "All Time"],
    index=1
)

# ESG focus area
st.sidebar.subheader("Focus Area")
focus_area = st.sidebar.selectbox(
    "Primary Focus",
    ["Environmental", "Social", "Governance", "Overall ESG"],
    index=0
)

# Benchmark comparison
st.sidebar.subheader("Benchmarking")
show_benchmarks = st.sidebar.checkbox("Show Industry Benchmarks", value=True)
show_targets = st.sidebar.checkbox("Show Target Goals", value=True)

# Main dashboard
tab1, tab2, tab3, tab4, tab5 = st.tabs([
    "🌍 Environmental", 
    "👥 Social", 
    "🏛️ Governance", 
    "📊 ESG Overview",
    "📈 Trends & Insights"
])

with tab1:
    st.header("🌍 Environmental Impact Analysis")
    
    # Environmental metrics
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        current_emissions = env_data['Carbon_Emissions_Tonnes'].iloc[-1]
        prev_emissions = env_data['Carbon_Emissions_Tonnes'].iloc[-2]
        change = (current_emissions - prev_emissions) / prev_emissions
        st.metric(
            label="Carbon Emissions",
            value=f"{current_emissions:,.0f} tonnes",
            delta=f"{change:.1%}",
            delta_color="inverse"
        )
    
    with col2:
        renewable_pct = env_data['Renewable_Energy_Percentage'].iloc[-1]
        st.metric(
            label="Renewable Energy",
            value=f"{renewable_pct:.1f}%",
            delta="2.3%"
        )
    
    with col3:
        recycling_rate = env_data['Recycling_Rate'].iloc[-1]
        st.metric(
            label="Recycling Rate",
            value=f"{recycling_rate:.1f}%",
            delta="1.8%"
        )
    
    with col4:
        energy_consumption = env_data['Energy_Consumption_MWh'].iloc[-1]
        st.metric(
            label="Energy Consumption",
            value=f"{energy_consumption:,.0f} MWh",
            delta="-3.2%"
        )
    
    # Environmental charts
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("📊 Carbon Emissions Trend")
        fig = go.Figure()
        fig.add_trace(go.Scatter(
            x=env_data['Date'],
            y=env_data['Carbon_Emissions_Tonnes'],
            mode='lines+markers',
            name='Carbon Emissions',
            line=dict(color='#d62728', width=3)
        ))
        
        if show_targets:
            target_emissions = env_data['Carbon_Emissions_Tonnes'].mean() * 0.8
            fig.add_hline(y=target_emissions, line_dash="dash", line_color="green",
                         annotation_text="2024 Target")
        
        fig.update_layout(
            title='Carbon Emissions Over Time',
            xaxis_title='Date',
            yaxis_title='Emissions (Tonnes)',
            height=400
        )
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        st.subheader("⚡ Energy Mix Analysis")
        current_month = env_data.iloc[-1]
        renewable = current_month['Renewable_Energy_Percentage']
        non_renewable = 100 - renewable
        
        fig = px.pie(
            values=[renewable, non_renewable],
            names=['Renewable', 'Non-Renewable'],
            title='Current Energy Mix',
            color_discrete_map={'Renewable': '#2ca02c', 'Non-Renewable': '#d62728'}
        )
        st.plotly_chart(fig, use_container_width=True)
    
    # Environmental KPIs
    st.subheader("🎯 Environmental KPIs")
    
    kpi_data = pd.DataFrame({
        'KPI': ['Carbon Intensity', 'Energy Efficiency', 'Water Efficiency', 'Waste Reduction'],
        'Current': [env_data['Carbon_Emissions_Tonnes'].iloc[-1] / 1000,
                   env_data['Energy_Consumption_MWh'].iloc[-1] / 1000,
                   env_data['Water_Usage_Litres'].iloc[-1] / 1000,
                   env_data['Waste_Generated_Tonnes'].iloc[-1]],
        'Target': [4000, 12000, 80000, 150],
        'Unit': ['Tonnes/M$ Revenue', 'MWh/M$ Revenue', 'Litres/M$ Revenue', 'Tonnes/Month']
    })
    
    fig = px.bar(
        kpi_data,
        x='KPI',
        y=['Current', 'Target'],
        title='Environmental KPIs vs Targets',
        barmode='group',
        color_discrete_sequence=['#1f77b4', '#2ca02c']
    )
    st.plotly_chart(fig, use_container_width=True)

with tab2:
    st.header("👥 Social Impact Analysis")
    
    # Social metrics
    col1, col2, col3 = st.columns(3)
    
    with col1:
        employee_satisfaction = social_data[social_data['Metric'] == 'Employee_Satisfaction']['Current_Value'].iloc[0]
        st.metric(
            label="Employee Satisfaction",
            value=f"{employee_satisfaction:.1f}/5.0",
            delta="0.2"
        )
    
    with col2:
        diversity_index = social_data[social_data['Metric'] == 'Diversity_Index']['Current_Value'].iloc[0]
        st.metric(
            label="Diversity Index",
            value=f"{diversity_index:.2f}",
            delta="0.03"
        )
    
    with col3:
        safety_incidents = social_data[social_data['Metric'] == 'Safety_Incidents']['Current_Value'].iloc[0]
        st.metric(
            label="Safety Incidents",
            value=f"{safety_incidents}",
            delta="-2",
            delta_color="inverse"
        )
    
    # Social performance chart
    st.subheader("📊 Social Performance vs Targets")
    
    fig = go.Figure()
    
    metrics = social_data['Metric'].tolist()
    current_values = social_data['Current_Value'].tolist()
    target_values = social_data['Target_Value'].tolist()
    
    fig.add_trace(go.Bar(
        name='Current',
        x=metrics,
        y=current_values,
        marker_color='#1f77b4'
    ))
    
    if show_targets:
        fig.add_trace(go.Bar(
            name='Target',
            x=metrics,
            y=target_values,
            marker_color='#2ca02c',
            opacity=0.7
        ))
    
    fig.update_layout(
        title='Social Performance Metrics',
        xaxis_title='Metrics',
        yaxis_title='Values',
        barmode='group',
        height=500
    )
    st.plotly_chart(fig, use_container_width=True)
    
    # Social impact areas
    st.subheader("🎯 Social Impact Areas")
    
    impact_areas = pd.DataFrame({
        'Area': ['Workplace Safety', 'Employee Development', 'Community Investment', 
                'Supplier Relations', 'Customer Satisfaction', 'Innovation'],
        'Score': [88, 82, 75, 79, 85, 90],
        'Impact': ['High', 'Medium', 'High', 'Medium', 'High', 'High']
    })
    
    fig = px.scatter(
        impact_areas,
        x='Score',
        y='Area',
        size='Score',
        color='Impact',
        title='Social Impact Areas Assessment',
        color_discrete_map={'High': '#2ca02c', 'Medium': '#ff7f0e', 'Low': '#d62728'}
    )
    st.plotly_chart(fig, use_container_width=True)

with tab3:
    st.header("🏛️ Governance Analysis")
    
    # Governance metrics
    col1, col2, col3 = st.columns(3)
    
    with col1:
        board_diversity = gov_data[gov_data['Category'] == 'Board_Diversity']['Score'].iloc[0]
        st.metric(
            label="Board Diversity",
            value=f"{board_diversity}%",
            delta="3%"
        )
    
    with col2:
        compliance_rate = gov_data[gov_data['Category'] == 'Compliance_Rate']['Score'].iloc[0]
        st.metric(
            label="Compliance Rate",
            value=f"{compliance_rate}%",
            delta="2%"
        )
    
    with col3:
        transparency_score = gov_data[gov_data['Category'] == 'Transparency_Score']['Score'].iloc[0]
        st.metric(
            label="Transparency Score",
            value=f"{transparency_score}%",
            delta="5%"
        )
    
    # Governance performance comparison
    st.subheader("📊 Governance Performance vs Benchmarks")
    
    fig = go.Figure()
    
    categories = gov_data['Category'].tolist()
    scores = gov_data['Score'].tolist()
    industry_avg = gov_data['Industry_Average'].tolist()
    best_practice = gov_data['Best_Practice'].tolist()
    
    fig.add_trace(go.Bar(
        name='Our Score',
        x=categories,
        y=scores,
        marker_color='#1f77b4'
    ))
    
    if show_benchmarks:
        fig.add_trace(go.Bar(
            name='Industry Average',
            x=categories,
            y=industry_avg,
            marker_color='#ff7f0e',
            opacity=0.7
        ))
        
        fig.add_trace(go.Bar(
            name='Best Practice',
            x=categories,
            y=best_practice,
            marker_color='#2ca02c',
            opacity=0.5
        ))
    
    fig.update_layout(
        title='Governance Performance Comparison',
        xaxis_title='Categories',
        yaxis_title='Score (%)',
        barmode='group',
        height=500
    )
    st.plotly_chart(fig, use_container_width=True)
    
    # Governance framework
    st.subheader("🏗️ Governance Framework")
    
    framework_data = pd.DataFrame({
        'Component': ['Board Structure', 'Risk Management', 'Audit & Controls', 
                     'Executive Compensation', 'Stakeholder Engagement', 'Ethics & Compliance'],
        'Maturity_Level': ['Advanced', 'Advanced', 'Mature', 'Developing', 'Advanced', 'Mature'],
        'Score': [92, 88, 95, 78, 85, 90]
    })
    
    fig = px.treemap(
        framework_data,
        path=['Component'],
        values='Score',
        color='Score',
        title='Governance Framework Maturity',
        color_continuous_scale='Greens'
    )
    st.plotly_chart(fig, use_container_width=True)

with tab4:
    st.header("📊 ESG Overview Dashboard")
    
    # Overall ESG score
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        overall_score = esg_scores[esg_scores['Category'] == 'Overall']['Current_Score'].iloc[0]
        st.metric(
            label="Overall ESG Score",
            value=f"{overall_score}/100",
            delta="3 points"
        )
    
    with col2:
        env_score = esg_scores[esg_scores['Category'] == 'Environmental']['Current_Score'].iloc[0]
        st.metric(
            label="Environmental Score",
            value=f"{env_score}/100",
            delta="3 points"
        )
    
    with col3:
        social_score = esg_scores[esg_scores['Category'] == 'Social']['Current_Score'].iloc[0]
        st.metric(
            label="Social Score",
            value=f"{social_score}/100",
            delta="2 points"
        )
    
    with col4:
        gov_score = esg_scores[esg_scores['Category'] == 'Governance']['Current_Score'].iloc[0]
        st.metric(
            label="Governance Score",
            value=f"{gov_score}/100",
            delta="3 points"
        )
    
    # ESG score evolution
    st.subheader("📈 ESG Score Evolution")
    
    fig = go.Figure()
    
    categories = esg_scores['Category'].tolist()
    current_scores = esg_scores['Current_Score'].tolist()
    previous_scores = esg_scores['Previous_Score'].tolist()
    target_scores = esg_scores['Target_Score'].tolist()
    
    fig.add_trace(go.Bar(
        name='Current Score',
        x=categories,
        y=current_scores,
        marker_color='#1f77b4'
    ))
    
    fig.add_trace(go.Bar(
        name='Previous Score',
        x=categories,
        y=previous_scores,
        marker_color='#ff7f0e',
        opacity=0.7
    ))
    
    if show_targets:
        fig.add_trace(go.Bar(
            name='Target Score',
            x=categories,
            y=target_scores,
            marker_color='#2ca02c',
            opacity=0.5
        ))
    
    fig.update_layout(
        title='ESG Score Evolution',
        xaxis_title='Categories',
        yaxis_title='Score',
        barmode='group',
        height=400
    )
    st.plotly_chart(fig, use_container_width=True)
    
    # ESG radar chart
    st.subheader("🎯 ESG Performance Radar")
    
    fig = go.Figure()
    
    fig.add_trace(go.Scatterpolar(
        r=[env_score, social_score, gov_score, overall_score],
        theta=['Environmental', 'Social', 'Governance', 'Overall'],
        fill='toself',
        name='Current Performance',
        line_color='#1f77b4'
    ))
    
    if show_benchmarks:
        industry_avg_overall = esg_scores['Industry_Average'].mean()
        fig.add_trace(go.Scatterpolar(
            r=[esg_scores[esg_scores['Category'] == 'Environmental']['Industry_Average'].iloc[0],
               esg_scores[esg_scores['Category'] == 'Social']['Industry_Average'].iloc[0],
               esg_scores[esg_scores['Category'] == 'Governance']['Industry_Average'].iloc[0],
               industry_avg_overall],
            theta=['Environmental', 'Social', 'Governance', 'Overall'],
            fill='toself',
            name='Industry Average',
            line_color='#ff7f0e'
        ))
    
    fig.update_layout(
        polar=dict(
            radialaxis=dict(
                visible=True,
                range=[0, 100]
            )),
        showlegend=True,
        title="ESG Performance Radar Chart",
        height=500
    )
    st.plotly_chart(fig, use_container_width=True)

with tab5:
    st.header("📈 ESG Trends & Insights")
    
    # Key insights
    st.subheader("💡 Key Insights")
    
    insights = [
        "🌱 Carbon emissions reduced by 15% year-over-year through renewable energy initiatives",
        "👥 Employee satisfaction increased to 4.2/5.0 following diversity and inclusion programs",
        "🏛️ Board diversity improved to 85%, exceeding industry average of 72%",
        "📊 Overall ESG score improved by 3 points, now ranking in top 25% of industry",
        "⚡ Renewable energy usage increased to 35%, on track to meet 50% target by 2025",
        "🔄 Circular economy initiatives reduced waste by 20% through improved recycling programs"
    ]
    
    for insight in insights:
        st.markdown(f"• {insight}")
    
    # ESG trends over time
    st.subheader("📊 ESG Trends Analysis")
    
    # Generate trend data
    trend_data = pd.DataFrame({
        'Month': pd.date_range(start='2023-01-01', end='2024-01-01', freq='M'),
        'ESG_Score': np.cumsum(np.random.normal(0.5, 0.2, 13)) + 80,
        'Carbon_Reduction': np.cumsum(np.random.normal(1.2, 0.5, 13)),
        'Employee_Satisfaction': np.cumsum(np.random.normal(0.1, 0.05, 13)) + 4.0,
        'Diversity_Index': np.cumsum(np.random.normal(0.01, 0.005, 13)) + 0.75
    })
    
    fig = make_subplots(
        rows=2, cols=2,
        subplot_titles=('ESG Score Trend', 'Carbon Reduction Trend', 
                       'Employee Satisfaction Trend', 'Diversity Index Trend'),
        specs=[[{"secondary_y": False}, {"secondary_y": False}],
               [{"secondary_y": False}, {"secondary_y": False}]]
    )
    
    fig.add_trace(
        go.Scatter(x=trend_data['Month'], y=trend_data['ESG_Score'], 
                  name='ESG Score', line=dict(color='#1f77b4')),
        row=1, col=1
    )
    
    fig.add_trace(
        go.Scatter(x=trend_data['Month'], y=trend_data['Carbon_Reduction'], 
                  name='Carbon Reduction', line=dict(color='#2ca02c')),
        row=1, col=2
    )
    
    fig.add_trace(
        go.Scatter(x=trend_data['Month'], y=trend_data['Employee_Satisfaction'], 
                  name='Employee Satisfaction', line=dict(color='#ff7f0e')),
        row=2, col=1
    )
    
    fig.add_trace(
        go.Scatter(x=trend_data['Month'], y=trend_data['Diversity_Index'], 
                  name='Diversity Index', line=dict(color='#d62728')),
        row=2, col=2
    )
    
    fig.update_layout(height=600, showlegend=False, title_text="ESG Trends Over Time")
    st.plotly_chart(fig, use_container_width=True)
    
    # Recommendations
    st.subheader("🎯 ESG Recommendations")
    
    recommendations = pd.DataFrame({
        'Priority': ['High', 'High', 'Medium', 'Medium', 'Low'],
        'Recommendation': [
            'Implement carbon offset program to achieve net-zero emissions by 2030',
            'Launch employee wellness program to improve satisfaction scores',
            'Enhance supplier diversity program to meet 75% target',
            'Develop comprehensive ESG reporting framework',
            'Invest in renewable energy infrastructure'
        ],
        'Expected_Impact': ['Reduce carbon footprint by 30%', 'Increase satisfaction to 4.5/5.0',
                          'Improve supplier diversity to 75%', 'Enhance transparency score to 95%',
                          'Achieve 50% renewable energy target'],
        'Timeline': ['6 months', '3 months', '12 months', '9 months', '18 months']
    })
    
    st.dataframe(recommendations, use_container_width=True)

# Footer
st.markdown("---")
st.markdown("""
<div style='text-align: center; color: #666;'>
    <p>🌱 EY ESG Analytics Dashboard | Built for Ernst & Young Data Analytics Portfolio</p>
    <p>Demonstrates comprehensive ESG analytics, sustainability reporting, and responsible business practices</p>
</div>
""", unsafe_allow_html=True)
