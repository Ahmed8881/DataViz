import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px
import io
import base64

def plot_age_distribution(df, library='matplotlib'):
    if library == 'matplotlib':
        plt.figure(figsize=(10, 6))
        plt.hist(df['Age'], bins=20, color='skyblue', edgecolor='black')
        plt.title('Age Distribution of Customers')
        plt.xlabel('Age')
        plt.ylabel('Count')
        return get_matplotlib_image(plt)
    
    elif library == 'seaborn':
        plt.figure(figsize=(10, 6))
        sns.histplot(data=df, x='Age', kde=True, color='skyblue')
        plt.title('Age Distribution of Customers')
        return get_matplotlib_image(plt)
    
    elif library == 'plotly':
        fig = px.histogram(df, x='Age', nbins=20, title='Age Distribution of Customers')
        return get_plotly_image(fig)

def plot_purchase_by_category(df, library='matplotlib'):
    category_purchase = df.groupby('Category')['Purchase Amount (USD)'].sum().reset_index()
    
    if library == 'matplotlib':
        plt.figure(figsize=(10, 6))
        plt.bar(category_purchase['Category'], category_purchase['Purchase Amount (USD)'], color='lightgreen')
        plt.title('Total Purchase Amount by Category')
        plt.xlabel('Category')
        plt.ylabel('Total Purchase Amount (USD)')
        plt.xticks(rotation=45)
        return get_matplotlib_image(plt)
    
    elif library == 'seaborn':
        plt.figure(figsize=(10, 6))
        sns.barplot(data=category_purchase, x='Category', y='Purchase Amount (USD)', palette='viridis')
        plt.title('Total Purchase Amount by Category')
        plt.xticks(rotation=45)
        return get_matplotlib_image(plt)
    
    elif library == 'plotly':
        fig = px.bar(category_purchase, x='Category', y='Purchase Amount (USD)', 
                     title='Total Purchase Amount by Category')
        return get_plotly_image(fig)

def plot_gender_distribution(df, library='matplotlib'):
    gender_counts = df['Gender'].value_counts()
    
    if library == 'matplotlib':
        plt.figure(figsize=(8, 8))
        plt.pie(gender_counts, labels=gender_counts.index, autopct='%1.1f%%', colors=['lightcoral', 'lightskyblue'])
        plt.title('Gender Distribution')
        return get_matplotlib_image(plt)
    
    elif library == 'seaborn':
        plt.figure(figsize=(8, 8))
        plt.pie(gender_counts, labels=gender_counts.index, autopct='%1.1f%%', colors=['lightcoral', 'lightskyblue'])
        plt.title('Gender Distribution')
        return get_matplotlib_image(plt)
    
    elif library == 'plotly':
        fig = px.pie(gender_counts, values=gender_counts.values, names=gender_counts.index, 
                     title='Gender Distribution')
        return get_plotly_image(fig)

def plot_seasonal_trends(df, library='matplotlib'):
    seasonal_purchase = df.groupby('Season')['Purchase Amount (USD)'].sum().reset_index()
    
    if library == 'matplotlib':
        plt.figure(figsize=(10, 6))
        plt.plot(seasonal_purchase['Season'], seasonal_purchase['Purchase Amount (USD)'], marker='o', color='orange')
        plt.title('Seasonal Purchase Trends')
        plt.xlabel('Season')
        plt.ylabel('Total Purchase Amount (USD)')
        return get_matplotlib_image(plt)
    
    elif library == 'seaborn':
        plt.figure(figsize=(10, 6))
        sns.lineplot(data=seasonal_purchase, x='Season', y='Purchase Amount (USD)', marker='o', color='orange')
        plt.title('Seasonal Purchase Trends')
        return get_matplotlib_image(plt)
    
    elif library == 'plotly':
        fig = px.line(seasonal_purchase, x='Season', y='Purchase Amount (USD)', 
                      title='Seasonal Purchase Trends', markers=True)
        return get_plotly_image(fig)

def plot_payment_methods(df, library='matplotlib'):
    payment_counts = df['Payment Method'].value_counts()
    
    if library == 'matplotlib':
        plt.figure(figsize=(10, 6))
        payment_counts.plot(kind='bar', color='purple')
        plt.title('Payment Method Distribution')
        plt.xlabel('Payment Method')
        plt.ylabel('Count')
        plt.xticks(rotation=45)
        return get_matplotlib_image(plt)
    
    elif library == 'seaborn':
        plt.figure(figsize=(10, 6))
        sns.countplot(data=df, x='Payment Method', palette='magma')
        plt.title('Payment Method Distribution')
        plt.xticks(rotation=45)
        return get_matplotlib_image(plt)
    
    elif library == 'plotly':
        fig = px.bar(payment_counts, x=payment_counts.index, y=payment_counts.values, 
                     title='Payment Method Distribution')
        return get_plotly_image(fig)

def get_matplotlib_image(plt):
    img = io.BytesIO()
    plt.savefig(img, format='png', bbox_inches='tight')
    plt.close()
    img.seek(0)
    return base64.b64encode(img.getvalue()).decode('utf-8')

def get_plotly_image(fig):
    img_bytes = fig.to_image(format="png")
    return base64.b64encode(img_bytes).decode('utf-8')

def get_image_bytes(df, library, chart_type):
    if chart_type == 'age_distribution':
        img_data = plot_age_distribution(df, library)
    elif chart_type == 'purchase_by_category':
        img_data = plot_purchase_by_category(df, library)
    # Add other chart types...
    
    return base64.b64decode(img_data)