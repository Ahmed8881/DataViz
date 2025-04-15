from flask import Flask, render_template, request, jsonify, send_file
import os
import io
import base64
import pandas as pd
# Set matplotlib to use non-interactive Agg backend before any other imports
import matplotlib

matplotlib.use('Agg')

from visualizations.matplotlib_visualizations import generate_matplotlib_visualizations
from visualizations.seaborn_visualizations import generate_seaborn_visualizations
from visualizations.pandas_visualizations import generate_pandas_visualizations
from visualizations.numpy_visualizations import generate_numpy_visualizations

app = Flask(__name__)
# ...existing code...


# Load dataset
def load_data():
    # Try to load from Kaggle first
    try:
         df = pd.read_csv('data/shopping_trends.csv')
     
    except:
        import kagglehub
        from kagglehub import KaggleDatasetAdapter
        df = kagglehub.load_dataset(
            KaggleDatasetAdapter.PANDAS,
            "bhadramohit/customer-shopping-latest-trends-dataset",
            "customer_shopping_trends.csv")
       
    return df

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/get_visualizations', methods=['POST'])
def get_visualizations():
    library = request.form.get('library')
    df = load_data()
    
    if library == 'matplotlib':
        results = generate_matplotlib_visualizations(df)
    elif library == 'seaborn':
        results = generate_seaborn_visualizations(df)
    elif library == 'pandas':
        results = generate_pandas_visualizations(df)
    elif library == 'plotly':
        results = generate_numpy_visualizations(df)
    else:
        return jsonify({'error': 'Invalid library selected'})
    
    return jsonify(results)

@app.route('/download_image', methods=['POST'])
def download_image():
    image_data = request.form.get('image_data')
    chart_title = request.form.get('chart_title', 'chart')
    
    # Remove the header part
    image_data = image_data.split(',')[1]
    
    # Decode the base64 image data
    image_bytes = base64.b64decode(image_data)
    
    # Create a BytesIO object to serve as a file-like object
    image_io = io.BytesIO(image_bytes)
    image_io.seek(0)
    
    # Send the image as a downloadable file
    return send_file(
        image_io,
        mimetype='image/png',
        as_attachment=True,
        download_name=f'{chart_title}.png'
    )

if __name__ == '__main__':
    app.run(debug=True)