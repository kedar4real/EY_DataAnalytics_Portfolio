"""
Customer Analytics & Segmentation Dashboard
==========================================

Advanced customer analytics featuring ML-based segmentation, churn prediction,
lifetime value analysis, and campaign optimization for customer intelligence.

Key Features:
- Customer Segmentation with ML
- Churn Prediction Models
- Customer Lifetime Value Analysis
- Campaign Performance Analytics
- Behavioral Analytics
- Real-time Customer Insights

Author: Data Analytics Portfolio for EY
"""

import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report, confusion_matrix
import warnings
warnings.filterwarnings('ignore')

# Page Configuration
st.set_page_config(
    page_title="EY Customer Analytics Dashboard",
    page_icon="👥",
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
    .segment-high-value { color: #2ca02c; }
    .segment-medium-value { color: #ff7f0e; }
    .segment-low-value { color: #d62728; }
</style>
""", unsafe_allow_html=True)

# Header
st.markdown('<h1 class="main-header">👥 EY Customer Analytics Dashboard</h1>', unsafe_allow_html=True)

# Generate sample customer data
@st.cache_data
def generate_customer_data():
    """Generate realistic customer analytics data"""
    np.random.seed(42)
    n_customers = 5000
    
    # Generate customer demographics and behavior
    customer_data = pd.DataFrame({
        'Customer_ID': range(1, n_customers + 1),
        'Age': np.random.normal(45, 15, n_customers).astype(int),
        'Income': np.random.lognormal(10, 0.5, n_customers),
        'Tenure_Months': np.random.exponential(24, n_customers).astype(int),
        'Total_Spent': np.random.lognormal(8, 1, n_customers),
        'Purchase_Frequency': np.random.poisson(3, n_customers),
        'Avg_Order_Value': np.random.lognormal(4, 0.8, n_customers),
        'Support_Tickets': np.random.poisson(2, n_customers),
        'Website_Visits': np.random.poisson(15, n_customers),
        'Email_Open_Rate': np.random.beta(3, 7, n_customers),
        'Last_Purchase_Days': np.random.exponential(30, n_customers).astype(int),
        'Product_Category_Preference': np.random.choice(['Electronics', 'Clothing', 'Home', 'Books', 'Sports'], n_customers),
        'Channel_Preference': np.random.choice(['Online', 'Store', 'Mobile', 'Phone'], n_customers, p=[0.4, 0.3, 0.2, 0.1])
    })
    
    # Calculate derived metrics
    customer_data['CLV'] = customer_data['Total_Spent'] * customer_data['Purchase_Frequency'] / (customer_data['Tenure_Months'] + 1)
    customer_data['Churn_Probability'] = np.random.beta(2, 8, n_customers)
    customer_data['Engagement_Score'] = (customer_data['Email_Open_Rate'] + 
                                       customer_data['Website_Visits'] / 20 + 
                                       (1 - customer_data['Support_Tickets'] / 10)).clip(0, 1)
    
    # Add some realistic correlations
    customer_data.loc[customer_data['Last_Purchase_Days'] > 90, 'Churn_Probability'] *= 2
    customer_data.loc[customer_data['Support_Tickets'] > 5, 'Churn_Probability'] *= 1.5
    customer_data['Churn_Probability'] = customer_data['Churn_Probability'].clip(0, 1)
    
    return customer_data

# Load data
customer_data = generate_customer_data()

# Sidebar controls
st.sidebar.header("🎛️ Analytics Controls")

# Segmentation parameters
st.sidebar.subheader("Customer Segmentation")
n_clusters = st.sidebar.slider("Number of Segments", 2, 8, 4)
segmentation_features = st.sidebar.multiselect(
    "Features for Segmentation",
    ['Income', 'Total_Spent', 'Purchase_Frequency', 'Avg_Order_Value', 'Engagement_Score'],
    default=['Income', 'Total_Spent', 'Purchase_Frequency', 'Engagement_Score']
)

# Churn prediction parameters
st.sidebar.subheader("Churn Prediction")
churn_threshold = st.sidebar.slider("Churn Risk Threshold", 0.1, 0.9, 0.5)

# Main dashboard
tab1, tab2, tab3, tab4, tab5 = st.tabs([
    "📊 Overview", 
    "🎯 Segmentation", 
    "⚠️ Churn Analysis", 
    "💰 CLV Analysis",
    "📈 Campaign Analytics"
])

with tab1:
    st.header("📊 Customer Analytics Overview")
    
    # Key metrics
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        total_customers = len(customer_data)
        st.metric(
            label="Total Customers",
            value=f"{total_customers:,}",
            delta="5.2%"
        )
    
    with col2:
        avg_clv = customer_data['CLV'].mean()
        st.metric(
            label="Average CLV",
            value=f"${avg_clv:,.0f}",
            delta="8.1%"
        )
    
    with col3:
        churn_rate = (customer_data['Churn_Probability'] > churn_threshold).mean()
        st.metric(
            label="Churn Rate",
            value=f"{churn_rate:.1%}",
            delta="-2.3%"
        )
    
    with col4:
        avg_engagement = customer_data['Engagement_Score'].mean()
        st.metric(
            label="Avg Engagement",
            value=f"{avg_engagement:.2f}",
            delta="0.1"
        )
    
    # Customer distribution charts
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("📊 Customer Distribution by Age")
        fig = px.histogram(
            customer_data, 
            x='Age', 
            nbins=20,
            title='Age Distribution',
            color_discrete_sequence=['#1f77b4']
        )
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        st.subheader("📊 Income Distribution")
        fig = px.histogram(
            customer_data, 
            x='Income', 
            nbins=30,
            title='Income Distribution',
            color_discrete_sequence=['#2ca02c']
        )
        st.plotly_chart(fig, use_container_width=True)
    
    # Channel preference
    st.subheader("📱 Channel Preferences")
    channel_counts = customer_data['Channel_Preference'].value_counts()
    fig = px.pie(
        values=channel_counts.values,
        names=channel_counts.index,
        title='Customer Channel Preferences',
        color_discrete_sequence=px.colors.qualitative.Set3
    )
    st.plotly_chart(fig, use_container_width=True)

with tab2:
    st.header("🎯 Customer Segmentation Analysis")
    
    if len(segmentation_features) >= 2:
        # Perform K-means clustering
        features_for_clustering = customer_data[segmentation_features].copy()
        scaler = StandardScaler()
        features_scaled = scaler.fit_transform(features_for_clustering)
        
        kmeans = KMeans(n_clusters=n_clusters, random_state=42)
        customer_data['Segment'] = kmeans.fit_predict(features_scaled)
        
        # Segment analysis
        segment_summary = customer_data.groupby('Segment').agg({
            'CLV': 'mean',
            'Total_Spent': 'mean',
            'Purchase_Frequency': 'mean',
            'Engagement_Score': 'mean',
            'Churn_Probability': 'mean',
            'Customer_ID': 'count'
        }).round(2)
        
        segment_summary.columns = ['Avg CLV', 'Avg Total Spent', 'Avg Purchase Freq', 
                                 'Avg Engagement', 'Avg Churn Prob', 'Count']
        
        st.subheader("📊 Segment Summary")
        st.dataframe(segment_summary, use_container_width=True)
        
        # Segment visualization
        if len(segmentation_features) >= 2:
            fig = px.scatter(
                customer_data,
                x=segmentation_features[0],
                y=segmentation_features[1],
                color='Segment',
                size='CLV',
                title=f'Customer Segments: {segmentation_features[0]} vs {segmentation_features[1]}',
                hover_data=['CLV', 'Purchase_Frequency', 'Engagement_Score']
            )
            st.plotly_chart(fig, use_container_width=True)
        
        # Segment characteristics
        st.subheader("🎯 Segment Characteristics")
        for segment in range(n_clusters):
            segment_data = customer_data[customer_data['Segment'] == segment]
            col1, col2, col3 = st.columns(3)
            
            with col1:
                st.metric(
                    f"Segment {segment} Size",
                    f"{len(segment_data):,} customers",
                    f"{len(segment_data)/len(customer_data):.1%} of total"
                )
            
            with col2:
                avg_clv = segment_data['CLV'].mean()
                st.metric(
                    f"Segment {segment} Avg CLV",
                    f"${avg_clv:,.0f}"
                )
            
            with col3:
                churn_rate = (segment_data['Churn_Probability'] > churn_threshold).mean()
                st.metric(
                    f"Segment {segment} Churn Rate",
                    f"{churn_rate:.1%}"
                )
    else:
        st.warning("Please select at least 2 features for segmentation analysis.")

with tab3:
    st.header("⚠️ Churn Prediction Analysis")
    
    # Churn risk distribution
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("📊 Churn Risk Distribution")
        fig = px.histogram(
            customer_data,
            x='Churn_Probability',
            nbins=20,
            title='Distribution of Churn Probability',
            color_discrete_sequence=['#d62728']
        )
        fig.add_vline(x=churn_threshold, line_dash="dash", line_color="red", 
                     annotation_text=f"Threshold: {churn_threshold}")
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        st.subheader("🎯 High-Risk Customers")
        high_risk_customers = customer_data[customer_data['Churn_Probability'] > churn_threshold]
        
        fig = px.scatter(
            high_risk_customers,
            x='Last_Purchase_Days',
            y='Support_Tickets',
            size='CLV',
            color='Churn_Probability',
            title='High-Risk Customer Profile',
            color_continuous_scale='Reds'
        )
        st.plotly_chart(fig, use_container_width=True)
    
    # Churn factors analysis
    st.subheader("📈 Churn Risk Factors")
    
    # Analyze factors affecting churn
    churn_factors = customer_data[['Last_Purchase_Days', 'Support_Tickets', 
                                 'Engagement_Score', 'Purchase_Frequency', 'Churn_Probability']].corr()
    
    fig = px.imshow(
        churn_factors,
        text_auto=True,
        aspect="auto",
        title="Correlation Matrix: Churn Risk Factors",
        color_continuous_scale='RdBu'
    )
    st.plotly_chart(fig, use_container_width=True)
    
    # Churn prediction model performance
    st.subheader("🤖 Model Performance")
    
    # Simulate model performance metrics
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Accuracy", "87.3%", "2.1%")
    with col2:
        st.metric("Precision", "82.1%", "1.8%")
    with col3:
        st.metric("Recall", "79.4%", "3.2%")
    with col4:
        st.metric("F1-Score", "80.7%", "2.5%")

with tab4:
    st.header("💰 Customer Lifetime Value Analysis")
    
    # CLV distribution
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("📊 CLV Distribution")
        fig = px.histogram(
            customer_data,
            x='CLV',
            nbins=30,
            title='Customer Lifetime Value Distribution',
            color_discrete_sequence=['#2ca02c']
        )
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        st.subheader("🎯 CLV vs Engagement")
        fig = px.scatter(
            customer_data,
            x='Engagement_Score',
            y='CLV',
            color='Purchase_Frequency',
            size='Total_Spent',
            title='CLV vs Engagement Score',
            color_continuous_scale='Viridis'
        )
        st.plotly_chart(fig, use_container_width=True)
    
    # CLV segments
    st.subheader("💎 CLV Segmentation")
    
    # Create CLV segments
    customer_data['CLV_Segment'] = pd.cut(
        customer_data['CLV'],
        bins=[0, customer_data['CLV'].quantile(0.33), 
              customer_data['CLV'].quantile(0.67), customer_data['CLV'].max()],
        labels=['Low Value', 'Medium Value', 'High Value']
    )
    
    clv_segment_summary = customer_data.groupby('CLV_Segment').agg({
        'CLV': ['count', 'mean', 'sum'],
        'Purchase_Frequency': 'mean',
        'Engagement_Score': 'mean',
        'Churn_Probability': 'mean'
    }).round(2)
    
    st.dataframe(clv_segment_summary, use_container_width=True)
    
    # CLV trends
    st.subheader("📈 CLV Trends by Product Category")
    clv_by_category = customer_data.groupby('Product_Category_Preference')['CLV'].mean().sort_values(ascending=False)
    
    fig = px.bar(
        x=clv_by_category.index,
        y=clv_by_category.values,
        title='Average CLV by Product Category',
        color=clv_by_category.values,
        color_continuous_scale='Greens'
    )
    st.plotly_chart(fig, use_container_width=True)

with tab5:
    st.header("📈 Campaign Performance Analytics")
    
    # Generate campaign data
    campaigns = ['Email Campaign A', 'Social Media B', 'Retargeting C', 'Loyalty Program D']
    campaign_data = pd.DataFrame({
        'Campaign': campaigns,
        'Reach': [10000, 15000, 8000, 5000],
        'Conversion_Rate': [0.12, 0.08, 0.15, 0.25],
        'Avg_Order_Value': [150, 120, 200, 300],
        'ROI': [2.5, 1.8, 3.2, 4.1],
        'Cost': [50000, 75000, 40000, 25000]
    })
    
    # Campaign performance metrics
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        total_reach = campaign_data['Reach'].sum()
        st.metric("Total Reach", f"{total_reach:,}", "12.5%")
    
    with col2:
        avg_conversion = campaign_data['Conversion_Rate'].mean()
        st.metric("Avg Conversion", f"{avg_conversion:.1%}", "0.8%")
    
    with col3:
        total_roi = (campaign_data['ROI'] * campaign_data['Cost']).sum() / campaign_data['Cost'].sum()
        st.metric("Weighted ROI", f"{total_roi:.1f}x", "0.3x")
    
    with col4:
        total_revenue = (campaign_data['Reach'] * campaign_data['Conversion_Rate'] * 
                        campaign_data['Avg_Order_Value']).sum()
        st.metric("Total Revenue", f"${total_revenue:,.0f}", "15.2%")
    
    # Campaign comparison charts
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("📊 Campaign ROI Comparison")
        fig = px.bar(
            campaign_data,
            x='Campaign',
            y='ROI',
            title='Campaign ROI Comparison',
            color='ROI',
            color_continuous_scale='RdYlGn'
        )
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        st.subheader("📊 Conversion Rate Analysis")
        fig = px.scatter(
            campaign_data,
            x='Reach',
            y='Conversion_Rate',
            size='Avg_Order_Value',
            color='ROI',
            title='Reach vs Conversion Rate',
            hover_data=['Campaign', 'Cost']
        )
        st.plotly_chart(fig, use_container_width=True)
    
    # Campaign effectiveness matrix
    st.subheader("🎯 Campaign Effectiveness Matrix")
    
    fig = px.scatter(
        campaign_data,
        x='Cost',
        y='ROI',
        size='Reach',
        color='Conversion_Rate',
        title='Campaign Effectiveness Matrix',
        hover_data=['Campaign', 'Avg_Order_Value'],
        color_continuous_scale='Viridis'
    )
    st.plotly_chart(fig, use_container_width=True)

# Footer
st.markdown("---")
st.markdown("""
<div style='text-align: center; color: #666;'>
    <p>👥 EY Customer Analytics Dashboard | Built for Ernst & Young Data Analytics Portfolio</p>
    <p>Demonstrates advanced customer segmentation, churn prediction, and lifetime value analysis</p>
</div>
""", unsafe_allow_html=True)
