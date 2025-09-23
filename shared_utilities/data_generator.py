"""
Shared Data Generation Utilities
===============================

Common data generation functions used across all EY Data Analytics projects.
Provides realistic, consistent data for demonstrations and testing.

Author: Data Analytics Portfolio for EY
"""

import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import random

class DataGenerator:
    """Utility class for generating realistic business data"""
    
    def __init__(self, seed=42):
        """Initialize with random seed for reproducibility"""
        np.random.seed(seed)
        random.seed(seed)
    
    def generate_time_series(self, start_date, end_date, freq='D', 
                           base_value=100, trend=0.01, seasonality=0.1, noise=0.05):
        """
        Generate realistic time series data
        
        Args:
            start_date: Start date for the series
            end_date: End date for the series
            freq: Frequency ('D' for daily, 'W' for weekly, 'M' for monthly)
            base_value: Base value for the series
            trend: Linear trend coefficient
            seasonality: Seasonal variation amplitude
            noise: Random noise level
        
        Returns:
            pandas.DataFrame with Date and Value columns
        """
        dates = pd.date_range(start=start_date, end=end_date, freq=freq)
        n_periods = len(dates)
        
        # Generate trend
        trend_values = np.arange(n_periods) * trend
        
        # Generate seasonality (annual cycle)
        seasonal_period = 365 if freq == 'D' else 52 if freq == 'W' else 12
        seasonal_values = seasonality * np.sin(2 * np.pi * np.arange(n_periods) / seasonal_period)
        
        # Generate noise
        noise_values = np.random.normal(0, noise, n_periods)
        
        # Combine components
        values = base_value * (1 + trend_values + seasonal_values + noise_values)
        values = np.maximum(values, 0)  # Ensure non-negative values
        
        return pd.DataFrame({
            'Date': dates,
            'Value': values
        })
    
    def generate_customer_data(self, n_customers=1000):
        """
        Generate realistic customer data
        
        Args:
            n_customers: Number of customers to generate
        
        Returns:
            pandas.DataFrame with customer information
        """
        customers = []
        
        for i in range(n_customers):
            customer = {
                'Customer_ID': i + 1,
                'Age': np.random.normal(35, 12),
                'Income': np.random.lognormal(10, 0.5),
                'Tenure_Months': np.random.exponential(24),
                'Total_Spent': np.random.lognormal(8, 1),
                'Purchase_Frequency': np.random.poisson(3),
                'Last_Purchase_Days': np.random.exponential(30),
                'Engagement_Score': np.random.uniform(0, 1),
                'Churn_Probability': np.random.beta(2, 8)
            }
            
            # Ensure realistic values
            customer['Age'] = max(18, min(80, customer['Age']))
            customer['Income'] = max(20000, min(200000, customer['Income']))
            customer['Tenure_Months'] = max(1, customer['Tenure_Months'])
            
            customers.append(customer)
        
        return pd.DataFrame(customers)
    
    def generate_financial_data(self, n_periods=365):
        """
        Generate realistic financial data
        
        Args:
            n_periods: Number of periods to generate
        
        Returns:
            pandas.DataFrame with financial metrics
        """
        dates = pd.date_range(start='2023-01-01', periods=n_periods, freq='D')
        
        # Generate correlated financial metrics
        base_returns = np.random.normal(0.0005, 0.02, n_periods)
        
        financial_data = pd.DataFrame({
            'Date': dates,
            'Portfolio_Value': np.cumsum(np.random.normal(0, 1000000, n_periods)) + 1000000000,
            'Returns': base_returns,
            'Volatility': np.random.normal(0.15, 0.02, n_periods),
            'VaR_95': np.random.normal(5000000, 500000, n_periods),
            'VaR_99': np.random.normal(8000000, 800000, n_periods),
            'Sharpe_Ratio': np.random.normal(1.2, 0.3, n_periods)
        })
        
        return financial_data
    
    def generate_supply_chain_data(self, n_products=10, n_periods=52):
        """
        Generate realistic supply chain data
        
        Args:
            n_products: Number of products
            n_periods: Number of periods (weeks)
        
        Returns:
            pandas.DataFrame with supply chain metrics
        """
        products = [f'Product_{chr(65+i)}' for i in range(n_products)]
        dates = pd.date_range(start='2023-01-01', periods=n_periods, freq='W')
        
        supply_chain_data = []
        
        for product in products:
            base_demand = np.random.uniform(100, 1000)
            trend = np.random.uniform(-0.02, 0.02)
            seasonality = np.sin(np.arange(n_periods) * 2 * np.pi / 52) * 0.3
            noise = np.random.normal(0, 0.1, n_periods)
            
            demand = base_demand * (1 + trend * np.arange(n_periods)) * (1 + seasonality + noise)
            demand = np.maximum(demand, 0)
            
            product_data = pd.DataFrame({
                'Date': dates,
                'Product': product,
                'Demand': demand,
                'Inventory': np.random.uniform(50, 500, n_periods),
                'Lead_Time': np.random.uniform(7, 21, n_periods),
                'Cost': np.random.uniform(10, 100, n_periods)
            })
            
            supply_chain_data.append(product_data)
        
        return pd.concat(supply_chain_data, ignore_index=True)
    
    def generate_esg_data(self, n_periods=12):
        """
        Generate realistic ESG data
        
        Args:
            n_periods: Number of periods (months)
        
        Returns:
            pandas.DataFrame with ESG metrics
        """
        dates = pd.date_range(start='2023-01-01', periods=n_periods, freq='M')
        
        esg_data = pd.DataFrame({
            'Date': dates,
            'Carbon_Emissions': np.random.normal(5000, 500, n_periods),
            'Energy_Consumption': np.random.normal(15000, 1500, n_periods),
            'Water_Usage': np.random.normal(100000, 10000, n_periods),
            'Waste_Generated': np.random.normal(200, 20, n_periods),
            'Renewable_Energy_Pct': np.random.uniform(25, 45, n_periods),
            'Employee_Satisfaction': np.random.normal(4.2, 0.1, n_periods),
            'Diversity_Index': np.random.normal(0.75, 0.02, n_periods),
            'Safety_Score': np.random.normal(8.5, 0.5, n_periods),
            'Compliance_Rate': np.random.uniform(0.95, 1.0, n_periods)
        })
        
        return esg_data
    
    def add_correlation(self, df, target_col, source_cols, correlation_strength=0.7):
        """
        Add correlation between columns
        
        Args:
            df: DataFrame to modify
            target_col: Column to add correlation to
            source_cols: Columns to correlate with
            correlation_strength: Strength of correlation (0-1)
        
        Returns:
            Modified DataFrame
        """
        df_copy = df.copy()
        
        for source_col in source_cols:
            if source_col in df_copy.columns:
                correlation = correlation_strength * np.random.normal(0, 1, len(df_copy))
                df_copy[target_col] += correlation * df_copy[source_col] / df_copy[source_col].std()
        
        return df_copy
    
    def add_outliers(self, df, column, outlier_rate=0.05, outlier_multiplier=3):
        """
        Add outliers to a column
        
        Args:
            df: DataFrame to modify
            column: Column to add outliers to
            outlier_rate: Percentage of values to make outliers
            outlier_multiplier: How extreme outliers should be
        
        Returns:
            Modified DataFrame
        """
        df_copy = df.copy()
        n_outliers = int(len(df_copy) * outlier_rate)
        outlier_indices = np.random.choice(len(df_copy), n_outliers, replace=False)
        
        for idx in outlier_indices:
            if np.random.random() > 0.5:
                df_copy.loc[idx, column] *= outlier_multiplier
            else:
                df_copy.loc[idx, column] /= outlier_multiplier
        
        return df_copy

# Example usage
if __name__ == "__main__":
    generator = DataGenerator()
    
    # Generate sample data
    time_series = generator.generate_time_series('2023-01-01', '2024-01-01')
    customers = generator.generate_customer_data(100)
    financial = generator.generate_financial_data(365)
    
    print("Sample data generated successfully!")
    print(f"Time series: {len(time_series)} records")
    print(f"Customers: {len(customers)} records")
    print(f"Financial: {len(financial)} records")
