import pandas as pd
import matplotlib.pyplot as plt
import io
import base64

def generate_pandas_visualizations(df):
    visualizations = []
    
    # Visualization 1: Top 10 Items Purchased
    plt.figure(figsize=(10, 6))
    
    # Get items frequency and prepare data for plotting
    item_counts = df['Item Purchased'].value_counts()
    top_10_items = item_counts.head(10)
    sorted_top_items = top_10_items.sort_values()
    
    # Create horizontal bar chart
    sorted_top_items.plot(kind='barh', color='teal')
    
    # Add chart labels
    plt.title('Top 10 Most Purchased Items')
    plt.xlabel('Count')
    plt.ylabel('Item')
    
    # Save and close
    visualizations.append(save_plot_to_base64(plt, 'Top 10 Items Purchased'))
    plt.close()
    
    # Visualization 2: Subscription Status Distribution
    plt.figure(figsize=(8, 6))
    # Get subscription status counts
    subscription_counts = df['Subscription Status'].value_counts()
    # Create pie chart
    subscription_counts.plot(
        kind='pie', 
        autopct='%1.1f%%', 
        colors=['lightcoral', 'lightgreen']
    )
    # Customize chart appearance
    plt.title('Subscription Status Distribution')
    plt.ylabel('')  # Remove y-label for cleaner look
    
    # Save and close
    visualizations.append(save_plot_to_base64(plt, 'Subscription Status Distribution'))
    plt.close()
    
    
    # Visualization 3: Previous Purchases Distribution    
    # Step 1: Create a new figure with specified size 
    plt.figure(figsize=(10, 6))
    purchase_history = df['Previous Purchases'] 
    purchase_history.plot(
        kind='hist',       # Create a histogram
        bins=20,           # Divide data into 20 bins
        edgecolor='black', # Add black edges to bars
        color='purple',    # Fill bars with purple color
        alpha=0.7          # Make bars slightly transparent (0.7 = 70% opaque)
    )
    plt.title('Distribution of Previous Purchases')
    plt.xlabel('Number of Previous Purchases')
    plt.ylabel('Count')
    
    # Step 4: Save the visualization and close the figure
    visualizations.append(save_plot_to_base64(plt, 'Previous Purchases Distribution'))
    plt.close()
    
    # Visualization 4: Purchase Amount Over Age
    plt.figure(figsize=(10, 6))
    df.plot(kind='scatter'
            , x='Age',
            y='Purchase Amount (USD)',
            alpha=0.5,
            color='orange')
    plt.title('Purchase Amount Over Age')
    plt.xlabel('Age')
    plt.ylabel('Purchase Amount (USD)')
    visualizations.append(save_plot_to_base64(plt, 'Purchase Amount Over Age'))
    plt.close()

    # Visualization 5: Payment Method Popularity
    plt.figure(figsize=(10, 6))
    payment_counts = df['Payment Method'].value_counts().sort_values()
    payment_counts.plot(
        kind='barh',
        color=['skyblue', 'lightgreen', 'salmon', 'gold'],
        edgecolor='black'
    )
    plt.title('Most Popular Payment Methods')
    plt.xlabel('Number of Transactions')
    plt.ylabel('Payment Method')
    plt.grid(axis='x', linestyle='--', alpha=0.4)
    visualizations.append(save_plot_to_base64(plt, 'Payment Method Popularity'))
    plt.close()

    # Visualization 6: Purchase Amount by Category
    plt.figure(figsize=(12, 6))
    df.boxplot(
        column='Purchase Amount (USD)',
        by='Category',
        vert=False,
        patch_artist=True,
        boxprops={'facecolor': 'lightblue'},
        flierprops={'marker': 'o', 'markersize': 5, 'markerfacecolor': 'red'}
    )
    plt.title('Purchase Amount Distribution by Category')
    plt.suptitle('')  
    plt.xlabel('Purchase Amount (USD)')
    plt.ylabel('Category')
    plt.grid(axis='x', linestyle='--', alpha=0.3)
    visualizations.append(save_plot_to_base64(plt, 'Purchase Amount by Category'))
    plt.close()
    
    # NEW Visualization 7: Review Rating Distribution
    plt.figure(figsize=(10, 6))
    df['Review Rating'].plot(
        kind='hist',
        bins=10,
        color='lightgreen',
        edgecolor='black',
        alpha=0.7
    )
    plt.title('Distribution of Review Ratings')
    plt.xlabel('Rating')
    plt.ylabel('Count')
    plt.grid(axis='y', linestyle='--', alpha=0.4)
    visualizations.append(save_plot_to_base64(plt, 'Review Rating Distribution'))
    plt.close()
    
    # NEW Visualization 8: Seasonal Purchase Patterns
    plt.figure(figsize=(10, 6))
    season_data = df.groupby('Season')['Purchase Amount (USD)'].mean().sort_values()
    season_data.plot(
        kind='bar',
        color='skyblue',
        edgecolor='black'
    )
    plt.title('Average Purchase Amount by Season')
    plt.xlabel('Season')
    plt.ylabel('Average Purchase Amount (USD)')
    plt.xticks(rotation=45)
    plt.grid(axis='y', linestyle='--', alpha=0.4)
    visualizations.append(save_plot_to_base64(plt, 'Seasonal Purchase Patterns'))
    plt.close()
    
    # NEW Visualization 9: Size Popularity Breakdown
    plt.figure(figsize=(8, 6))
    size_counts = df['Size'].value_counts()
    size_counts.plot(
        kind='pie',
        autopct='%1.1f%%',
        colors=['#ff9999', '#66b3ff', '#99ff99', '#ffcc99'],
        shadow=True
    )
    plt.title('Size Popularity Breakdown')
    plt.ylabel('')
    visualizations.append(save_plot_to_base64(plt, 'Size Popularity'))
    plt.close()
    
    # NEW Visualization 10: Color Preference Analysis
    plt.figure(figsize=(12, 6))
    color_counts = df['Color'].value_counts().head(10).sort_values()
    color_counts.plot(
        kind='barh',
        colormap='viridis'
    )
    plt.title('Top 10 Most Popular Colors')
    plt.xlabel('Count')
    plt.ylabel('Color')
    plt.grid(axis='x', linestyle='--', alpha=0.4)
    visualizations.append(save_plot_to_base64(plt, 'Color Preference Analysis'))
    plt.close()
    
    # NEW Visualization 11: Location-based Purchase Comparison
    plt.figure(figsize=(12, 6))
    location_data = df.groupby('Location')['Purchase Amount (USD)'].mean().sort_values(ascending=False).head(10)
    location_data.plot(
        kind='bar',
        color='coral',
        edgecolor='black'
    )
    plt.title('Top 10 Locations by Average Purchase Amount')
    plt.xlabel('Location')
    plt.ylabel('Average Purchase Amount (USD)')
    plt.xticks(rotation=45)
    plt.grid(axis='y', linestyle='--', alpha=0.4)
    visualizations.append(save_plot_to_base64(plt, 'Location Purchase Comparison'))
    plt.close()
    
    # NEW Visualization 12: Shipping Type Preference
    plt.figure(figsize=(10, 6))
    shipping_counts = df['Shipping Type'].value_counts().sort_values()
    shipping_counts.plot(
        kind='barh',
        color='lightseagreen'
    )
    plt.title('Shipping Type Popularity')
    plt.xlabel('Count')
    plt.ylabel('Shipping Type')
    plt.grid(axis='x', linestyle='--', alpha=0.4)
    visualizations.append(save_plot_to_base64(plt, 'Shipping Type Preference'))
    plt.close()
    
    # NEW Visualization 13: Discount Impact Analysis
    plt.figure(figsize=(8, 6))
    discount_impact = df.groupby('Discount Applied')['Purchase Amount (USD)'].mean()
    discount_impact.index = ['No Discount', 'Discount Applied']
    discount_impact.plot(
        kind='bar',
        color=['#ff9999', '#66b3ff'],
        edgecolor='black'
    )
    plt.title('Impact of Discount on Average Purchase Amount')
    plt.xlabel('Discount Status')
    plt.ylabel('Average Purchase Amount (USD)')
    plt.xticks(rotation=0)
    plt.grid(axis='y', linestyle='--', alpha=0.4)
    visualizations.append(save_plot_to_base64(plt, 'Discount Impact Analysis'))
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