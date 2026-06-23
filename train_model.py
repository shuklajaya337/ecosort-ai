import pandas as pd
import pickle
import os
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn.pipeline import make_pipeline

def train_model():
    print("Training EcoSort AI waste classifier...")
    
    # Check if dataset exists
    dataset_path = 'dataset.csv'
    if not os.path.exists(dataset_path):
        print(f"Error: {dataset_path} not found. Please run this in the correct folder.")
        return

    # Load dataset
    df = pd.read_csv(dataset_path)
    
    # Ensure no empty values
    df['Item'] = df['Item'].fillna('').str.lower()
    df['Category'] = df['Category'].fillna('Organic Waste')

    # Features and labels
    X = df['Item']
    y = df['Category']

    # Create a pipeline with TF-IDF Vectorizer and Multinomial Naive Bayes.
    # We use char_wb analyzer with ngram range (2, 5) to robustly capture
    # word fragments and minor typos / plural forms (e.g. 'apples' matching 'apple').
    model = make_pipeline(
        TfidfVectorizer(analyzer='char_wb', ngram_range=(2, 5), lowercase=True),
        MultinomialNB(alpha=0.1)
    )

    # Train model
    model.fit(X, y)
    print("Model trained successfully.")

    # Save model and mapping details
    with open('classifier_model.pkl', 'wb') as f:
        pickle.dump(model, f)
    
    print("Saved classifier_model.pkl")

if __name__ == '__main__':
    train_model()
