import seaborn as sns
import matplotlib.pyplot as plt
import pandas as pd
import io
import base64

def generate_seaborn_visualizations(df):
    visualizations = []
    
    # Visualization 1: Age Distribution by Gender
    plt.figure(figsize=(10, 6))
    sns.histplot(data=df, x='Age', hue='Gender', kde=True, bins=20, alpha=0.6)
    plt.title('Age Distribution by Gender')
    plt.xlabel('Age')
    plt.ylabel('Count')
    visualizations.append(save_plot_to_base64(plt, 'Age Distribution by Gender'))
    plt.close()
    
    # Visualization 2: Purchase Amount by Category and Gender
    plt.figure(figsize=(12, 6))
    sns.barplot(data=df, x='Category', y='Purchase Amount (USD)', hue='Gender', ci=None)
    plt.title('Average Purchase Amount by Category and Gender')
    plt.xlabel('Category')
    plt.ylabel('Average Purchase Amount (USD)')
    plt.xticks(rotation=45)
    visualizations.append(save_plot_to_base64(plt, 'Purchase Amount by Category and Gender'))
    plt.close()
    
    # Visualization 3: Heatmap of Correlation
    plt.figure(figsize=(10, 8))
    numeric_df = df.select_dtypes(include=['int64', 'float64'])
    sns.heatmap(numeric_df.corr(), annot=True, cmap='coolwarm', center=0)
    plt.title('Correlation Heatmap')
    visualizations.append(save_plot_to_base64(plt, 'Correlation Heatmap'))
    plt.close()
    
    # Visualization 4: Boxplot of Purchase Amount by Season
    plt.figure(figsize=(10, 6))
    sns.boxplot(data=df, x='Season', y='Purchase Amount (USD)', palette='pastel')
    plt.title('Purchase Amount Distribution by Season')
    plt.xlabel('Season')
    plt.ylabel('Purchase Amount (USD)')
    visualizations.append(save_plot_to_base64(plt, 'Purchase Amount by Season'))
    plt.close()
    
    return {
        'library': 'seaborn',
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