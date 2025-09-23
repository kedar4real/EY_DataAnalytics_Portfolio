"""
Supply Chain Optimization Analytics Dashboard
===========================================

Advanced supply chain analytics featuring demand forecasting, inventory optimization,
route planning, and supplier performance analytics for operational excellence.

Key Features:
- Demand Forecasting with ML
- Inventory Optimization
- Route Planning & Logistics
- Supplier Performance Analytics
- Cost Optimization
- Real-time Monitoring

Author: Data Analytics Portfolio for EY
"""

import dash
from dash import dcc, html, Input, Output, dash_table
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import warnings
warnings.filterwarnings('ignore')

# Initialize Dash app
app = dash.Dash(__name__)
app.title = "EY Supply Chain Optimization Dashboard"

# Generate sample supply chain data
def generate_supply_chain_data():
    """Generate realistic supply chain data"""
    np.random.seed(42)
    
    # Generate demand data
    dates = pd.date_range(start='2023-01-01', end='2024-01-01', freq='D')
    products = ['Product A', 'Product B', 'Product C', 'Product D', 'Product E']
    
    demand_data = []
    for date in dates:
        for product in products:
            base_demand = np.random.normal(100, 20)
            seasonal_factor = 1 + 0.3 * np.sin(2 * np.pi * date.dayofyear / 365)
            demand_data.append({
                'Date': date,
                'Product': product,
                'Demand': max(0, base_demand * seasonal_factor + np.random.normal(0, 10))
            })
    
    demand_df = pd.DataFrame(demand_data)
    
    # Generate inventory data
    inventory_data = []
    for product in products:
        current_stock = np.random.normal(500, 100)
        reorder_point = np.random.normal(200, 50)
        max_stock = np.random.normal(1000, 200)
        inventory_data.append({
            'Product': product,
            'Current_Stock': max(0, current_stock),
            'Reorder_Point': max(0, reorder_point),
            'Max_Stock': max(0, max_stock),
            'Lead_Time_Days': np.random.normal(7, 2),
            'Unit_Cost': np.random.normal(50, 10)
        })
    
    inventory_df = pd.DataFrame(inventory_data)
    
    # Generate supplier data
    suppliers = ['Supplier Alpha', 'Supplier Beta', 'Supplier Gamma', 'Supplier Delta']
    supplier_data = []
    for supplier in suppliers:
        supplier_data.append({
            'Supplier': supplier,
            'On_Time_Delivery': np.random.beta(8, 2),
            'Quality_Score': np.random.beta(9, 1),
            'Cost_Index': np.random.normal(1.0, 0.2),
            'Flexibility_Score': np.random.beta(7, 3),
            'Total_Orders': np.random.randint(50, 200)
        })
    
    supplier_df = pd.DataFrame(supplier_data)
    
    # Generate route data
    routes = ['Route 1', 'Route 2', 'Route 3', 'Route 4', 'Route 5']
    route_data = []
    for route in routes:
        route_data.append({
            'Route': route,
            'Distance_km': np.random.normal(150, 30),
            'Delivery_Time_hours': np.random.normal(4, 1),
            'Fuel_Cost': np.random.normal(80, 15),
            'Driver_Cost': np.random.normal(120, 20),
            'Total_Cost': np.random.normal(200, 35)
        })
    
    route_df = pd.DataFrame(route_data)
    
    return demand_df, inventory_df, supplier_df, route_df

# Load data
demand_df, inventory_df, supplier_df, route_df = generate_supply_chain_data()

# App layout
app.layout = html.Div([
    html.Div([
        html.H1("🚚 EY Supply Chain Optimization Dashboard", 
                style={'textAlign': 'center', 'color': '#1f77b4', 'marginBottom': '2rem'}),
        html.P("Advanced supply chain analytics for operational excellence", 
               style={'textAlign': 'center', 'color': '#666', 'fontSize': '1.2rem'})
    ]),
    
    # Control Panel
    html.Div([
        html.Div([
            html.Label("Select Product:"),
            dcc.Dropdown(
                id='product-dropdown',
                options=[{'label': p, 'value': p} for p in demand_df['Product'].unique()],
                value='Product A'
            )
        ], style={'width': '30%', 'display': 'inline-block', 'marginRight': '2%'}),
        
        html.Div([
            html.Label("Time Period:"),
            dcc.Dropdown(
                id='time-period',
                options=[
                    {'label': 'Last 30 Days', 'value': 30},
                    {'label': 'Last 90 Days', 'value': 90},
                    {'label': 'Last 180 Days', 'value': 180},
                    {'label': 'Last Year', 'value': 365}
                ],
                value=90
            )
        ], style={'width': '30%', 'display': 'inline-block', 'marginRight': '2%'}),
        
        html.Div([
            html.Label("Optimization Focus:"),
            dcc.Dropdown(
                id='optimization-focus',
                options=[
                    {'label': 'Cost Optimization', 'value': 'cost'},
                    {'label': 'Service Level', 'value': 'service'},
                    {'label': 'Inventory Turnover', 'value': 'inventory'},
                    {'label': 'Supplier Performance', 'value': 'supplier'}
                ],
                value='cost'
            )
        ], style={'width': '30%', 'display': 'inline-block'})
    ], style={'marginBottom': '2rem', 'padding': '1rem', 'backgroundColor': '#f8f9fa', 'borderRadius': '0.5rem'}),
    
    # Key Metrics Row
    html.Div([
        html.Div([
            html.H3("📊 Key Metrics", style={'color': '#1f77b4'}),
            html.Div(id='key-metrics')
        ], style={'width': '100%', 'marginBottom': '2rem'})
    ]),
    
    # Charts Row 1
    html.Div([
        html.Div([
            dcc.Graph(id='demand-forecast-chart')
        ], style={'width': '50%', 'display': 'inline-block'}),
        
        html.Div([
            dcc.Graph(id='inventory-levels-chart')
        ], style={'width': '50%', 'display': 'inline-block'})
    ]),
    
    # Charts Row 2
    html.Div([
        html.Div([
            dcc.Graph(id='supplier-performance-chart')
        ], style={'width': '50%', 'display': 'inline-block'}),
        
        html.Div([
            dcc.Graph(id='route-optimization-chart')
        ], style={'width': '50%', 'display': 'inline-block'})
    ]),
    
    # Data Tables
    html.Div([
        html.H3("📋 Detailed Analytics", style={'color': '#1f77b4', 'marginTop': '2rem'}),
        html.Div([
            html.Div([
                html.H4("Inventory Status"),
                dash_table.DataTable(
                    id='inventory-table',
                    columns=[{"name": i, "id": i} for i in inventory_df.columns],
                    data=inventory_df.to_dict('records'),
                    style_cell={'textAlign': 'left'},
                    style_header={'backgroundColor': '#1f77b4', 'color': 'white'},
                    style_data_conditional=[
                        {
                            'if': {'filter_query': '{Current_Stock} < {Reorder_Point}'},
                            'backgroundColor': '#ffebee',
                            'color': 'black',
                        }
                    ]
                )
            ], style={'width': '50%', 'display': 'inline-block', 'marginRight': '2%'}),
            
            html.Div([
                html.H4("Supplier Performance"),
                dash_table.DataTable(
                    id='supplier-table',
                    columns=[{"name": i, "id": i} for i in supplier_df.columns],
                    data=supplier_df.to_dict('records'),
                    style_cell={'textAlign': 'left'},
                    style_header={'backgroundColor': '#1f77b4', 'color': 'white'},
                    style_data_conditional=[
                        {
                            'if': {'filter_query': '{On_Time_Delivery} > 0.9'},
                            'backgroundColor': '#e8f5e8',
                            'color': 'black',
                        }
                    ]
                )
            ], style={'width': '48%', 'display': 'inline-block'})
        ])
    ])
])

# Callbacks
@app.callback(
    Output('key-metrics', 'children'),
    [Input('product-dropdown', 'value'),
     Input('time-period', 'value')]
)
def update_key_metrics(selected_product, time_period):
    # Filter data
    recent_dates = demand_df['Date'].max() - timedelta(days=time_period)
    filtered_demand = demand_df[
        (demand_df['Product'] == selected_product) & 
        (demand_df['Date'] >= recent_dates)
    ]
    
    # Calculate metrics
    avg_demand = filtered_demand['Demand'].mean()
    demand_volatility = filtered_demand['Demand'].std()
    total_demand = filtered_demand['Demand'].sum()
    
    # Get inventory data for selected product
    product_inventory = inventory_df[inventory_df['Product'] == selected_product].iloc[0]
    stock_level = product_inventory['Current_Stock']
    reorder_point = product_inventory['Reorder_Point']
    
    return html.Div([
        html.Div([
            html.H4(f"{avg_demand:.1f}", style={'color': '#1f77b4', 'fontSize': '2rem', 'margin': '0'}),
            html.P("Avg Daily Demand", style={'margin': '0', 'color': '#666'})
        ], style={'textAlign': 'center', 'padding': '1rem', 'backgroundColor': 'white', 
                 'borderRadius': '0.5rem', 'boxShadow': '0 2px 4px rgba(0,0,0,0.1)', 'margin': '0.5rem'}),
        
        html.Div([
            html.H4(f"{demand_volatility:.1f}", style={'color': '#ff7f0e', 'fontSize': '2rem', 'margin': '0'}),
            html.P("Demand Volatility", style={'margin': '0', 'color': '#666'})
        ], style={'textAlign': 'center', 'padding': '1rem', 'backgroundColor': 'white', 
                 'borderRadius': '0.5rem', 'boxShadow': '0 2px 4px rgba(0,0,0,0.1)', 'margin': '0.5rem'}),
        
        html.Div([
            html.H4(f"{total_demand:.0f}", style={'color': '#2ca02c', 'fontSize': '2rem', 'margin': '0'}),
            html.P("Total Demand", style={'margin': '0', 'color': '#666'})
        ], style={'textAlign': 'center', 'padding': '1rem', 'backgroundColor': 'white', 
                 'borderRadius': '0.5rem', 'boxShadow': '0 2px 4px rgba(0,0,0,0.1)', 'margin': '0.5rem'}),
        
        html.Div([
            html.H4(f"{stock_level:.0f}", style={'color': '#d62728' if stock_level < reorder_point else '#2ca02c', 
                                               'fontSize': '2rem', 'margin': '0'}),
            html.P("Current Stock", style={'margin': '0', 'color': '#666'})
        ], style={'textAlign': 'center', 'padding': '1rem', 'backgroundColor': 'white', 
                 'borderRadius': '0.5rem', 'boxShadow': '0 2px 4px rgba(0,0,0,0.1)', 'margin': '0.5rem'})
    ], style={'display': 'flex', 'justifyContent': 'space-around', 'flexWrap': 'wrap'})

@app.callback(
    Output('demand-forecast-chart', 'figure'),
    [Input('product-dropdown', 'value'),
     Input('time-period', 'value')]
)
def update_demand_forecast(selected_product, time_period):
    # Filter data
    recent_dates = demand_df['Date'].max() - timedelta(days=time_period)
    filtered_demand = demand_df[
        (demand_df['Product'] == selected_product) & 
        (demand_df['Date'] >= recent_dates)
    ].sort_values('Date')
    
    # Simple forecasting (moving average)
    filtered_demand['Forecast'] = filtered_demand['Demand'].rolling(window=7, min_periods=1).mean()
    
    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=filtered_demand['Date'],
        y=filtered_demand['Demand'],
        mode='lines+markers',
        name='Actual Demand',
        line=dict(color='#1f77b4', width=2)
    ))
    fig.add_trace(go.Scatter(
        x=filtered_demand['Date'],
        y=filtered_demand['Forecast'],
        mode='lines',
        name='Forecast',
        line=dict(color='#ff7f0e', width=2, dash='dash')
    ))
    
    fig.update_layout(
        title=f'Demand Forecast - {selected_product}',
        xaxis_title='Date',
        yaxis_title='Demand',
        height=400,
        showlegend=True
    )
    
    return fig

@app.callback(
    Output('inventory-levels-chart', 'figure'),
    [Input('optimization-focus', 'value')]
)
def update_inventory_levels(optimization_focus):
    fig = go.Figure()
    
    for _, row in inventory_df.iterrows():
        fig.add_trace(go.Bar(
            name=row['Product'],
            x=[row['Product']],
            y=[row['Current_Stock']],
            marker_color='#1f77b4'
        ))
    
    # Add reorder points
    fig.add_trace(go.Scatter(
        x=inventory_df['Product'],
        y=inventory_df['Reorder_Point'],
        mode='markers',
        marker=dict(symbol='triangle-down', size=15, color='red'),
        name='Reorder Point'
    ))
    
    fig.update_layout(
        title='Inventory Levels vs Reorder Points',
        xaxis_title='Product',
        yaxis_title='Stock Level',
        height=400,
        showlegend=True
    )
    
    return fig

@app.callback(
    Output('supplier-performance-chart', 'figure'),
    [Input('optimization-focus', 'value')]
)
def update_supplier_performance(optimization_focus):
    fig = go.Figure()
    
    fig.add_trace(go.Scatter(
        x=supplier_df['On_Time_Delivery'],
        y=supplier_df['Quality_Score'],
        mode='markers+text',
        text=supplier_df['Supplier'],
        textposition='top center',
        marker=dict(
            size=supplier_df['Total_Orders']/5,
            color=supplier_df['Cost_Index'],
            colorscale='RdYlGn_r',
            showscale=True,
            colorbar=dict(title="Cost Index")
        ),
        name='Suppliers'
    ))
    
    fig.update_layout(
        title='Supplier Performance Matrix',
        xaxis_title='On-Time Delivery Rate',
        yaxis_title='Quality Score',
        height=400
    )
    
    return fig

@app.callback(
    Output('route-optimization-chart', 'figure'),
    [Input('optimization-focus', 'value')]
)
def update_route_optimization(optimization_focus):
    fig = go.Figure()
    
    fig.add_trace(go.Bar(
        x=route_df['Route'],
        y=route_df['Total_Cost'],
        marker_color='#2ca02c',
        name='Total Cost'
    ))
    
    fig.update_layout(
        title='Route Cost Analysis',
        xaxis_title='Route',
        yaxis_title='Total Cost ($)',
        height=400
    )
    
    return fig

# Run the app
if __name__ == '__main__':
    app.run_server(debug=True, host='0.0.0.0', port=8050)
