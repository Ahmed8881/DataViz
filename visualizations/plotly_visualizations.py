import plotly.express as px
import pandas as pd
import io
import base64
from PIL import Image
import plotly.io as pio

def generate_plotly_visualizations(df):
    visualizations = []
    
    # Visualization 1: Interactive Age Distribution
    fig = px.histogram(df, x='Age', nbins=20, title='Interactive Age Distribution')
    visualizations.append(save_plotly_to_base64(fig, 'Interactive Age Distribution'))
    
    # Visualization 2: 3D Scatter Plot
    fig = px.scatter_3d(df, x='Age', y='Purchase Amount (USD)', z='Review Rating',
                       color='Gender', title='3D View: Age, Purchase Amount, and Rating')
    visualizations.append(save_plotly_to_base64(fig, '3D Scatter Plot'))
    
    # Visualization 3: Sunburst Chart
    fig = px.sunburst(df, path=['Category', 'Item Purchased'], 
                     title='Category and Item Purchased Hierarchy')
    visualizations.append(save_plotly_to_base64(fig, 'Sunburst Chart'))
    
    # Visualization 4: Animated Scatter Plot
    fig = px.scatter(df, x='Age', y='Purchase Amount (USD)', 
                    animation_frame='Season', color='Gender',
                    title='Seasonal Purchase Patterns by Age and Gender')
    visualizations.append(save_plotly_to_base64(fig, 'Animated Scatter Plot'))
    
    return {
        'library': 'plotly',
        'visualizations': visualizations
    }

def save_plotly_to_base64(fig, title):
    img_bytes = pio.to_image(fig, format="png")
    image_base64 = base64.b64encode(img_bytes).decode('utf-8')
    return {
        'title': title,
        'image': f'data:image/png;base64,{image_base64}'
    }