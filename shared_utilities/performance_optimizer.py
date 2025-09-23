"""
Performance Optimization Utilities
=================================

Implements caching, lazy loading, and performance monitoring
for better dashboard responsiveness and user experience.
"""

import streamlit as st
import pandas as pd
import time
import hashlib
import pickle
import os
from functools import wraps
import psutil
import matplotlib.pyplot as plt
import plotly.graph_objects as go

class PerformanceOptimizer:
    """Handles performance optimization for dashboards"""
    
    def __init__(self, cache_dir="cache"):
        self.cache_dir = cache_dir
        os.makedirs(cache_dir, exist_ok=True)
        
    def smart_cache(self, ttl=3600):
        """Intelligent caching decorator with TTL"""
        def decorator(func):
            @wraps(func)
            def wrapper(*args, **kwargs):
                # Create cache key from function name and arguments
                cache_key = hashlib.md5(
                    f"{func.__name__}_{str(args)}_{str(kwargs)}".encode()
                ).hexdigest()
                
                cache_file = os.path.join(self.cache_dir, f"{cache_key}.pkl")
                
                # Check if cache exists and is valid
                if os.path.exists(cache_file):
                    cache_age = time.time() - os.path.getmtime(cache_file)
                    if cache_age < ttl:
                        with open(cache_file, 'rb') as f:
                            return pickle.load(f)
                
                # Execute function and cache result
                result = func(*args, **kwargs)
                with open(cache_file, 'wb') as f:
                    pickle.dump(result, f)
                
                return result
            return wrapper
        return decorator
    
    def lazy_load_data(self, data_loader_func, placeholder_text="Loading data..."):
        """Lazy loading with progress indication"""
        if 'data_loaded' not in st.session_state:
            st.session_state.data_loaded = False
            st.session_state.cached_data = None
        
        if not st.session_state.data_loaded:
            with st.spinner(placeholder_text):
                data = data_loader_func()
                st.session_state.cached_data = data
                st.session_state.data_loaded = True
        
        return st.session_state.cached_data
    
    def monitor_performance(self):
        """Monitor and display performance metrics"""
        cpu_percent = psutil.cpu_percent()
        memory_info = psutil.virtual_memory()
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.metric("CPU Usage", f"{cpu_percent:.1f}%")
        
        with col2:
            st.metric("Memory Usage", f"{memory_info.percent:.1f}%")
        
        with col3:
            st.metric("Available Memory", f"{memory_info.available / (1024**3):.1f} GB")
    
    def optimize_dataframe(self, df):
        """Optimize DataFrame for better performance"""
        # Convert object columns to category where appropriate
        for col in df.select_dtypes(include=['object']).columns:
            if df[col].nunique() / len(df) < 0.5:  # Less than 50% unique values
                df[col] = df[col].astype('category')
        
        # Downcast numeric types
        for col in df.select_dtypes(include=['int64']).columns:
            df[col] = pd.to_numeric(df[col], downcast='integer')
        
        for col in df.select_dtypes(include=['float64']).columns:
            df[col] = pd.to_numeric(df[col], downcast='float')
        
        return df
    
    def batch_process_data(self, data, batch_size=1000, process_func=None):
        """Process large datasets in batches"""
        results = []
        total_batches = len(data) // batch_size + (1 if len(data) % batch_size else 0)
        
        progress_bar = st.progress(0)
        status_text = st.empty()
        
        for i in range(0, len(data), batch_size):
            batch = data[i:i + batch_size]
            
            if process_func:
                batch_result = process_func(batch)
                results.append(batch_result)
            
            # Update progress
            progress = (i // batch_size + 1) / total_batches
            progress_bar.progress(progress)
            status_text.text(f'Processing batch {i//batch_size + 1}/{total_batches}')
        
        progress_bar.empty()
        status_text.empty()
        
        return pd.concat(results) if results else data
    
    def create_performance_dashboard(self):
        """Create performance monitoring dashboard"""
        st.subheader("📊 Performance Monitoring")
        
        # System metrics
        self.monitor_performance()
        
        # Cache statistics
        cache_files = os.listdir(self.cache_dir) if os.path.exists(self.cache_dir) else []
        cache_size = sum(
            os.path.getsize(os.path.join(self.cache_dir, f)) 
            for f in cache_files
        ) / (1024**2)  # MB
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.metric("Cache Files", len(cache_files))
        
        with col2:
            st.metric("Cache Size", f"{cache_size:.1f} MB")
        
        # Performance tips
        with st.expander("🚀 Performance Tips"):
            st.markdown("""
            - **Use caching**: All data loading functions use smart caching
            - **Lazy loading**: Data loads only when needed
            - **Batch processing**: Large datasets processed in chunks
            - **Memory optimization**: DataFrames optimized for memory usage
            - **Progress indicators**: User feedback for long operations
            """)
    
    def benchmark_function(self, func, *args, **kwargs):
        """Benchmark function execution time"""
        start_time = time.time()
        result = func(*args, **kwargs)
        end_time = time.time()
        
        execution_time = end_time - start_time
        
        return result, execution_time
    
    def clear_cache(self):
        """Clear all cached files"""
        if os.path.exists(self.cache_dir):
            for file in os.listdir(self.cache_dir):
                os.remove(os.path.join(self.cache_dir, file))
            st.success("Cache cleared successfully!")
        else:
            st.info("No cache to clear.")