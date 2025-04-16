import seaborn as sns
import matplotlib.pyplot as plt
import pandas as pd
import io
import base64
import numpy as np

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
    
    # Visualization 2: Purchase Amount by Category and Gender (fixed deprecated ci parameter)
    plt.figure(figsize=(12, 6))
    sns.barplot(data=df, x='Category', y='Purchase Amount (USD)', hue='Gender', errorbar=None)
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
    
    # Visualization 4: Boxplot of Purchase Amount by Season (fixed palette warning)
    plt.figure(figsize=(10, 6))
    # Create a categorical palette mapping
    season_order = ['Winter', 'Spring', 'Summer', 'Fall']
    sns.boxplot(data=df, x='Season', y='Purchase Amount (USD)', order=season_order, 
                hue='Season', palette='pastel', legend=False)
    plt.title('Purchase Amount Distribution by Season')
    plt.xlabel('Season')
    plt.ylabel('Purchase Amount (USD)')
    visualizations.append(save_plot_to_base64(plt, 'Purchase Amount by Season'))
    plt.close()
    
    # Visualization 5: Review Rating by Category (fixed deprecated parameters)
    plt.figure(figsize=(12, 6))
    sns.pointplot(data=df, x='Category', y='Review Rating', errorbar=None, 
                 hue='Category', palette='Set2', legend=False)
    plt.title('Average Review Rating by Category')
    plt.xlabel('Product Category')
    plt.ylabel('Average Rating')
    plt.xticks(rotation=45)
    plt.grid(axis='y', linestyle='--', alpha=0.7)
    visualizations.append(save_plot_to_base64(plt, 'Review Rating by Category'))
    plt.close()
    
    # Visualization 6: Subscription Status by Gender
    plt.figure(figsize=(10, 6))
    sns.countplot(data=df, x='Subscription Status', hue='Gender', palette='pastel')
    plt.title('Subscription Status Distribution by Gender')
    plt.xlabel('Subscription Status')
    plt.ylabel('Count')
    plt.legend(title='Gender')
    visualizations.append(save_plot_to_base64(plt, 'Subscription Status by Gender'))
    plt.close()
    
    # Visualization 7: Purchase Amount Distribution by Payment Method (fixed palette warning)
    plt.figure(figsize=(12, 6))
    sns.violinplot(data=df, x='Payment Method', y='Purchase Amount (USD)', 
                  hue='Payment Method', palette='muted', legend=False)
    plt.title('Purchase Amount Distribution by Payment Method')
    plt.xlabel('Payment Method')
    plt.ylabel('Purchase Amount (USD)')
    plt.xticks(rotation=45)
    visualizations.append(save_plot_to_base64(plt, 'Purchase Amount by Payment Method'))
    plt.close()
    
    # Visualization 8: Previous Purchases vs Purchase Amount
    plt.figure(figsize=(10, 6))
    sns.regplot(data=df, x='Previous Purchases', y='Purchase Amount (USD)', 
                scatter_kws={'alpha':0.5}, line_kws={'color':'red'})
    plt.title('Relationship Between Previous Purchases and Purchase Amount')
    plt.xlabel('Number of Previous Purchases')
    plt.ylabel('Purchase Amount (USD)')
    plt.grid(True, alpha=0.3)
    visualizations.append(save_plot_to_base64(plt, 'Previous Purchases vs Purchase Amount'))
    plt.close()
    
    # Visualization 9: Discount Usage by Category
    plt.figure(figsize=(12, 6))
    sns.countplot(data=df, x='Category', hue='Discount Applied', palette='Blues')
    plt.title('Discount Usage Across Product Categories')
    plt.xlabel('Product Category')
    plt.ylabel('Count')
    plt.xticks(rotation=45)
    plt.legend(title='Discount Applied')
    visualizations.append(save_plot_to_base64(plt, 'Discount Usage by Category'))
    plt.close()
    
    # Visualization 10: Purchase Amount by Frequency of Purchases (fixed palette warning)
    plt.figure(figsize=(12, 6))
    sns.boxplot(data=df, x='Frequency of Purchases', y='Purchase Amount (USD)', 
               hue='Frequency of Purchases', palette='viridis', legend=False)
    plt.title('Purchase Amount Distribution by Purchase Frequency')
    plt.xlabel('Frequency of Purchases')
    plt.ylabel('Purchase Amount (USD)')
    plt.xticks(rotation=45)
    visualizations.append(save_plot_to_base64(plt, 'Purchase Amount by Frequency'))
    plt.close()
    
    # Visualization 11: Item Size vs Purchase Amount (replaced swarmplot with stripplot)
    plt.figure(figsize=(10, 6))
    sns.stripplot(data=df, x='Size', y='Purchase Amount (USD)', 
                 hue='Size', palette='Set3', legend=False, size=4, jitter=True, alpha=0.7)
    plt.title('Purchase Amount by Item Size')
    plt.xlabel('Size')
    plt.ylabel('Purchase Amount (USD)')
    visualizations.append(save_plot_to_base64(plt, 'Size vs Purchase Amount'))
    plt.close()
    
    # Visualization 12: Review Rating Distribution by Shipping Type (fixed palette warning)
    plt.figure(figsize=(12, 6))
    sns.violinplot(data=df, x='Shipping Type', y='Review Rating', 
                  hue='Shipping Type', palette='rocket', legend=False)
    plt.title('Review Rating Distribution by Shipping Type')
    plt.xlabel('Shipping Type')
    plt.ylabel('Review Rating')
    plt.xticks(rotation=45)
    visualizations.append(save_plot_to_base64(plt, 'Rating by Shipping Type'))
    plt.close()
    
    # NEW Visualization 13: Age vs Purchase Amount with Color Mapped to Review Rating
    plt.figure(figsize=(10, 6))
    scatter = sns.scatterplot(data=df, x='Age', y='Purchase Amount (USD)', 
                              hue='Review Rating', palette='viridis', size='Previous Purchases',
                              sizes=(20, 200), alpha=0.7)
    plt.title('Age vs Purchase Amount (Colored by Review Rating)')
    plt.xlabel('Customer Age')
    plt.ylabel('Purchase Amount (USD)')
    plt.legend(title='Review Rating', bbox_to_anchor=(1.05, 1), loc='upper left')
    visualizations.append(save_plot_to_base64(plt, 'Age vs Purchase Amount by Rating'))
    plt.close()
    
    # NEW Visualization 14: Promo Code Usage by Purchase Frequency
    plt.figure(figsize=(10, 6))
    sns.countplot(data=df, x='Frequency of Purchases', hue='Promo Code Used', palette='Set2')
    plt.title('Promo Code Usage by Purchase Frequency')
    plt.xlabel('Purchase Frequency')
    plt.ylabel('Count')
    plt.legend(title='Promo Code Used')
    plt.xticks(rotation=45)
    visualizations.append(save_plot_to_base64(plt, 'Promo Code Usage by Frequency'))
    plt.close()
    
    # NEW Visualization 15: Preferred Payment Method vs Actual Payment Method
    plt.figure(figsize=(10, 8))
    payment_crosstab = pd.crosstab(df['Preferred Payment Method'], df['Payment Method'])
    sns.heatmap(payment_crosstab, annot=True, cmap='YlGnBu', fmt='d')
    plt.title('Preferred Payment Method vs Actual Payment Method Used')
    plt.xlabel('Payment Method Used')
    plt.ylabel('Preferred Payment Method')
    visualizations.append(save_plot_to_base64(plt, 'Payment Method Preference vs Usage'))
    plt.close()
    
    # NEW Visualization 16: Color Preferences by Gender
    plt.figure(figsize=(12, 6))
    # Get the top colors
    top_colors = df['Color'].value_counts().head(8).index
    # Filter data for those colors
    color_gender_df = df[df['Color'].isin(top_colors)]
    sns.countplot(data=color_gender_df, x='Color', hue='Gender', palette='Pastel1')
    plt.title('Top Color Preferences by Gender')
    plt.xlabel('Color')
    plt.ylabel('Count')
    plt.xticks(rotation=45)
    plt.legend(title='Gender')
    visualizations.append(save_plot_to_base64(plt, 'Color Preferences by Gender'))
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