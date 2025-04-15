import matplotlib.pyplot as plt
import pandas as pd
import io
import base64

def generate_matplotlib_visualizations(df):
    visualizations = []    
    # Visualization 1: Age Distribution
    plt.figure(figsize=(10, 6))
    plt.hist(df['Age'].values, bins=20, edgecolor='black', color='skyblue')
    plt.title('Age Distribution of Customers')
    plt.xlabel('Age')
    plt.ylabel('Count')
    visualizations.append(save_plot_to_base64(plt, 'Age Distribution'))
    plt.close()
    
    # Visualization 2: Purchase Amount by Category
    plt.figure(figsize=(10, 6))
    df.groupby('Category')['Purchase Amount (USD)'].mean().sort_values().plot(kind='barh', color='skyblue')
    plt.title('Average Purchase Amount by Category')
    plt.xlabel('Average Purchase Amount (USD)')
    plt.ylabel('Category')
    visualizations.append(save_plot_to_base64(plt, 'Purchase Amount by Category'))
    plt.close()
    
    # Visualization 3: Payment Method Distribution
    plt.figure(figsize=(10, 6))
    df['Payment Method'].value_counts().plot(kind='pie', autopct='%1.1f%%')
    plt.title('Payment Method Distribution')
    plt.ylabel('')
    visualizations.append(save_plot_to_base64(plt, 'Payment Method Distribution'))
    plt.close()
    
    # Visualization 4: Purchase Amount vs. Review Rating
    plt.figure(figsize=(10, 6))
    plt.scatter(df['Purchase Amount (USD)'], df['Review Rating'], alpha=0.5)
    plt.title('Purchase Amount vs. Review Rating')
    plt.xlabel('Purchase Amount (USD)')
    plt.ylabel('Review Rating')
    visualizations.append(save_plot_to_base64(plt, 'Purchase Amount vs Review Rating'))
    plt.close()
    
    return {
        'library': 'matplotlib',
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