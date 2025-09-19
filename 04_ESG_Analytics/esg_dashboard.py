"""
ESG Analytics Dashboard
======================

A comprehensive Environmental, Social, and Governance analytics system
demonstrating sustainability metrics, impact measurement, and ESG reporting.

Key Features:
- Carbon Footprint Analysis
- Social Impact Measurement
- Governance Compliance Tracking
- Sustainability Reporting
- ESG Score Calculation
- Impact Assessment

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
        color: #228B22;
        text-align: center;
        margin-bottom: 2rem;
        font-weight: bold;
    }
    .metric-card {
        background-color: #f0fff0;
        padding: 1rem;
        border-radius: 0.5rem;
        border-left: 4px solid #228B22;
        margin: 0.5rem 0;
    }
    .esg-excellent { color: #228B22; }
    .esg-good { color: #32CD32; }
    .esg-fair { color: #FFD700; }
    .esg-poor { color: #FF6347; }
</style>
""", unsafe_allow_html=True)

# Header
st.markdown('<h1 class="main-header">🌱 EY ESG Analytics Dashboard</h1>', unsafe_allow_html=True)

# Sidebar Controls
st.sidebar.header("🎛️ ESG Controls")

# ESG Parameters
st.sidebar.subheader("ESG Parameters")
reporting_period = st.sidebar.selectbox(
    "Reporting Period",
    ["Q1 2024", "Q2 2024", "Q3 2024", "Q4 2024", "Annual 2024"],
    help="ESG reporting period"
)

esg_framework = st.sidebar.selectbox(
    "ESG Framework",
    ["GRI Standards", "SASB", "TCFD", "UN SDGs", "Custom"],
    help="ESG reporting framework"
)

carbon_target_year = st.sidebar.selectbox(
    "Carbon Neutrality Target",
    ["2030", "2035", "2040", "2050"],
    index=3,
    help="Target year for carbon neutrality"
)

# Generate sample ESG data
@st.cache_data
def generate_esg_data():
    """Generate realistic ESG analytics data"""
    np.random.seed(42)
    
    # Generate environmental data
    months = pd.date_range(start='2023-01-01', end='2024-01-01', freq='M')
    
    environmental_data = pd.DataFrame({
        'Month': months,
        'Carbon_Emissions_Tonnes': np.random.normal(5000, 500, len(months)),
        'Energy_Consumption_MWh': np.random.normal(15000, 1500, len(months)),
        'Water_Usage_Liters': np.random.normal(100000, 10000, len(months)),
        'Waste_Generated_Tonnes': np.random.normal(200, 20, len(months)),
        'Renewable_Energy_Percentage': np.random.uniform(25, 45, len(months)),
        'Recycling_Rate': np.random.uniform(60, 85, len(months))
    })
    
    # Generate social data
    social_data = pd.DataFrame({
        'Metric': ['Employee Satisfaction', 'Diversity Index', 'Training Hours', 
                  'Safety Incidents', 'Community Investment', 'Supplier Diversity'],
        'Current_Value': [4.2, 0.75, 40, 2, 500000, 0.65],
        'Target_Value': [4.5, 0.80, 50, 1, 750000, 0.70],
        'Unit': ['Score (1-5)', 'Index (0-1)', 'Hours/Employee', 'Incidents/Month', 'USD', 'Percentage'],
        'Trend': ['Improving', 'Improving', 'Stable', 'Improving', 'Improving', 'Stable']
    })
    
    # Generate governance data
    governance_data = pd.DataFrame({
        'Metric': ['Board Diversity', 'Executive Compensation Ratio', 'Audit Committee Independence',
                  'Whistleblower Reports', 'Ethics Training Completion', 'Data Privacy Compliance'],
        'Current_Value': [0.60, 150, 1.0, 5, 0.95, 0.98],
        'Target_Value': [0.65, 120, 1.0, 3, 1.0, 1.0],
        'Unit': ['Percentage', 'Ratio', 'Score', 'Reports/Month', 'Percentage', 'Percentage'],
        'Trend': ['Improving', 'Improving', 'Stable', 'Improving', 'Improving', 'Stable']
    })
    
    # Generate ESG scores by department
    departments = ['Operations', 'Manufacturing', 'Sales', 'R&D', 'HR', 'Finance']
    esg_scores = pd.DataFrame({
        'Department': departments,
        'Environmental_Score': np.random.uniform(70, 95, len(departments)),
        'Social_Score': np.random.uniform(65, 90, len(departments)),
        'Governance_Score': np.random.uniform(75, 95, len(departments)),
        'Overall_ESG_Score': np.random.uniform(70, 93, len(departments))
    })
    
    # Generate sustainability initiatives
    initiatives = pd.DataFrame({
        'Initiative': ['Solar Panel Installation', 'Employee Wellness Program', 
                      'Supply Chain Audit', 'Carbon Offset Program', 'Diversity Training'],
        'Category': ['Environmental', 'Social', 'Governance', 'Environmental', 'Social'],
        'Status': ['Completed', 'In Progress', 'Planned', 'In Progress', 'Completed'],
        'Impact_Score': [8.5, 7.2, 6.8, 9.1, 7.5],
        'Investment_USD': [2500000, 500000, 200000, 1000000, 300000],
        'ROI_Years': [5, 3, 2, 4, 2]
    })
    
    return environmental_data, social_data, governance_data, esg_scores, initiatives

# Load data
env_data, social_data, gov_data, esg_scores, initiatives = generate_esg_data()

# Main dashboard
tab1, tab2, tab3, tab4, tab5 = st.tabs([
    "🌍 Environmental", 
    "👥 Social", 
    "🏛️ Governance",
    "📊 ESG Overview",
    "🎯 Initiatives"
])

with tab1:
    st.header("🌍 Environmental Impact Analysis")
    
    # Environmental KPIs
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        current_emissions = env_data['Carbon_Emissions_Tonnes'].iloc[-1]
        target_emissions = current_emissions * 0.8  # 20% reduction target
        st.metric(
            label="Carbon Emissions",
            value=f"{current_emissions:,.0f} tonnes",
            delta=f"{((current_emissions - target_emissions) / target_emissions * 100):.1f}% vs target"
        )
    
    with col2:
        renewable_percentage = env_data['Renewable_Energy_Percentage'].iloc[-1]
        st.metric(
            label="Renewable Energy",
            value=f"{renewable_percentage:.1f}%",
            delta="5.2%"
        )
    
    with col3:
        recycling_rate = env_data['Recycling_Rate'].iloc[-1]
        st.metric(
            label="Recycling Rate",
            value=f"{recycling_rate:.1f}%",
            delta="2.1%"
        )
    
    with col4:
        water_usage = env_data['Water_Usage_Liters'].iloc[-1]
        st.metric(
            label="Water Usage",
            value=f"{water_usage:,.0f} L",
            delta="-3.5%"
        )
    
    # Carbon Footprint Trend
    st.subheader("📈 Carbon Footprint Trend")
    
    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=env_data['Month'],
        y=env_data['Carbon_Emissions_Tonnes'],
        mode='lines+markers',
        name='Carbon Emissions',
        line=dict(color='#DC143C', width=3)
    ))
    
    # Add target line
    target_line = [current_emissions * 0.8] * len(env_data)
    fig.add_trace(go.Scatter(
        x=env_data['Month'],
        y=target_line,
        mode='lines',
        name='2024 Target',
        line=dict(color='#228B22', width=2, dash='dash')
    ))
    
    fig.update_layout(
        title='Carbon Emissions Trend vs Target',
        xaxis_title='Month',
        yaxis_title='Carbon Emissions (tonnes)',
        height=400
    )
    st.plotly_chart(fig, use_container_width=True)
    
    # Environmental Metrics Comparison
    st.subheader("📊 Environmental Metrics Overview")
    
    col1, col2 = st.columns(2)
    
    with col1:
        # Energy consumption
        fig = px.line(
            env_data,
            x='Month',
            y='Energy_Consumption_MWh',
            title='Energy Consumption Trend',
            color_discrete_sequence=['#FF8C00']
        )
        fig.update_layout(height=300)
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        # Waste generation
        fig = px.line(
            env_data,
            x='Month',
            y='Waste_Generated_Tonnes',
            title='Waste Generation Trend',
            color_discrete_sequence=['#8B4513']
        )
        fig.update_layout(height=300)
        st.plotly_chart(fig, use_container_width=True)
    
    # Environmental Performance by Category
    st.subheader("🎯 Environmental Performance by Category")
    
    env_categories = pd.DataFrame({
        'Category': ['Energy Efficiency', 'Waste Management', 'Water Conservation', 'Carbon Reduction'],
        'Current_Score': [85, 78, 82, 75],
        'Target_Score': [90, 85, 88, 85],
        'Progress': [85/90*100, 78/85*100, 82/88*100, 75/85*100]
    })
    
    fig = px.bar(
        env_categories,
        x='Category',
        y='Current_Score',
        color='Progress',
        title='Environmental Performance by Category',
        color_continuous_scale='Greens'
    )
    fig.update_layout(height=400)
    st.plotly_chart(fig, use_container_width=True)

with tab2:
    st.header("👥 Social Impact Analysis")
    
    # Social KPIs
    col1, col2, col3 = st.columns(3)
    
    with col1:
        employee_satisfaction = social_data.iloc[0]['Current_Value']
        st.metric(
            label="Employee Satisfaction",
            value=f"{employee_satisfaction:.1f}/5.0",
            delta="0.2"
        )
    
    with col2:
        diversity_index = social_data.iloc[1]['Current_Value']
        st.metric(
            label="Diversity Index",
            value=f"{diversity_index:.2f}",
            delta="0.05"
        )
    
    with col3:
        safety_incidents = social_data.iloc[3]['Current_Value']
        st.metric(
            label="Safety Incidents",
            value=f"{safety_incidents}",
            delta="-1"
        )
    
    # Social Metrics Dashboard
    st.subheader("📊 Social Metrics Dashboard")
    
    # Create progress bars for social metrics
    for idx, row in social_data.iterrows():
        progress = (row['Current_Value'] / row['Target_Value']) * 100
        st.progress(min(progress, 100) / 100)
        st.write(f"**{row['Metric']}**: {row['Current_Value']:.2f} {row['Unit']} "
                f"(Target: {row['Target_Value']:.2f}) - {row['Trend']}")
    
    # Social Impact Trends
    st.subheader("📈 Social Impact Trends")
    
    # Generate trend data
    months = pd.date_range(start='2023-01-01', end='2024-01-01', freq='M')
    social_trends = pd.DataFrame({
        'Month': months,
        'Employee_Satisfaction': np.random.normal(4.2, 0.1, len(months)),
        'Diversity_Index': np.random.normal(0.75, 0.02, len(months)),
        'Training_Hours': np.random.normal(40, 5, len(months)),
        'Community_Investment': np.random.normal(500000, 50000, len(months))
    })
    
    fig = make_subplots(
        rows=2, cols=2,
        subplot_titles=('Employee Satisfaction', 'Diversity Index', 
                       'Training Hours', 'Community Investment'),
        vertical_spacing=0.1
    )
    
    fig.add_trace(
        go.Scatter(x=social_trends['Month'], y=social_trends['Employee_Satisfaction'], 
                  name='Employee Satisfaction', line=dict(color='#1f77b4')),
        row=1, col=1
    )
    
    fig.add_trace(
        go.Scatter(x=social_trends['Month'], y=social_trends['Diversity_Index'], 
                  name='Diversity Index', line=dict(color='#ff7f0e')),
        row=1, col=2
    )
    
    fig.add_trace(
        go.Scatter(x=social_trends['Month'], y=social_trends['Training_Hours'], 
                  name='Training Hours', line=dict(color='#2ca02c')),
        row=2, col=1
    )
    
    fig.add_trace(
        go.Scatter(x=social_trends['Month'], y=social_trends['Community_Investment'], 
                  name='Community Investment', line=dict(color='#d62728')),
        row=2, col=2
    )
    
    fig.update_layout(height=500, showlegend=False)
    st.plotly_chart(fig, use_container_width=True)
    
    # Social Impact by Department
    st.subheader("🏢 Social Impact by Department")
    
    dept_social_data = pd.DataFrame({
        'Department': ['Operations', 'Manufacturing', 'Sales', 'R&D', 'HR', 'Finance'],
        'Employee_Satisfaction': [4.1, 4.3, 4.0, 4.5, 4.4, 4.2],
        'Diversity_Score': [0.72, 0.68, 0.78, 0.82, 0.85, 0.75],
        'Training_Hours': [35, 45, 30, 55, 50, 40],
        'Safety_Score': [8.5, 7.8, 9.2, 9.5, 9.0, 8.8]
    })
    
    fig = px.scatter(
        dept_social_data,
        x='Employee_Satisfaction',
        y='Diversity_Score',
        size='Training_Hours',
        color='Safety_Score',
        hover_data=['Department'],
        title='Social Performance by Department',
        color_continuous_scale='RdYlGn'
    )
    fig.update_layout(height=400)
    st.plotly_chart(fig, use_container_width=True)

with tab3:
    st.header("🏛️ Governance Analysis")
    
    # Governance KPIs
    col1, col2, col3 = st.columns(3)
    
    with col1:
        board_diversity = gov_data.iloc[0]['Current_Value']
        st.metric(
            label="Board Diversity",
            value=f"{board_diversity:.1%}",
            delta="5%"
        )
    
    with col2:
        audit_independence = gov_data.iloc[2]['Current_Value']
        st.metric(
            label="Audit Independence",
            value=f"{audit_independence:.1%}",
            delta="0%"
        )
    
    with col3:
        ethics_training = gov_data.iloc[4]['Current_Value']
        st.metric(
            label="Ethics Training",
            value=f"{ethics_training:.1%}",
            delta="2%"
        )
    
    # Governance Metrics Dashboard
    st.subheader("📊 Governance Metrics Dashboard")
    
    # Create progress bars for governance metrics
    for idx, row in gov_data.iterrows():
        if row['Unit'] == 'Percentage':
            progress = row['Current_Value']
        else:
            progress = (row['Current_Value'] / row['Target_Value']) * 100
        st.progress(min(progress, 100) / 100)
        st.write(f"**{row['Metric']}**: {row['Current_Value']:.2f} {row['Unit']} "
                f"(Target: {row['Target_Value']:.2f}) - {row['Trend']}")
    
    # Governance Risk Assessment
    st.subheader("⚠️ Governance Risk Assessment")
    
    governance_risks = pd.DataFrame({
        'Risk_Category': ['Board Composition', 'Executive Compensation', 'Audit Quality',
                         'Regulatory Compliance', 'Data Security', 'Ethics & Culture'],
        'Risk_Level': ['Low', 'Medium', 'Low', 'Low', 'Medium', 'Low'],
        'Impact_Score': [3, 6, 2, 2, 5, 3],
        'Probability_Score': [2, 4, 1, 1, 3, 2],
        'Mitigation_Status': ['Completed', 'In Progress', 'Completed', 'Completed', 'In Progress', 'Completed']
    })
    
    fig = px.scatter(
        governance_risks,
        x='Probability_Score',
        y='Impact_Score',
        size='Impact_Score',
        color='Risk_Level',
        hover_data=['Risk_Category', 'Mitigation_Status'],
        title='Governance Risk Assessment Matrix',
        color_discrete_map={'Low': 'green', 'Medium': 'orange', 'High': 'red'}
    )
    
    # Add risk zones
    fig.add_shape(
        type="rect", x0=0, y0=0, x1=3, y1=3,
        fillcolor="green", opacity=0.1, line=dict(color="green")
    )
    fig.add_shape(
        type="rect", x0=3, y0=3, x1=6, y1=6,
        fillcolor="red", opacity=0.1, line=dict(color="red")
    )
    
    fig.update_layout(height=400)
    st.plotly_chart(fig, use_container_width=True)
    
    # Compliance Timeline
    st.subheader("📅 Compliance Timeline")
    
    compliance_schedule = pd.DataFrame({
        'Regulation': ['SOX Compliance', 'GDPR Review', 'Audit Committee Meeting',
                      'Board Diversity Review', 'Ethics Training Update'],
        'Due_Date': ['2024-03-15', '2024-05-25', '2024-06-30', '2024-09-15', '2024-12-31'],
        'Status': ['Completed', 'On Track', 'On Track', 'Planned', 'Planned'],
        'Priority': ['High', 'High', 'Medium', 'Medium', 'Low']
    })
    
    fig = px.timeline(
        compliance_schedule,
        x_start='Due_Date',
        x_end='Due_Date',
        y='Regulation',
        color='Priority',
        title='Governance Compliance Schedule',
        color_discrete_map={'High': 'red', 'Medium': 'orange', 'Low': 'green'}
    )
    
    fig.update_layout(height=400)
    st.plotly_chart(fig, use_container_width=True)

with tab4:
    st.header("📊 ESG Overview Dashboard")
    
    # Overall ESG Score
    overall_esg_score = esg_scores['Overall_ESG_Score'].mean()
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric(
            label="Overall ESG Score",
            value=f"{overall_esg_score:.1f}/100",
            delta="3.2"
        )
    
    with col2:
        env_score = esg_scores['Environmental_Score'].mean()
        st.metric(
            label="Environmental Score",
            value=f"{env_score:.1f}/100",
            delta="2.1"
        )
    
    with col3:
        social_score = esg_scores['Social_Score'].mean()
        st.metric(
            label="Social Score",
            value=f"{social_score:.1f}/100",
            delta="4.3"
        )
    
    with col4:
        gov_score = esg_scores['Governance_Score'].mean()
        st.metric(
            label="Governance Score",
            value=f"{gov_score:.1f}/100",
            delta="1.8"
        )
    
    # ESG Score Distribution
    st.subheader("📈 ESG Score Distribution by Department")
    
    fig = px.bar(
        esg_scores,
        x='Department',
        y=['Environmental_Score', 'Social_Score', 'Governance_Score'],
        title='ESG Scores by Department',
        barmode='group',
        color_discrete_sequence=['#228B22', '#1f77b4', '#ff7f0e']
    )
    fig.update_layout(height=400)
    st.plotly_chart(fig, use_container_width=True)
    
    # ESG Performance Radar Chart
    st.subheader("🎯 ESG Performance Radar Chart")
    
    # Select department for radar chart
    selected_dept = st.selectbox(
        "Select Department for Detailed Analysis",
        esg_scores['Department'].unique()
    )
    
    dept_data = esg_scores[esg_scores['Department'] == selected_dept].iloc[0]
    
    categories = ['Environmental', 'Social', 'Governance', 'Overall']
    values = [dept_data['Environmental_Score'], dept_data['Social_Score'], 
              dept_data['Governance_Score'], dept_data['Overall_ESG_Score']]
    
    fig = go.Figure()
    
    fig.add_trace(go.Scatterpolar(
        r=values,
        theta=categories,
        fill='toself',
        name=selected_dept,
        line_color='#228B22'
    ))
    
    fig.update_layout(
        polar=dict(
            radialaxis=dict(
                visible=True,
                range=[0, 100]
            )),
        showlegend=True,
        title=f'ESG Performance - {selected_dept}',
        height=400
    )
    
    st.plotly_chart(fig, use_container_width=True)
    
    # ESG Trends Over Time
    st.subheader("📊 ESG Trends Over Time")
    
    # Generate historical ESG data
    months = pd.date_range(start='2023-01-01', end='2024-01-01', freq='M')
    esg_trends = pd.DataFrame({
        'Month': months,
        'Environmental_Score': np.random.normal(82, 2, len(months)),
        'Social_Score': np.random.normal(78, 3, len(months)),
        'Governance_Score': np.random.normal(85, 1.5, len(months)),
        'Overall_ESG_Score': np.random.normal(82, 2, len(months))
    })
    
    fig = go.Figure()
    
    fig.add_trace(go.Scatter(x=esg_trends['Month'], y=esg_trends['Environmental_Score'], 
                             name='Environmental', line=dict(color='#228B22')))
    fig.add_trace(go.Scatter(x=esg_trends['Month'], y=esg_trends['Social_Score'], 
                             name='Social', line=dict(color='#1f77b4')))
    fig.add_trace(go.Scatter(x=esg_trends['Month'], y=esg_trends['Governance_Score'], 
                             name='Governance', line=dict(color='#ff7f0e')))
    fig.add_trace(go.Scatter(x=esg_trends['Month'], y=esg_trends['Overall_ESG_Score'], 
                             name='Overall', line=dict(color='#d62728', width=3)))
    
    fig.update_layout(
        title='ESG Score Trends Over Time',
        xaxis_title='Month',
        yaxis_title='ESG Score',
        height=400
    )
    
    st.plotly_chart(fig, use_container_width=True)

with tab5:
    st.header("🎯 Sustainability Initiatives")
    
    # Initiative Overview
    st.subheader("📊 Initiative Overview")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        total_initiatives = len(initiatives)
        st.metric(
            label="Total Initiatives",
            value=f"{total_initiatives}",
            delta="2 new"
        )
    
    with col2:
        completed_initiatives = len(initiatives[initiatives['Status'] == 'Completed'])
        st.metric(
            label="Completed",
            value=f"{completed_initiatives}",
            delta="1"
        )
    
    with col3:
        total_investment = initiatives['Investment_USD'].sum()
        st.metric(
            label="Total Investment",
            value=f"${total_investment:,.0f}",
            delta="$500K"
        )
    
    # Initiative Performance
    st.subheader("📈 Initiative Performance Analysis")
    
    fig = px.scatter(
        initiatives,
        x='Investment_USD',
        y='Impact_Score',
        size='ROI_Years',
        color='Status',
        hover_data=['Initiative', 'Category'],
        title='Initiative Performance: Investment vs Impact',
        color_discrete_map={'Completed': 'green', 'In Progress': 'orange', 'Planned': 'blue'}
    )
    fig.update_layout(height=400)
    st.plotly_chart(fig, use_container_width=True)
    
    # Initiative ROI Analysis
    st.subheader("💰 Initiative ROI Analysis")
    
    fig = px.bar(
        initiatives,
        x='Initiative',
        y='ROI_Years',
        color='Category',
        title='Return on Investment Timeline by Initiative',
        color_discrete_sequence=px.colors.qualitative.Set3
    )
    fig.update_layout(height=400)
    st.plotly_chart(fig, use_container_width=True)
    
    # Initiative Status Summary
    st.subheader("📋 Initiative Status Summary")
    
    initiative_summary = initiatives.groupby(['Category', 'Status']).agg({
        'Initiative': 'count',
        'Investment_USD': 'sum',
        'Impact_Score': 'mean'
    }).round(2)
    
    st.dataframe(initiative_summary, use_container_width=True)
    
    # Initiative Timeline
    st.subheader("📅 Initiative Timeline")
    
    # Add start dates for initiatives
    initiatives['Start_Date'] = pd.to_datetime(['2023-01-01', '2023-06-01', '2024-01-01', 
                                              '2023-09-01', '2023-03-01'])
    initiatives['End_Date'] = pd.to_datetime(['2023-12-31', '2024-12-31', '2024-06-30', 
                                             '2024-06-30', '2023-12-31'])
    
    fig = px.timeline(
        initiatives,
        x_start='Start_Date',
        x_end='End_Date',
        y='Initiative',
        color='Status',
        title='Sustainability Initiative Timeline',
        color_discrete_map={'Completed': 'green', 'In Progress': 'orange', 'Planned': 'blue'}
    )
    
    fig.update_layout(height=400)
    st.plotly_chart(fig, use_container_width=True)

# Footer
st.markdown("---")
st.markdown("""
<div style='text-align: center; color: #666;'>
    <p>🌱 EY ESG Analytics Dashboard | Built for Ernst & Young Data Analytics Portfolio</p>
    <p>Demonstrates advanced sustainability metrics, impact measurement, and ESG reporting capabilities</p>
</div>
""", unsafe_allow_html=True)
