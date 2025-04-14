import pandas as pd
import matplotlib.pyplot as plt
import io
import base64

def generate_pandas_visualizations(df):
    visualizations = []
    
    # Visualization 1: Top 10 Items Purchased
    plt.figure(figsize=(10, 6))
    df['Item Purchased'].value_counts().head(10).sort_values().plot(kind='barh', color='teal')
    plt.title('Top 10 Most Purchased Items')
    plt.xlabel('Count')
    plt.ylabel('Item')
    visualizations.append(save_plot_to_base64(plt, 'Top 10 Items Purchased'))
    plt.close()
    
    # Visualization 2: Subscription Status Distribution
    plt.figure(figsize=(8, 6))
    df['Subscription Status'].value_counts().plot(kind='pie', autopct='%1.1f%%', colors=['lightgreen', 'lightcoral'])
    plt.title('Subscription Status Distribution')
    plt.ylabel('')
    visualizations.append(save_plot_to_base64(plt, 'Subscription Status Distribution'))
    plt.close()
    
    # Visualization 3: Previous Purchases Distribution
    plt.figure(figsize=(10, 6))
    df['Previous Purchases'].plot(kind='hist', bins=20, edgecolor='black', color='purple', alpha=0.7)
    plt.title('Distribution of Previous Purchases')
    plt.xlabel('Number of Previous Purchases')
    plt.ylabel('Count')
    visualizations.append(save_plot_to_base64(plt, 'Previous Purchases Distribution'))
    plt.close()
    
    # Visualization 4: Purchase Amount Over Age
    plt.figure(figsize=(10, 6))
    df.plot(kind='scatter', x='Age', y='Purchase Amount (USD)', alpha=0.5, color='orange')
    plt.title('Purchase Amount Over Age')
    plt.xlabel('Age')
    plt.ylabel('Purchase Amount (USD)')
    visualizations.append(save_plot_to_base64(plt, 'Purchase Amount Over Age'))
    plt.close()
    
    return {
        'library': 'pandas',
        'visualizations': visualizations
    }

def save_plot_to_base64(plt, title):
    buffer = io.BytesIO()
    plt.savefig(buffer, format='png', bbox_inches='tight')
    buffer.seek(0)
    image_base64 = base64.b64encode(buffer.read()).decode('utf-8')
    return {
        'title': title,
        'image': f'data:image/png;base64,{image_base64}'
    }