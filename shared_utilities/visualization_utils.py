"""
Shared Visualization Utilities
==============================

Common visualization functions used across all EY Data Analytics projects.
Provides consistent, professional charts and graphs.

Author: Data Analytics Portfolio for EY
"""

import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import pandas as pd
import numpy as np

class VisualizationUtils:
    """Utility class for creating consistent visualizations"""
    
    # EY Brand Colors
    EY_COLORS = {
        'primary': '#1f77b4',
        'secondary': '#ff7f0e',
        'success': '#2ca02c',
        'warning': '#ff7f0e',
        'danger': '#d62728',
        'info': '#17a2b8',
        'light': '#f8f9fa',
        'dark': '#343a40'
    }
    
    # Color palettes for different use cases
    PALETTES = {
        'financial': ['#1f77b4', '#ff7f0e', '#2ca02c', '#d62728', '#9467bd'],
        'supply_chain': ['#2E8B57', '#FF8C00', '#DC143C', '#8B4513', '#32CD32'],
        'customer': ['#8B4513', '#FFD700', '#FF6347', '#32CD32', '#1E90FF'],
        'esg': ['#228B22', '#32CD32', '#FFD700', '#FF6347', '#1E90FF']
    }
    
    @classmethod
    def create_metric_card(cls, title, value, delta=None, delta_color='normal'):
        """
        Create a metric card visualization
        
        Args:
            title: Card title
            value: Main value to display
            delta: Change value
            delta_color: Color of delta ('normal', 'inverse', 'off')
        
        Returns:
            plotly.graph_objects.Figure
        """
        fig = go.Figure()
        
        # Add text annotations
        fig.add_annotation(
            x=0.5, y=0.7,
            text=f"<b>{title}</b>",
            showarrow=False,
            font=dict(size=14, color=cls.EY_COLORS['dark'])
        )
        
        fig.add_annotation(
            x=0.5, y=0.4,
            text=f"<b>{value}</b>",
            showarrow=False,
            font=dict(size=24, color=cls.EY_COLORS['primary'])
        )
        
        if delta:
            delta_color_map = {
                'normal': cls.EY_COLORS['success'] if delta.startswith('+') else cls.EY_COLORS['danger'],
                'inverse': cls.EY_COLORS['danger'] if delta.startswith('+') else cls.EY_COLORS['success'],
                'off': cls.EY_COLORS['dark']
            }
            
            fig.add_annotation(
                x=0.5, y=0.1,
                text=f"<b>{delta}</b>",
                showarrow=False,
                font=dict(size=12, color=delta_color_map[delta_color])
            )
        
        fig.update_layout(
            xaxis=dict(visible=False),
            yaxis=dict(visible=False),
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            margin=dict(l=0, r=0, t=0, b=0),
            height=150
        )
        
        return fig
    
    @classmethod
    def create_trend_chart(cls, df, x_col, y_col, title, color=None, palette='financial'):
        """
        Create a trend line chart
        
        Args:
            df: DataFrame with data
            x_col: Column name for x-axis
            y_col: Column name for y-axis
            title: Chart title
            color: Color for the line
            palette: Color palette to use
        
        Returns:
            plotly.graph_objects.Figure
        """
        if color is None:
            color = cls.PALETTES[palette][0]
        
        fig = px.line(
            df, 
            x=x_col, 
            y=y_col,
            title=title,
            color_discrete_sequence=[color]
        )
        
        fig.update_layout(
            title_font_size=16,
            title_font_color=cls.EY_COLORS['dark'],
            xaxis_title_font_size=12,
            yaxis_title_font_size=12,
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)'
        )
        
        return fig
    
    @classmethod
    def create_bar_chart(cls, df, x_col, y_col, title, color_col=None, palette='financial'):
        """
        Create a bar chart
        
        Args:
            df: DataFrame with data
            x_col: Column name for x-axis
            y_col: Column name for y-axis
            title: Chart title
            color_col: Column to use for coloring
            palette: Color palette to use
        
        Returns:
            plotly.graph_objects.Figure
        """
        if color_col:
            fig = px.bar(
                df, 
                x=x_col, 
                y=y_col,
                color=color_col,
                title=title,
                color_discrete_sequence=cls.PALETTES[palette]
            )
        else:
            fig = px.bar(
                df, 
                x=x_col, 
                y=y_col,
                title=title,
                color_discrete_sequence=[cls.PALETTES[palette][0]]
            )
        
        fig.update_layout(
            title_font_size=16,
            title_font_color=cls.EY_COLORS['dark'],
            xaxis_title_font_size=12,
            yaxis_title_font_size=12,
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)'
        )
        
        return fig
    
    @classmethod
    def create_scatter_plot(cls, df, x_col, y_col, title, size_col=None, color_col=None, palette='financial'):
        """
        Create a scatter plot
        
        Args:
            df: DataFrame with data
            x_col: Column name for x-axis
            y_col: Column name for y-axis
            title: Chart title
            size_col: Column to use for point size
            color_col: Column to use for coloring
            palette: Color palette to use
        
        Returns:
            plotly.graph_objects.Figure
        """
        fig = px.scatter(
            df, 
            x=x_col, 
            y=y_col,
            size=size_col,
            color=color_col,
            title=title,
            color_discrete_sequence=cls.PALETTES[palette]
        )
        
        fig.update_layout(
            title_font_size=16,
            title_font_color=cls.EY_COLORS['dark'],
            xaxis_title_font_size=12,
            yaxis_title_font_size=12,
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)'
        )
        
        return fig
    
    @classmethod
    def create_pie_chart(cls, df, values_col, names_col, title, palette='financial'):
        """
        Create a pie chart
        
        Args:
            df: DataFrame with data
            values_col: Column name for values
            names_col: Column name for labels
            title: Chart title
            palette: Color palette to use
        
        Returns:
            plotly.graph_objects.Figure
        """
        fig = px.pie(
            df, 
            values=values_col, 
            names=names_col,
            title=title,
            color_discrete_sequence=cls.PALETTES[palette]
        )
        
        fig.update_layout(
            title_font_size=16,
            title_font_color=cls.EY_COLORS['dark'],
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)'
        )
        
        return fig
    
    @classmethod
    def create_heatmap(cls, df, x_col, y_col, values_col, title, palette='financial'):
        """
        Create a heatmap
        
        Args:
            df: DataFrame with data
            x_col: Column name for x-axis
            y_col: Column name for y-axis
            values_col: Column name for values
            title: Chart title
            palette: Color palette to use
        
        Returns:
            plotly.graph_objects.Figure
        """
        # Pivot data for heatmap
        heatmap_data = df.pivot(index=y_col, columns=x_col, values=values_col)
        
        fig = px.imshow(
            heatmap_data,
            title=title,
            color_continuous_scale=cls.PALETTES[palette]
        )
        
        fig.update_layout(
            title_font_size=16,
            title_font_color=cls.EY_COLORS['dark'],
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)'
        )
        
        return fig
    
    @classmethod
    def create_gauge_chart(cls, value, max_value, title, color=None):
        """
        Create a gauge chart
        
        Args:
            value: Current value
            max_value: Maximum value
            title: Chart title
            color: Color for the gauge
        
        Returns:
            plotly.graph_objects.Figure
        """
        if color is None:
            color = cls.EY_COLORS['primary']
        
        fig = go.Figure(go.Indicator(
            mode = "gauge+number+delta",
            value = value,
            domain = {'x': [0, 1], 'y': [0, 1]},
            title = {'text': title},
            delta = {'reference': max_value * 0.8},
            gauge = {
                'axis': {'range': [None, max_value]},
                'bar': {'color': color},
                'steps': [
                    {'range': [0, max_value * 0.5], 'color': "lightgray"},
                    {'range': [max_value * 0.5, max_value * 0.8], 'color': "gray"}
                ],
                'threshold': {
                    'line': {'color': "red", 'width': 4},
                    'thickness': 0.75,
                    'value': max_value * 0.9
                }
            }
        ))
        
        fig.update_layout(
            title_font_size=16,
            title_font_color=cls.EY_COLORS['dark'],
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            height=300
        )
        
        return fig
    
    @classmethod
    def create_radar_chart(cls, categories, values, title, max_value=100):
        """
        Create a radar chart
        
        Args:
            categories: List of category names
            values: List of values for each category
            title: Chart title
            max_value: Maximum value for the scale
        
        Returns:
            plotly.graph_objects.Figure
        """
        fig = go.Figure()
        
        fig.add_trace(go.Scatterpolar(
            r=values,
            theta=categories,
            fill='toself',
            name='Performance',
            line_color=cls.EY_COLORS['primary']
        ))
        
        fig.update_layout(
            polar=dict(
                radialaxis=dict(
                    visible=True,
                    range=[0, max_value]
                )),
            showlegend=True,
            title=title,
            title_font_size=16,
            title_font_color=cls.EY_COLORS['dark'],
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            height=400
        )
        
        return fig
    
    @classmethod
    def add_ey_styling(cls, fig):
        """
        Add EY styling to any plotly figure
        
        Args:
            fig: plotly.graph_objects.Figure to style
        
        Returns:
            Styled plotly.graph_objects.Figure
        """
        fig.update_layout(
            font=dict(family="Arial", size=12, color=cls.EY_COLORS['dark']),
            title_font_size=18,
            title_font_color=cls.EY_COLORS['primary'],
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            margin=dict(l=50, r=50, t=50, b=50)
        )
        
        return fig

# Example usage
if __name__ == "__main__":
    # Create sample data
    df = pd.DataFrame({
        'Category': ['A', 'B', 'C', 'D'],
        'Value': [10, 20, 15, 25],
        'Trend': [1, 2, 1.5, 2.5]
    })
    
    viz = VisualizationUtils()
    
    # Create sample charts
    bar_chart = viz.create_bar_chart(df, 'Category', 'Value', 'Sample Bar Chart')
    trend_chart = viz.create_trend_chart(df, 'Category', 'Trend', 'Sample Trend Chart')
    
    print("Sample visualizations created successfully!")
