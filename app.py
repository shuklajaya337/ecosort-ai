from flask import Flask, render_template, jsonify, request
import pandas as pd
import pickle
import os

app = Flask(__name__)

# Constants for waste categories mapping
CATEGORY_INFO = {
    'Organic Waste': {
        'Bin': 'Green Bin',
        'Recyclable': 'No',
        'Color': '#2ecc71',
        'Tips': 'Compost this item! Organic waste breaks down into nutrient-rich soil. Avoid putting plastics or metals here.'
    },
    'Plastic Waste': {
        'Bin': 'Blue Bin',
        'Recyclable': 'Yes',
        'Color': '#3498db',
        'Tips': 'Rinse containers to remove food residue. Check local codes, but most rigid plastics are highly recyclable.'
    },
    'Paper Waste': {
        'Bin': 'Blue Bin',
        'Recyclable': 'Yes',
        'Color': '#f1c40f',
        'Tips': 'Ensure paper is clean and dry. Greasy items (like pizza boxes) or laminated paper cannot be recycled.'
    },
    'Glass Waste': {
        'Bin': 'Glass Bin / Blue Bin',
        'Recyclable': 'Yes',
        'Color': '#1abc9c',
        'Tips': 'Rinse glass jars and bottles. Do not mix window panes, drinking cups, or ceramics, as they melt at different temperatures.'
    },
    'Metal Waste': {
        'Bin': 'Blue Bin',
        'Recyclable': 'Yes',
        'Color': '#95a5a6',
        'Tips': 'Aluminum and tin cans are infinitely recyclable! Make sure to rinse food residue and compress them if possible.'
    },
    'Electronic Waste': {
        'Bin': 'E-Waste Drop-off',
        'Recyclable': 'Yes (Special)',
        'Color': '#9b59b6',
        'Tips': 'Do NOT put in regular trash. Take this to an electronics recycling center. Contains hazardous heavy metals and valuable materials.'
    },
    'Hazardous Waste': {
        'Bin': 'Hazardous Waste Depot',
        'Recyclable': 'No',
        'Color': '#e74c3c',
        'Tips': 'Warning! Paint, batteries, chemicals, and medical waste pose fire and toxicity hazards. Take them to local hazardous waste events.'
    }
}

# Global variables for dataset and classifier
df = None
model = None

def load_resources():
    global df, model
    # Load dataset
    dataset_path = 'dataset.csv'
    if os.path.exists(dataset_path):
        df = pd.read_csv(dataset_path)
        df['Item_Lower'] = df['Item'].str.lower()
    else:
        print(f"Warning: {dataset_path} not found.")

    # Load ML Model
    model_path = 'classifier_model.pkl'
    if os.path.exists(model_path):
        with open(model_path, 'rb') as f:
            model = pickle.load(f)
        print("Classifier model loaded successfully.")
    else:
        print("Warning: classifier_model.pkl not found. Running training script...")
        try:
            import train_model
            train_model.train_model()
            if os.path.exists(model_path):
                with open(model_path, 'rb') as f:
                    model = pickle.load(f)
                print("Model trained and loaded dynamically.")
        except Exception as e:
            print(f"Could not train model dynamically: {e}")

load_resources()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/autocomplete', methods=['GET'])
def autocomplete():
    query = request.args.get('q', '').strip().lower()
    if not query or df is None:
        return jsonify([])

    # Find matching items in dataset (starts with or contains query)
    matches = df[df['Item_Lower'].str.contains(query, na=False)].head(6)
    suggestions = matches['Item'].tolist()
    return jsonify(suggestions)

@app.route('/classify', methods=['POST'])
def classify():
    data = request.get_json() or {}
    item_name = data.get('item', '').strip()
    
    if not item_name:
        return jsonify({'error': 'Please enter a waste item.'}), 400

    item_lower = item_name.lower()
    result = None

    # 1. Check for exact match in dataset
    if df is not None:
        match_row = df[df['Item_Lower'] == item_lower]
        if not match_row.empty:
            row = match_row.iloc[0]
            cat = row['Category']
            bin_name = row['Bin']
            recyclable = row['Recyclable']
            info = CATEGORY_INFO.get(cat, {'Color': '#34495e', 'Tips': 'Dispose of responsibly according to local guidance.'})
            result = {
                'item': row['Item'],
                'category': cat,
                'bin': bin_name,
                'recyclable': recyclable,
                'color': info['Color'],
                'tips': info['Tips'],
                'method': 'Exact Match'
            }

    # 2. If no exact match, fallback to Machine Learning model prediction
    if result is None:
        if model is not None:
            try:
                predicted_cat = model.predict([item_lower])[0]
                info = CATEGORY_INFO.get(predicted_cat, {
                    'Bin': 'General Waste Bin',
                    'Recyclable': 'No',
                    'Color': '#34495e',
                    'Tips': 'Check local classification guidelines.'
                })
                result = {
                    'item': item_name,
                    'category': predicted_cat,
                    'bin': info['Bin'],
                    'recyclable': info['Recyclable'],
                    'color': info['Color'],
                    'tips': info['Tips'],
                    'method': 'AI Predicted'
                }
            except Exception as e:
                print(f"Prediction error: {e}")

    # 3. Ultimate fallback if model fails
    if result is None:
        result = {
            'item': item_name,
            'category': 'General Waste',
            'bin': 'General Waste Bin',
            'recyclable': 'No',
            'color': '#7f8c8d',
            'tips': 'Item could not be classified. Please consult local recycling authorities.',
            'method': 'Fallback'
        }

    return jsonify(result)

if __name__ == '__main__':
    app.run(debug=True, port=5000)
