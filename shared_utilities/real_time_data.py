"""
Real-Time Data Integration Module
===============================

Connects to live data sources for more realistic analytics demonstrations.
Includes APIs for financial data, market feeds, and business metrics.
"""

import yfinance as yf
import requests
import pandas as pd
from datetime import datetime, timedelta
import streamlit as st

class RealTimeDataConnector:
    """Handles real-time data connections"""
    
    def __init__(self):
        self.cache_duration = 300  # 5 minutes
    
    @st.cache_data(ttl=300)
    def get_market_data(self, symbols=['AAPL', 'GOOGL', 'MSFT', 'AMZN']):
        """Fetch real market data from Yahoo Finance"""
        try:
            data = {}
            for symbol in symbols:
                ticker = yf.Ticker(symbol)
                hist = ticker.history(period="1mo")
                info = ticker.info
                
                data[symbol] = {
                    'current_price': info.get('currentPrice', 0),
                    'change_percent': info.get('regularMarketChangePercent', 0),
                    'volume': info.get('volume', 0),
                    'market_cap': info.get('marketCap', 0),
                    'historical_data': hist
                }
            return data
        except Exception as e:
            st.warning(f"Could not fetch real market data: {e}")
            return None
    
    @st.cache_data(ttl=300)
    def get_economic_indicators(self):
        """Fetch economic indicators from public APIs"""
        try:
            # Example: FRED API for economic data
            indicators = {
                'gdp_growth': 2.1,  # Placeholder - replace with real API
                'unemployment_rate': 3.7,
                'inflation_rate': 3.2,
                'interest_rate': 5.25
            }
            return indicators
        except Exception as e:
            st.warning(f"Could not fetch economic data: {e}")
            return None
    
    @st.cache_data(ttl=600)
    def get_crypto_data(self):
        """Fetch cryptocurrency data"""
        try:
            url = "https://api.coingecko.com/api/v3/simple/price"
            params = {
                'ids': 'bitcoin,ethereum,cardano',
                'vs_currencies': 'usd',
                'include_24hr_change': 'true'
            }
            response = requests.get(url, params=params)
            return response.json() if response.status_code == 200 else None
        except Exception as e:
            st.warning(f"Could not fetch crypto data: {e}")
            return None