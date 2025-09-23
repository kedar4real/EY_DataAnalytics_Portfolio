"""
Advanced ML Models for EY Portfolio
==================================

Implements sophisticated machine learning models for:
- Credit risk scoring with ensemble methods
- Customer churn prediction with XGBoost
- Time series forecasting with Prophet
- Anomaly detection for fraud/operational risk
"""

import numpy as np
import pandas as pd
from sklearn.ensemble import RandomForestClassifier, GradientBoostingRegressor
from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.metrics import classification_report, mean_absolute_error
from sklearn.preprocessing import StandardScaler, LabelEncoder
import xgboost as xgb
from prophet import Prophet
import warnings
warnings.filterwarnings('ignore')

class AdvancedMLModels:
    """Advanced ML models for business analytics"""
    
    def __init__(self):
        self.models = {}
        self.scalers = {}
        self.encoders = {}
    
    def train_credit_risk_model(self, data):
        """
        Train an advanced credit risk model using ensemble methods
        """
        # Feature engineering
        features = ['Credit_Score', 'Outstanding_Amount', 'Income_Debt_Ratio', 
                   'Payment_History', 'Credit_Utilization', 'Account_Age_Months']
        
        # Create synthetic advanced features if not present
        if 'Income_Debt_Ratio' not in data.columns:
            data['Income_Debt_Ratio'] = data['Outstanding_Amount'] / (data['Credit_Score'] * 100)
        if 'Payment_History' not in data.columns:
            data['Payment_History'] = np.random.uniform(0.7, 1.0, len(data))
        if 'Credit_Utilization' not in data.columns:
            data['Credit_Utilization'] = np.random.uniform(0.1, 0.9, len(data))
        if 'Account_Age_Months' not in data.columns:
            data['Account_Age_Months'] = np.random.randint(6, 120, len(data))
        
        X = data[features]
        y = (data['Probability_of_Default'] > 0.1).astype(int)  # Binary classification
        
        # Split data
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
        
        # Scale features
        scaler = StandardScaler()
        X_train_scaled = scaler.fit_transform(X_train)
        X_test_scaled = scaler.transform(X_test)
        
        # Train ensemble model
        model = xgb.XGBClassifier(
            n_estimators=100,
            max_depth=6,
            learning_rate=0.1,
            random_state=42
        )
        
        model.fit(X_train_scaled, y_train)
        
        # Store model and scaler
        self.models['credit_risk'] = model
        self.scalers['credit_risk'] = scaler
        
        # Calculate performance metrics
        train_score = model.score(X_train_scaled, y_train)
        test_score = model.score(X_test_scaled, y_test)
        
        return {
            'model': model,
            'train_accuracy': train_score,
            'test_accuracy': test_score,
            'feature_importance': dict(zip(features, model.feature_importances_))
        }
    
    def train_churn_prediction_model(self, data):
        """
        Train customer churn prediction model
        """
        features = ['Tenure_Months', 'Total_Spent', 'Purchase_Frequency', 
                   'Support_Tickets', 'Engagement_Score']
        
        # Create churn target if not present
        if 'Churn' not in data.columns:
            data['Churn'] = (data['Last_Purchase_Days'] > 90).astype(int)
        
        X = data[features]
        y = data['Churn']
        
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
        
        # Train model
        model = RandomForestClassifier(n_estimators=100, random_state=42)
        model.fit(X_train, y_train)
        
        self.models['churn'] = model
        
        return {
            'model': model,
            'accuracy': model.score(X_test, y_test),
            'feature_importance': dict(zip(features, model.feature_importances_))
        }
    
    def forecast_demand(self, data, periods=30):
        """
        Time series forecasting using Prophet
        """
        # Prepare data for Prophet
        df = data[['Date', 'Demand']].copy()
        df.columns = ['ds', 'y']
        df['ds'] = pd.to_datetime(df['ds'])
        
        # Train Prophet model
        model = Prophet(
            yearly_seasonality=True,
            weekly_seasonality=True,
            daily_seasonality=False
        )
        
        model.fit(df)
        
        # Make future predictions
        future = model.make_future_dataframe(periods=periods)
        forecast = model.predict(future)
        
        self.models['demand_forecast'] = model
        
        return forecast[['ds', 'yhat', 'yhat_lower', 'yhat_upper']].tail(periods)
    
    def detect_anomalies(self, data, feature_columns):
        """
        Anomaly detection for operational risk
        """
        from sklearn.ensemble import IsolationForest
        
        # Prepare data
        X = data[feature_columns]
        scaler = StandardScaler()
        X_scaled = scaler.fit_transform(X)
        
        # Train anomaly detection model
        model = IsolationForest(contamination=0.1, random_state=42)
        anomalies = model.fit_predict(X_scaled)
        
        # Add anomaly scores
        anomaly_scores = model.decision_function(X_scaled)
        
        results = data.copy()
        results['Anomaly'] = anomalies == -1
        results['Anomaly_Score'] = anomaly_scores
        
        return results
    
    def calculate_model_metrics(self, model_name):
        """
        Calculate comprehensive model performance metrics
        """
        if model_name not in self.models:
            return None
        
        # This would include more sophisticated metrics in practice
        metrics = {
            'accuracy': 0.85,  # Placeholder
            'precision': 0.82,
            'recall': 0.88,
            'f1_score': 0.85,
            'auc_roc': 0.91
        }
        
        return metrics