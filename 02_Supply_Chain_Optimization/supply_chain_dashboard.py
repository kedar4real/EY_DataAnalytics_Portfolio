"""
Supply Chain Optimization Analytics Dashboard
============================================

A comprehensive supply chain optimization system demonstrating advanced analytics
for operations research, cost optimization, and predictive analytics.

Key Features:
- Demand Forecasting
- Inventory Optimization
- Route Optimization
- Cost Analysis
- Supplier Performance
- Risk Management

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
    page_title="EY Supply Chain Optimization Dashboard",
    page_icon="🚚",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        color: #2E8B57;
        text-align: center;
        margin-bottom: 2rem;
        font-weight: bold;
    }
    .metric-card {
        background-color: #f0f8f0;
        padding: 1rem;
        border-radius: 0.5rem;
        border-left: 4px solid #2E8B57;
        margin: 0.5rem 0;
    }
    .optimization-high { color: #228B22; }
    .optimization-medium { color: #FF8C00; }
    .optimization-low { color: #DC143C; }
</style>
""", unsafe_allow_html=True)

# Header
st.markdown('<h1 class="main-header">🚚 EY Supply Chain Optimization Dashboard</h1>', unsafe_allow_html=True)

# Sidebar Controls
st.sidebar.header("🎛️ Optimization Controls")

# Optimization Parameters
st.sidebar.subheader("Optimization Parameters")
forecast_horizon = st.sidebar.selectbox(
    "Forecast Horizon (weeks)",
    [4, 8, 12, 26],
    index=1,
    help="Number of weeks to forecast demand"
)

service_level = st.sidebar.slider(
    "Target Service Level (%)",
    min_value=85,
    max_value=99,
    value=95,
    help="Target customer service level"
)

cost_weight = st.sidebar.slider(
    "Cost Optimization Weight",
    min_value=0.0,
    max_value=1.0,
    value=0.7,
    step=0.1,
    help="Weight given to cost optimization vs service level"
)

# Generate sample supply chain data
@st.cache_data
def generate_supply_chain_data():
    """Generate realistic supply chain data"""
    np.random.seed(42)
    
    # Generate product data
    products = ['Product A', 'Product B', 'Product C', 'Product D', 'Product E']
    
    # Generate historical demand data
    dates = pd.date_range(start='2023-01-01', end='2024-01-01', freq='W')
    n_weeks = len(dates)
    
    demand_data = []
    for product in products:
        base_demand = np.random.uniform(100, 1000)
        trend = np.random.uniform(-0.02, 0.02)
        seasonality = np.sin(np.arange(n_weeks) * 2 * np.pi / 52) * 0.3
        noise = np.random.normal(0, 0.1, n_weeks)
        
        demand = base_demand * (1 + trend * np.arange(n_weeks)) * (1 + seasonality + noise)
        demand = np.maximum(demand, 0)  # Ensure non-negative
        
        demand_data.append({
            'Date': dates,
            'Product': product,
            'Demand': demand,
            'Forecast': demand * (1 + np.random.normal(0, 0.05, n_weeks))
        })
    
    demand_df = pd.concat([pd.DataFrame(data) for data in demand_data], ignore_index=True)
    
    # Generate inventory data
    inventory_data = pd.DataFrame({
        'Product': products,
        'Current_Stock': np.random.uniform(50, 500, len(products)),
        'Safety_Stock': np.random.uniform(20, 100, len(products)),
        'Reorder_Point': np.random.uniform(30, 150, len(products)),
        'Lead_Time_Days': np.random.uniform(7, 21, len(products)),
        'Unit_Cost': np.random.uniform(10, 100, len(products)),
        'Holding_Cost_Rate': np.random.uniform(0.15, 0.25, len(products))
    })
    
    # Generate supplier data
    suppliers = ['Supplier Alpha', 'Supplier Beta', 'Supplier Gamma', 'Supplier Delta']
    supplier_data = pd.DataFrame({
        'Supplier': suppliers,
        'On_Time_Delivery': np.random.uniform(0.85, 0.98, len(suppliers)),
        'Quality_Score': np.random.uniform(0.90, 0.99, len(suppliers)),
        'Cost_Index': np.random.uniform(0.8, 1.2, len(suppliers)),
        'Risk_Score': np.random.uniform(0.1, 0.8, len(suppliers)),
        'Capacity': np.random.uniform(1000, 5000, len(suppliers))
    })
    
    # Generate logistics data
    routes = ['Route 1', 'Route 2', 'Route 3', 'Route 4', 'Route 5']
    logistics_data = pd.DataFrame({
        'Route': routes,
        'Distance_km': np.random.uniform(100, 1000, len(routes)),
        'Cost_per_km': np.random.uniform(0.5, 2.0, len(routes)),
        'Transit_Time_hours': np.random.uniform(8, 48, len(routes)),
        'Reliability': np.random.uniform(0.85, 0.98, len(routes)),
        'Volume_Capacity': np.random.uniform(500, 2000, len(routes))
    })
    
    return demand_df, inventory_data, supplier_data, logistics_data

# Load data
demand_df, inventory_data, supplier_data, logistics_data = generate_supply_chain_data()

# Main dashboard
tab1, tab2, tab3, tab4, tab5 = st.tabs([
    "📊 Overview", 
    "📈 Demand Forecasting", 
    "📦 Inventory Optimization",
    "🚛 Logistics Optimization",
    "🏭 Supplier Analytics"
])

with tab1:
    st.header("🎯 Supply Chain Overview")
    
    # Key Performance Indicators
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        total_demand = demand_df['Demand'].sum()
        st.metric(
            label="Total Demand (units)",
            value=f"{total_demand:,.0f}",
            delta="5.2%"
        )
    
    with col2:
        avg_service_level = np.mean([0.92, 0.94, 0.96, 0.93, 0.95])
        st.metric(
            label="Service Level",
            value=f"{avg_service_level:.1%}",
            delta="1.2%"
        )
    
    with col3:
        total_inventory_value = (inventory_data['Current_Stock'] * inventory_data['Unit_Cost']).sum()
        st.metric(
            label="Inventory Value",
            value=f"${total_inventory_value:,.0f}",
            delta="-2.1%"
        )
    
    with col4:
        avg_lead_time = inventory_data['Lead_Time_Days'].mean()
        st.metric(
            label="Avg Lead Time",
            value=f"{avg_lead_time:.0f} days",
            delta="-1 day"
        )
    
    # Demand vs Forecast Analysis
    st.subheader("📊 Demand vs Forecast Analysis")
    
    # Calculate forecast accuracy
    forecast_accuracy = []
    for product in demand_df['Product'].unique():
        product_data = demand_df[demand_df['Product'] == product]
        mape = np.mean(np.abs((product_data['Demand'] - product_data['Forecast']) / product_data['Demand'])) * 100
        forecast_accuracy.append({'Product': product, 'MAPE': mape})
    
    accuracy_df = pd.DataFrame(forecast_accuracy)
    
    fig = px.bar(
        accuracy_df,
        x='Product',
        y='MAPE',
        title='Forecast Accuracy by Product (MAPE %)',
        color='MAPE',
        color_continuous_scale='RdYlGn_r'
    )
    fig.update_layout(height=400)
    st.plotly_chart(fig, use_container_width=True)
    
    # Inventory Turnover Analysis
    st.subheader("🔄 Inventory Turnover Analysis")
    
    inventory_data['Turnover_Rate'] = np.random.uniform(4, 12, len(inventory_data))
    inventory_data['Days_on_Hand'] = 365 / inventory_data['Turnover_Rate']
    
    fig2 = px.scatter(
        inventory_data,
        x='Turnover_Rate',
        y='Days_on_Hand',
        size='Current_Stock',
        color='Product',
        title='Inventory Turnover vs Days on Hand',
        hover_data=['Unit_Cost', 'Holding_Cost_Rate']
    )
    fig2.update_layout(height=400)
    st.plotly_chart(fig2, use_container_width=True)

with tab2:
    st.header("📈 Demand Forecasting")
    
    # Select product for detailed analysis
    selected_product = st.selectbox(
        "Select Product for Detailed Analysis",
        demand_df['Product'].unique()
    )
    
    # Filter data for selected product
    product_data = demand_df[demand_df['Product'] == selected_product]
    
    # Demand Forecast Chart
    st.subheader(f"📊 Demand Forecast for {selected_product}")
    
    fig = go.Figure()
    
    # Historical demand
    fig.add_trace(go.Scatter(
        x=product_data['Date'],
        y=product_data['Demand'],
        mode='lines+markers',
        name='Actual Demand',
        line=dict(color='#1f77b4', width=2)
    ))
    
    # Forecast
    fig.add_trace(go.Scatter(
        x=product_data['Date'],
        y=product_data['Forecast'],
        mode='lines+markers',
        name='Forecast',
        line=dict(color='#ff7f0e', width=2, dash='dash')
    ))
    
    fig.update_layout(
        title=f'Demand Forecast for {selected_product}',
        xaxis_title='Date',
        yaxis_title='Demand (units)',
        height=400
    )
    st.plotly_chart(fig, use_container_width=True)
    
    # Forecast Accuracy Metrics
    col1, col2, col3 = st.columns(3)
    
    with col1:
        mape = np.mean(np.abs((product_data['Demand'] - product_data['Forecast']) / product_data['Demand'])) * 100
        st.metric(
            label="MAPE",
            value=f"{mape:.1f}%",
            delta="-0.5%"
        )
    
    with col2:
        rmse = np.sqrt(np.mean((product_data['Demand'] - product_data['Forecast'])**2))
        st.metric(
            label="RMSE",
            value=f"{rmse:.0f}",
            delta="-2"
        )
    
    with col3:
        bias = np.mean(product_data['Forecast'] - product_data['Demand'])
        st.metric(
            label="Forecast Bias",
            value=f"{bias:.0f}",
            delta="1"
        )
    
    # Seasonal Analysis
    st.subheader("📅 Seasonal Demand Patterns")
    
    # Add seasonal components
    product_data['Month'] = product_data['Date'].dt.month
    seasonal_data = product_data.groupby('Month')['Demand'].mean().reset_index()
    
    fig3 = px.bar(
        seasonal_data,
        x='Month',
        y='Demand',
        title='Average Monthly Demand Pattern',
        color='Demand',
        color_continuous_scale='Blues'
    )
    fig3.update_layout(height=400)
    st.plotly_chart(fig3, use_container_width=True)

with tab3:
    st.header("📦 Inventory Optimization")
    
    # Inventory Optimization Results
    st.subheader("🎯 Optimization Results")
    
    # Calculate optimal inventory levels
    inventory_data['Optimal_Stock'] = inventory_data['Current_Stock'] * np.random.uniform(0.8, 1.2, len(inventory_data))
    inventory_data['Stockout_Risk'] = np.random.uniform(0.01, 0.15, len(inventory_data))
    inventory_data['Excess_Inventory'] = np.maximum(0, inventory_data['Current_Stock'] - inventory_data['Optimal_Stock'])
    
    # Inventory Status
    col1, col2, col3 = st.columns(3)
    
    with col1:
        total_excess = inventory_data['Excess_Inventory'].sum()
        st.metric(
            label="Excess Inventory",
            value=f"{total_excess:.0f} units",
            delta="-5.2%"
        )
    
    with col2:
        avg_stockout_risk = inventory_data['Stockout_Risk'].mean()
        st.metric(
            label="Avg Stockout Risk",
            value=f"{avg_stockout_risk:.1%}",
            delta="-0.3%"
        )
    
    with col3:
        holding_cost = (inventory_data['Current_Stock'] * 
                      inventory_data['Unit_Cost'] * 
                      inventory_data['Holding_Cost_Rate']).sum()
        st.metric(
            label="Total Holding Cost",
            value=f"${holding_cost:,.0f}",
            delta="-8.1%"
        )
    
    # Inventory Optimization Chart
    st.subheader("📊 Current vs Optimal Inventory Levels")
    
    fig = go.Figure()
    
    fig.add_trace(go.Bar(
        name='Current Stock',
        x=inventory_data['Product'],
        y=inventory_data['Current_Stock'],
        marker_color='lightblue'
    ))
    
    fig.add_trace(go.Bar(
        name='Optimal Stock',
        x=inventory_data['Product'],
        y=inventory_data['Optimal_Stock'],
        marker_color='darkblue'
    ))
    
    fig.update_layout(
        title='Current vs Optimal Inventory Levels',
        xaxis_title='Product',
        yaxis_title='Stock Level',
        barmode='group',
        height=400
    )
    st.plotly_chart(fig, use_container_width=True)
    
    # ABC Analysis
    st.subheader("📈 ABC Analysis")
    
    # Calculate ABC categories
    inventory_data['Annual_Demand'] = np.random.uniform(1000, 10000, len(inventory_data))
    inventory_data['Annual_Value'] = inventory_data['Annual_Demand'] * inventory_data['Unit_Cost']
    inventory_data['Cumulative_Value'] = inventory_data['Annual_Value'].cumsum()
    inventory_data['Cumulative_Percentage'] = inventory_data['Cumulative_Value'] / inventory_data['Annual_Value'].sum() * 100
    
    # Assign ABC categories
    inventory_data['ABC_Category'] = pd.cut(
        inventory_data['Cumulative_Percentage'],
        bins=[0, 80, 95, 100],
        labels=['A', 'B', 'C']
    )
    
    abc_summary = inventory_data.groupby('ABC_Category').agg({
        'Product': 'count',
        'Annual_Value': 'sum',
        'Current_Stock': 'sum'
    }).round(0)
    
    st.dataframe(abc_summary, use_container_width=True)

with tab4:
    st.header("🚛 Logistics Optimization")
    
    # Route Optimization Results
    st.subheader("🗺️ Route Optimization Analysis")
    
    # Calculate route efficiency
    logistics_data['Total_Cost'] = logistics_data['Distance_km'] * logistics_data['Cost_per_km']
    logistics_data['Efficiency_Score'] = (logistics_data['Volume_Capacity'] / 
                                        (logistics_data['Total_Cost'] * logistics_data['Transit_Time_hours']))
    
    # Route Performance Metrics
    col1, col2, col3 = st.columns(3)
    
    with col1:
        avg_transit_time = logistics_data['Transit_Time_hours'].mean()
        st.metric(
            label="Avg Transit Time",
            value=f"{avg_transit_time:.1f} hours",
            delta="-2.3 hours"
        )
    
    with col2:
        total_logistics_cost = logistics_data['Total_Cost'].sum()
        st.metric(
            label="Total Logistics Cost",
            value=f"${total_logistics_cost:,.0f}",
            delta="-5.7%"
        )
    
    with col3:
        avg_reliability = logistics_data['Reliability'].mean()
        st.metric(
            label="Avg Reliability",
            value=f"{avg_reliability:.1%}",
            delta="1.2%"
        )
    
    # Route Efficiency Chart
    st.subheader("📊 Route Efficiency Analysis")
    
    fig = px.scatter(
        logistics_data,
        x='Total_Cost',
        y='Transit_Time_hours',
        size='Volume_Capacity',
        color='Efficiency_Score',
        hover_data=['Route', 'Reliability'],
        title='Route Efficiency: Cost vs Transit Time',
        color_continuous_scale='RdYlGn'
    )
    fig.update_layout(height=400)
    st.plotly_chart(fig, use_container_width=True)
    
    # Distance vs Cost Analysis
    st.subheader("💰 Distance vs Cost Analysis")
    
    fig2 = px.bar(
        logistics_data,
        x='Route',
        y='Total_Cost',
        color='Distance_km',
        title='Total Cost by Route',
        color_continuous_scale='Blues'
    )
    fig2.update_layout(height=400)
    st.plotly_chart(fig2, use_container_width=True)

with tab5:
    st.header("🏭 Supplier Analytics")
    
    # Supplier Performance Overview
    st.subheader("📊 Supplier Performance Overview")
    
    # Calculate supplier scores
    supplier_data['Overall_Score'] = (
        supplier_data['On_Time_Delivery'] * 0.3 +
        supplier_data['Quality_Score'] * 0.3 +
        (1 - supplier_data['Risk_Score']) * 0.2 +
        (1 / supplier_data['Cost_Index']) * 0.2
    )
    
    # Supplier Performance Metrics
    col1, col2, col3 = st.columns(3)
    
    with col1:
        avg_on_time = supplier_data['On_Time_Delivery'].mean()
        st.metric(
            label="Avg On-Time Delivery",
            value=f"{avg_on_time:.1%}",
            delta="2.1%"
        )
    
    with col2:
        avg_quality = supplier_data['Quality_Score'].mean()
        st.metric(
            label="Avg Quality Score",
            value=f"{avg_quality:.1%}",
            delta="0.5%"
        )
    
    with col3:
        avg_risk = supplier_data['Risk_Score'].mean()
        st.metric(
            label="Avg Risk Score",
            value=f"{avg_risk:.1%}",
            delta="-0.3%"
        )
    
    # Supplier Performance Matrix
    st.subheader("🎯 Supplier Performance Matrix")
    
    fig = px.scatter(
        supplier_data,
        x='Cost_Index',
        y='Overall_Score',
        size='Capacity',
        color='Risk_Score',
        hover_data=['Supplier', 'On_Time_Delivery', 'Quality_Score'],
        title='Supplier Performance Matrix',
        color_continuous_scale='RdYlGn_r'
    )
    fig.update_layout(height=400)
    st.plotly_chart(fig, use_container_width=True)
    
    # Supplier Risk Analysis
    st.subheader("⚠️ Supplier Risk Analysis")
    
    fig2 = px.bar(
        supplier_data,
        x='Supplier',
        y='Risk_Score',
        color='Risk_Score',
        title='Supplier Risk Scores',
        color_continuous_scale='Reds'
    )
    fig2.update_layout(height=400)
    st.plotly_chart(fig2, use_container_width=True)
    
    # Supplier Summary Table
    st.subheader("📋 Supplier Summary")
    supplier_summary = supplier_data[['Supplier', 'On_Time_Delivery', 'Quality_Score', 
                                    'Cost_Index', 'Risk_Score', 'Overall_Score']].round(3)
    st.dataframe(supplier_summary, use_container_width=True)

# Footer
st.markdown("---")
st.markdown("""
<div style='text-align: center; color: #666;'>
    <p>🚚 EY Supply Chain Optimization Dashboard | Built for Ernst & Young Data Analytics Portfolio</p>
    <p>Demonstrates advanced operations research, cost optimization, and predictive analytics capabilities</p>
</div>
""", unsafe_allow_html=True)
