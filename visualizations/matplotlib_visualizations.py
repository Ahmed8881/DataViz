import matplotlib.pyplot as plt
import pandas as pd
import io
import base64

def generate_matplotlib_visualizations(df):
    # Clean data before visualization
    df_clean = df.copy()
    
    # Fill missing numeric values with their respective means
    numeric_cols = ['Age', 'Purchase Amount (USD)', 'Review Rating']
    for col in numeric_cols:
        if col in df_clean.columns:
            df_clean[col] = df_clean[col].fillna(df_clean[col].mean())
    
    # Fill missing categorical values with their most frequent value
    categorical_cols = ['Category', 'Payment Method']
    for col in categorical_cols:
        if col in df_clean.columns:
            df_clean[col] = df_clean[col].fillna(df_clean[col].mode()[0])
    
    # Drop any remaining rows with missing values in critical columns
    critical_cols = ['Age', 'Category', 'Purchase Amount (USD)', 'Payment Method', 'Review Rating']
    df_clean = df_clean.dropna(subset=[col for col in critical_cols if col in df_clean.columns])
    
    visualizations = []    
    
    # Visualization 1: Age Distribution
    plt.figure(figsize=(10, 6))
    plt.hist(df_clean['Age'].values, bins=20, edgecolor='black', color='skyblue')
    plt.title('Age Distribution of Customers')
    plt.xlabel('Age')
    plt.ylabel('Count')
    visualizations.append(save_plot_to_base64(plt, 'Age Distribution'))
    plt.close()
    
    # Visualization 2: Purchase Amount by Category
    plt.figure(figsize=(10, 6))
    category_means = df_clean.groupby('Category')['Purchase Amount (USD)'].mean().sort_values()
    categories = category_means.index
    means = category_means.values 
    plt.barh(categories, means, color='skyblue', edgecolor='black')
    plt.title('Average Purchase Amount by Category')
    plt.xlabel('Average Purchase Amount (USD)')
    plt.ylabel('Category')
    visualizations.append(save_plot_to_base64(plt, 'Purchase Amount by Category'))
    plt.close()
    
    # Visualization 3: Payment Method Distribution
    plt.figure(figsize=(8, 6))
    payment_counts = df_clean['Payment Method'].value_counts()
    plt.pie(payment_counts, labels=payment_counts.index, autopct='%1.1f%%')
    plt.title('Payment Method Distribution')
    visualizations.append(save_plot_to_base64(plt, 'Payment Method Distribution'))
    plt.close()
    
    # Visualization 4: Purchase Amount vs. Review Rating
    plt.figure(figsize=(10, 6))
    plt.scatter(df_clean['Purchase Amount (USD)'], df_clean['Review Rating'], alpha=0.5)
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