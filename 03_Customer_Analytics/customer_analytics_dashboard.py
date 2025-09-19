"""
Customer Analytics & Segmentation Dashboard
==========================================

A comprehensive customer analytics system demonstrating advanced customer insights,
behavioral analysis, and marketing optimization capabilities.

Key Features:
- Customer Segmentation using ML
- Churn Prediction
- Lifetime Value Analysis
- Marketing Campaign Optimization
- Customer Journey Analysis
- Behavioral Analytics

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
        color: #8B4513;
        text-align: center;
        margin-bottom: 2rem;
        font-weight: bold;
    }
    .metric-card {
        background-color: #fdf5e6;
        padding: 1rem;
        border-radius: 0.5rem;
        border-left: 4px solid #8B4513;
        margin: 0.5rem 0;
    }
    .segment-high { color: #228B22; }
    .segment-medium { color: #FF8C00; }
    .segment-low { color: #DC143C; }
</style>
""", unsafe_allow_html=True)

# Header
st.markdown('<h1 class="main-header">👥 EY Customer Analytics Dashboard</h1>', unsafe_allow_html=True)

# Sidebar Controls
st.sidebar.header("🎛️ Analytics Controls")

# Analysis Parameters
st.sidebar.subheader("Analysis Parameters")
segmentation_method = st.sidebar.selectbox(
    "Segmentation Method",
    ["K-Means", "RFM Analysis", "Behavioral Clustering"],
    help="Method for customer segmentation"
)

churn_threshold = st.sidebar.slider(
    "Churn Probability Threshold",
    min_value=0.1,
    max_value=0.9,
    value=0.5,
    step=0.05,
    help="Threshold for churn prediction"
)

clv_timeframe = st.sidebar.selectbox(
    "CLV Timeframe",
    ["6 months", "12 months", "24 months", "Lifetime"],
    help="Timeframe for customer lifetime value calculation"
)

# Generate sample customer data
@st.cache_data
def generate_customer_data():
    """Generate realistic customer analytics data"""
    np.random.seed(42)
    n_customers = 5000
    
    # Generate customer demographics
    customer_data = pd.DataFrame({
        'Customer_ID': range(1, n_customers + 1),
        'Age': np.random.normal(35, 12, n_customers),
        'Income': np.random.lognormal(10, 0.5, n_customers),
        'Tenure_Months': np.random.exponential(24, n_customers),
        'Total_Spent': np.random.lognormal(8, 1, n_customers),
        'Purchase_Frequency': np.random.poisson(3, n_customers),
        'Avg_Order_Value': np.random.lognormal(4, 0.8, n_customers),
        'Website_Visits': np.random.poisson(15, n_customers),
        'Email_Opens': np.random.binomial(10, 0.3, n_customers),
        'Support_Tickets': np.random.poisson(2, n_customers),
        'Last_Purchase_Days': np.random.exponential(30, n_customers)
    })
    
    # Ensure realistic values
    customer_data['Age'] = np.clip(customer_data['Age'], 18, 80)
    customer_data['Income'] = np.clip(customer_data['Income'], 20000, 200000)
    customer_data['Tenure_Months'] = np.clip(customer_data['Tenure_Months'], 1, 120)
    customer_data['Avg_Order_Value'] = np.clip(customer_data['Avg_Order_Value'], 10, 1000)
    
    # Generate behavioral features
    customer_data['Engagement_Score'] = (
        customer_data['Website_Visits'] * 0.3 +
        customer_data['Email_Opens'] * 0.4 +
        (1 / (customer_data['Support_Tickets'] + 1)) * 0.3
    )
    
    customer_data['Recency_Score'] = np.exp(-customer_data['Last_Purchase_Days'] / 30)
    customer_data['Frequency_Score'] = customer_data['Purchase_Frequency'] / customer_data['Purchase_Frequency'].max()
    customer_data['Monetary_Score'] = customer_data['Total_Spent'] / customer_data['Total_Spent'].max()
    
    # Generate RFM scores
    customer_data['RFM_Score'] = (
        customer_data['Recency_Score'] * 0.3 +
        customer_data['Frequency_Score'] * 0.3 +
        customer_data['Monetary_Score'] * 0.4
    )
    
    # Generate churn probability
    customer_data['Churn_Probability'] = (
        1 / (1 + np.exp(-(
            -2 + 
            customer_data['Last_Purchase_Days'] * 0.01 +
            customer_data['Support_Tickets'] * 0.2 -
            customer_data['Engagement_Score'] * 0.5 +
            np.random.normal(0, 0.3, n_customers)
        )))
    )
    
    # Generate customer lifetime value
    customer_data['CLV'] = (
        customer_data['Avg_Order_Value'] * customer_data['Purchase_Frequency'] * (12 / (customer_data['Churn_Probability'] + 0.1)) *
        np.random.uniform(0.8, 1.2, n_customers)
    )
    
    # Generate campaign data
    campaigns = ['Email Campaign A', 'Social Media B', 'Retargeting C', 'Loyalty Program D']
    campaign_data = []
    
    for campaign in campaigns:
        campaign_customers = np.random.choice(n_customers, size=int(n_customers * 0.3), replace=False)
        campaign_df = pd.DataFrame({
            'Customer_ID': campaign_customers,
            'Campaign': campaign,
            'Response_Rate': np.random.beta(2, 8, len(campaign_customers)),
            'Conversion_Rate': np.random.beta(1, 9, len(campaign_customers)),
            'Revenue_Generated': np.random.lognormal(6, 1, len(campaign_customers))
        })
        campaign_data.append(campaign_df)
    
    campaign_df = pd.concat(campaign_data, ignore_index=True)
    
    return customer_data, campaign_df

# Load data
customer_data, campaign_data = generate_customer_data()

# Main dashboard
tab1, tab2, tab3, tab4, tab5 = st.tabs([
    "📊 Customer Overview", 
    "🎯 Segmentation", 
    "⚠️ Churn Analysis",
    "💰 Lifetime Value",
    "📢 Campaign Analytics"
])

with tab1:
    st.header("👥 Customer Overview Dashboard")
    
    # Key Customer Metrics
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        total_customers = len(customer_data)
        st.metric(
            label="Total Customers",
            value=f"{total_customers:,}",
            delta="8.2%"
        )
    
    with col2:
        avg_clv = customer_data['CLV'].mean()
        st.metric(
            label="Average CLV",
            value=f"${avg_clv:,.0f}",
            delta="12.5%"
        )
    
    with col3:
        churn_rate = (customer_data['Churn_Probability'] > 0.5).mean()
        st.metric(
            label="Churn Rate",
            value=f"{churn_rate:.1%}",
            delta="-2.1%"
        )
    
    with col4:
        avg_engagement = customer_data['Engagement_Score'].mean()
        st.metric(
            label="Avg Engagement",
            value=f"{avg_engagement:.2f}",
            delta="0.15"
        )
    
    # Customer Distribution Analysis
    st.subheader("📊 Customer Distribution Analysis")
    
    col1, col2 = st.columns(2)
    
    with col1:
        # Age Distribution
        fig = px.histogram(
            customer_data,
            x='Age',
            nbins=20,
            title='Customer Age Distribution',
            color_discrete_sequence=['#8B4513']
        )
        fig.update_layout(height=300)
        st.plotly_chart(fig, width='stretch')
    
    with col2:
        # Income Distribution
        fig = px.histogram(
            customer_data,
            x='Income',
            nbins=20,
            title='Customer Income Distribution',
            color_discrete_sequence=['#8B4513']
        )
        fig.update_layout(height=300)
        st.plotly_chart(fig, width='stretch')
    
    # RFM Analysis Overview
    st.subheader("📈 RFM Analysis Overview")
    
    # Create RFM segments
    customer_data['RFM_Segment'] = pd.cut(
        customer_data['RFM_Score'],
        bins=[0, 0.3, 0.6, 1.0],
        labels=['Low Value', 'Medium Value', 'High Value']
    )
    
    rfm_summary = customer_data.groupby('RFM_Segment').agg({
        'Customer_ID': 'count',
        'CLV': 'mean',
        'Churn_Probability': 'mean',
        'Total_Spent': 'mean'
    }).round(2)
    
    st.dataframe(rfm_summary, width='stretch')

with tab2:
    st.header("🎯 Customer Segmentation")
    
    # Perform K-Means clustering
    @st.cache_data
    def perform_segmentation():
        """Perform customer segmentation using K-Means"""
        # Select features for clustering
        features = ['Age', 'Income', 'Total_Spent', 'Purchase_Frequency', 
                    'Engagement_Score', 'RFM_Score']
        
        # Prepare data
        X = customer_data[features].fillna(0)
        
        # Standardize features
        scaler = StandardScaler()
        X_scaled = scaler.fit_transform(X)
        
        # Perform K-Means clustering
        kmeans = KMeans(n_clusters=4, random_state=42, n_init=10)
        customer_data['Cluster'] = kmeans.fit_predict(X_scaled)
        
        # Create cluster names
        cluster_names = ['Budget Conscious', 'High Value', 'Occasional Buyers', 'Loyal Customers']
        customer_data['Segment'] = customer_data['Cluster'].map(dict(enumerate(cluster_names)))
        
        return customer_data
    
    segmented_data = perform_segmentation()
    
    # Segmentation Results
    st.subheader("📊 Segmentation Results")
    
    # Segment Distribution
    segment_counts = segmented_data['Segment'].value_counts()
    
    fig = px.pie(
        values=segment_counts.values,
        names=segment_counts.index,
        title='Customer Segment Distribution',
        color_discrete_sequence=px.colors.qualitative.Set3
    )
    fig.update_layout(height=400)
    st.plotly_chart(fig, width='stretch')
    
    # Segment Characteristics
    st.subheader("📈 Segment Characteristics")
    
    segment_analysis = segmented_data.groupby('Segment').agg({
        'Age': 'mean',
        'Income': 'mean',
        'Total_Spent': 'mean',
        'Purchase_Frequency': 'mean',
        'CLV': 'mean',
        'Churn_Probability': 'mean',
        'Customer_ID': 'count'
    }).round(2)
    
    st.dataframe(segment_analysis, width='stretch')
    
    # Segment Comparison Chart
    st.subheader("📊 Segment Comparison")
    
    # Select metrics for comparison
    comparison_metrics = ['Age', 'Income', 'Total_Spent', 'CLV']
    
    fig = go.Figure()
    
    for segment in segmented_data['Segment'].unique():
        segment_data = segmented_data[segmented_data['Segment'] == segment]
        fig.add_trace(go.Scatter(
            x=comparison_metrics,
            y=[segment_data[metric].mean() for metric in comparison_metrics],
            mode='lines+markers',
            name=segment,
            line=dict(width=3)
        ))
    
    fig.update_layout(
        title='Segment Comparison Across Key Metrics',
        xaxis_title='Metrics',
        yaxis_title='Average Value',
        height=400
    )
    st.plotly_chart(fig, width='stretch')
    
    # Detailed Segment Analysis
    st.subheader("🔍 Detailed Segment Analysis")
    
    selected_segment = st.selectbox(
        "Select Segment for Detailed Analysis",
        segmented_data['Segment'].unique()
    )
    
    segment_data = segmented_data[segmented_data['Segment'] == selected_segment]
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.metric(
            label="Segment Size",
            value=f"{len(segment_data):,} customers",
            delta=f"{len(segment_data)/len(segmented_data):.1%} of total"
        )
    
    with col2:
        st.metric(
            label="Average CLV",
            value=f"${segment_data['CLV'].mean():,.0f}",
            delta=f"{segment_data['CLV'].mean()/segmented_data['CLV'].mean():.1%} of average"
        )

with tab3:
    st.header("⚠️ Churn Analysis")
    
    # Churn Prediction Model
    @st.cache_data
    def build_churn_model():
        """Build churn prediction model"""
        # Prepare features
        features = ['Age', 'Income', 'Tenure_Months', 'Total_Spent', 
                    'Purchase_Frequency', 'Engagement_Score', 'Support_Tickets',
                    'Last_Purchase_Days', 'RFM_Score']
        
        X = customer_data[features]
        y = (customer_data['Churn_Probability'] > churn_threshold).astype(int)
        
        # FIX: Check if both classes exist in the target variable
        if len(np.unique(y)) < 2:
            st.error("Error: The generated data for the selected churn threshold contains only one class. Please adjust the threshold or the data generation logic to include both churning and non-churning customers.")
            return None, None, None, None, None
        
        # Split data with stratification to maintain class balance
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42, stratify=y)
        
        # Train model
        model = RandomForestClassifier(n_estimators=100, random_state=42)
        model.fit(X_train, y_train)
        
        # Predictions
        y_pred = model.predict(X_test)
        
        # FIX: Check the shape of predict_proba before slicing
        y_proba_raw = model.predict_proba(X_test)
        if y_proba_raw.shape[1] > 1:
            y_proba = y_proba_raw[:, 1]
        else:
            y_proba = np.zeros(y_proba_raw.shape[0]) # Default to 0 if only one class is predicted
            st.warning("Warning: Model predicted only one class. Probability values are not reliable.")
        
        return model, X_test, y_test, y_pred, y_proba
    
    model, X_test, y_test, y_pred, y_proba = build_churn_model()
    
    if model is not None:
        # Churn Metrics
        col1, col2, col3 = st.columns(3)
        
        with col1:
            churn_rate = y_test.mean()
            st.metric(
                label="Actual Churn Rate",
                value=f"{churn_rate:.1%}",
                delta="Test Set"
            )
        
        with col2:
            predicted_churn_rate = y_pred.mean()
            st.metric(
                label="Predicted Churn Rate",
                value=f"{predicted_churn_rate:.1%}",
                delta="Model Output"
            )
        
        with col3:
            accuracy = (y_pred == y_test).mean()
            st.metric(
                label="Model Accuracy",
                value=f"{accuracy:.1%}",
                delta="Performance"
            )
        
        # Churn Distribution
        st.subheader("📊 Churn Probability Distribution")
        
        fig = px.histogram(
            customer_data,
            x='Churn_Probability',
            nbins=30,
            title='Distribution of Churn Probabilities',
            color_discrete_sequence=['#DC143C']
        )
        fig.add_vline(x=churn_threshold, line_dash="dash", line_color="red", 
                      annotation_text=f"Threshold: {churn_threshold}")
        fig.update_layout(height=400)
        st.plotly_chart(fig, width='stretch')
        
        # Feature Importance
        st.subheader("🎯 Feature Importance for Churn Prediction")
        
        feature_importance = pd.DataFrame({
            'Feature': X_test.columns,
            'Importance': model.feature_importances_
        }).sort_values('Importance', ascending=True)
        
        fig = px.bar(
            feature_importance,
            x='Importance',
            y='Feature',
            orientation='h',
            title='Feature Importance for Churn Prediction',
            color='Importance',
            color_continuous_scale='Reds'
        )
        fig.update_layout(height=400)
        st.plotly_chart(fig, width='stretch')
        
        # High-Risk Customers
        st.subheader("🚨 High-Risk Customers")
        
        high_risk_customers = customer_data[customer_data['Churn_Probability'] > churn_threshold]
        
        st.write(f"**{len(high_risk_customers)} customers** are at high risk of churning")
        
        # Show top 10 high-risk customers
        top_risk = high_risk_customers.nlargest(10, 'Churn_Probability')[
            ['Customer_ID', 'Churn_Probability', 'CLV', 'Total_Spent', 'Last_Purchase_Days']
        ]
        
        st.dataframe(top_risk, width='stretch')

with tab4:
    st.header("💰 Customer Lifetime Value Analysis")
    
    # CLV Overview
    st.subheader("📊 CLV Overview")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        avg_clv = customer_data['CLV'].mean()
        st.metric(
            label="Average CLV",
            value=f"${avg_clv:,.0f}",
            delta="12.5%"
        )
    
    with col2:
        median_clv = customer_data['CLV'].median()
        st.metric(
            label="Median CLV",
            value=f"${median_clv:,.0f}",
            delta="8.3%"
        )
    
    with col3:
        total_clv = customer_data['CLV'].sum()
        st.metric(
            label="Total CLV",
            value=f"${total_clv:,.0f}",
            delta="15.2%"
        )
    
    # CLV Distribution
    st.subheader("📈 CLV Distribution Analysis")
    
    fig = px.histogram(
        customer_data,
        x='CLV',
        nbins=30,
        title='Customer Lifetime Value Distribution',
        color_discrete_sequence=['#8B4513']
    )
    fig.update_layout(height=400)
    st.plotly_chart(fig, width='stretch')
    
    # CLV vs Other Metrics
    st.subheader("📊 CLV Correlation Analysis")
    
    col1, col2 = st.columns(2)
    
    with col1:
        # CLV vs Total Spent
        fig = px.scatter(
            customer_data,
            x='Total_Spent',
            y='CLV',
            color='Churn_Probability',
            title='CLV vs Total Spent',
            color_continuous_scale='RdYlGn_r'
        )
        fig.update_layout(height=300)
        st.plotly_chart(fig, width='stretch')
    
    with col2:
        # CLV vs Engagement
        fig = px.scatter(
            customer_data,
            x='Engagement_Score',
            y='CLV',
            color='Purchase_Frequency',
            title='CLV vs Engagement Score',
            color_continuous_scale='Blues'
        )
        fig.update_layout(height=300)
        st.plotly_chart(fig, width='stretch')
    
    # CLV Segments
    st.subheader("🎯 CLV Segments")
    
    # Create CLV segments
    customer_data['CLV_Segment'] = pd.cut(
        customer_data['CLV'],
        bins=[0, customer_data['CLV'].quantile(0.25), 
              customer_data['CLV'].quantile(0.75), customer_data['CLV'].max()],
        labels=['Low CLV', 'Medium CLV', 'High CLV']
    )
    
    clv_segment_analysis = customer_data.groupby('CLV_Segment').agg({
        'Customer_ID': 'count',
        'CLV': 'mean',
        'Total_Spent': 'mean',
        'Purchase_Frequency': 'mean',
        'Churn_Probability': 'mean'
    }).round(2)
    
    st.dataframe(clv_segment_analysis, width='stretch')

with tab5:
    st.header("📢 Campaign Analytics")
    
    # Campaign Performance Overview
    st.subheader("📊 Campaign Performance Overview")
    
    campaign_summary = campaign_data.groupby('Campaign').agg({
        'Customer_ID': 'count',
        'Response_Rate': 'mean',
        'Conversion_Rate': 'mean',
        'Revenue_Generated': 'sum'
    }).round(3)
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        total_campaigns = len(campaign_summary)
        st.metric(
            label="Active Campaigns",
            value=f"{total_campaigns}",
            delta="2 new"
        )
    
    with col2:
        avg_response_rate = campaign_summary['Response_Rate'].mean()
        st.metric(
            label="Avg Response Rate",
            value=f"{avg_response_rate:.1%}",
            delta="3.2%"
        )
    
    with col3:
        avg_conversion_rate = campaign_summary['Conversion_Rate'].mean()
        st.metric(
            label="Avg Conversion Rate",
            value=f"{avg_conversion_rate:.1%}",
            delta="1.8%"
        )
    
    with col4:
        total_revenue = campaign_summary['Revenue_Generated'].sum()
        st.metric(
            label="Total Revenue",
            value=f"${total_revenue:,.0f}",
            delta="15.7%"
        )
    
    # Campaign Performance Chart
    st.subheader("📈 Campaign Performance Comparison")
    
    fig = px.bar(
        campaign_summary.reset_index(),
        x='Campaign',
        y='Revenue_Generated',
        color='Response_Rate',
        title='Campaign Revenue vs Response Rate',
        color_continuous_scale='Greens'
    )
    fig.update_layout(height=400)
    st.plotly_chart(fig, width='stretch')
    
    # Campaign ROI Analysis
    st.subheader("💰 Campaign ROI Analysis")
    
    # Calculate ROI (simplified)
    campaign_summary['ROI'] = campaign_summary['Revenue_Generated'] / 10000  # Assuming $10k cost per campaign
    
    fig = px.scatter(
        campaign_summary.reset_index(),
        x='Conversion_Rate',
        y='ROI',
        size='Revenue_Generated',
        color='Campaign',
        title='Campaign ROI vs Conversion Rate',
        hover_data=['Response_Rate']
    )
    fig.update_layout(height=400)
    st.plotly_chart(fig, width='stretch')
    
    # Campaign Effectiveness by Segment
    st.subheader("🎯 Campaign Effectiveness by Customer Segment")
    
    # Merge campaign data with customer segments
    campaign_segment_data = campaign_data.merge(
        customer_data[['Customer_ID', 'Segment']], 
        on='Customer_ID', 
        how='left'
    )
    
    segment_campaign_performance = campaign_segment_data.groupby(['Campaign', 'Segment']).agg({
        'Response_Rate': 'mean',
        'Conversion_Rate': 'mean',
        'Revenue_Generated': 'sum'
    }).round(3)
    
    fig = px.bar(
        segment_campaign_performance.reset_index(),
        x='Campaign',
        y='Response_Rate',
        color='Segment',
        title='Response Rate by Campaign and Segment',
        barmode='group'
    )
    fig.update_layout(height=400)
    st.plotly_chart(fig, width='stretch')

# Footer
st.markdown("---")
st.markdown("""
<div style='text-align: center; color: #666;'>
    <p>👥 EY Customer Analytics Dashboard | Built for Ernst & Young Data Analytics Portfolio</p>
    <p>Demonstrates advanced customer insights, behavioral analysis, and marketing optimization capabilities</p>
</div>
""", unsafe_allow_html=True)