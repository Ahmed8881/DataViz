import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
import io
import base64

def generate_numpy_visualizations(df):
    visualizations = []
    
    # Visualization 1: Average Age by Payment Method
    payment_methods = df['Preferred Payment Method'].unique()
    mean_ages = [df[df['Preferred Payment Method'] == method]['Age'].mean() for method in payment_methods]

    plt.figure(figsize=(10, 6))
    plt.bar(payment_methods, mean_ages, color=['skyblue', 'lightgreen', 'salmon'])
    plt.title('Average Age by Payment Method')
    plt.xlabel('Payment Method')
    plt.ylabel('Average Age')
    plt.xticks(rotation=45)
    visualizations.append(save_plot_to_base64(plt, 'Average Age by Payment Method'))
    plt.close()
    
    # Visualization 2: Average Purchase Amount by Category
    avg_purchase = df.groupby('Category')['Purchase Amount (USD)'].mean()
    plt.figure(figsize=(10, 6))
    plt.bar(avg_purchase.index, avg_purchase.values, color='lightblue')
    plt.title('Average Purchase Amount by Category')
    plt.xlabel('Category')
    plt.ylabel('Average Purchase Amount (USD)')
    plt.xticks(rotation=45)
    visualizations.append(save_plot_to_base64(plt, 'Average Purchase Amount by Category'))
    plt.close()
    
    # Visualization 3: Discount Application by Category
    discount_by_category = df.groupby(['Category', 'Discount Applied']).size().unstack()
    plt.figure(figsize=(10, 6))
    discount_by_category.plot(kind='bar', stacked=True, color=['salmon', 'lightgreen'])
    plt.title('Discount Application by Category')
    plt.xlabel('Category')
    plt.ylabel('Count')
    plt.xticks(rotation=45)
    plt.legend(title='Discount Applied?')
    visualizations.append(save_plot_to_base64(plt, 'Discount Application by Category'))
    plt.close()
    
    # Visualization 4: Review Rating Distribution
    plt.figure(figsize=(10, 6))
    x = np.linspace(df['Review Rating'].min(), df['Review Rating'].max(), 100)
    y = np.exp(-(x - df['Review Rating'].mean())**2 / (2 * df['Review Rating'].std()))  # Gaussian approximation
    plt.plot(x, y, color='purple', label='Approx. Distribution')
    plt.hist(df['Review Rating'], bins=15, density=True, alpha=0.5, color='orange')
    plt.title('Review Rating Distribution')
    plt.xlabel('Review Rating')
    plt.ylabel('Density')
    plt.legend()
    visualizations.append(save_plot_to_base64(plt, 'Review Rating Distribution'))
    plt.close()

    #Visualization 05:  Purchase Frequency by Gender
    plt.figure(figsize=(10, 6))
    counts = df.groupby(['Frequency of Purchases', 'Gender']).size().unstack()
    counts.plot(kind='bar', color=['lightpink', 'lightblue'])
    plt.title('Purchase Frequency by Gender')
    plt.xlabel('Frequency of Purchases')
    plt.ylabel('Count')
    plt.xticks(rotation=45)
    plt.legend(title='Gender')
    visualizations.append(save_plot_to_base64(plt, 'Purchase Frequency by Gender'))
    plt.close()

    #Visualization 06:  Average Rating by Season
    plt.figure(figsize=(10, 6))
    avg_ratings = df.groupby('Season')['Review Rating'].mean()
    plt.plot(avg_ratings.index, avg_ratings.values, marker='o', color='purple')
    plt.title('Average Rating by Season')
    plt.xlabel('Season')
    plt.ylabel('Average Rating')
    plt.ylim(0, 5) 
    plt.grid(True, linestyle='--', alpha=0.3)
    visualizations.append(save_plot_to_base64(plt, 'Average Rating by Season'))
    plt.close()
    
    return {
        'library': 'numpy',
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