"""
Resume Classifier Training Script
Trains a TF-IDF + Logistic Regression model for resume classification
Uses the resume_dataset.csv for training data
"""
import joblib
import os
import re
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import Pipeline
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report


# Path to the dataset
DATASET_PATH = os.path.join(os.path.dirname(__file__), 'dataset', 'resume_dataset.csv')


def preprocess_text(text: str) -> str:
    """Clean and preprocess resume text"""
    if not isinstance(text, str):
        return ""
    
    # Remove extra whitespace
    text = re.sub(r'\s+', ' ', text)
    
    # Remove special characters but keep important punctuation
    text = re.sub(r'[^\w\s\-\.\,\@\/\+\#]', ' ', text)
    
    # Normalize whitespace
    text = ' '.join(text.split())
    
    return text.strip()


def load_dataset():
    """Load and prepare training data from CSV dataset"""
    print(f"Loading dataset from: {DATASET_PATH}")
    
    if not os.path.exists(DATASET_PATH):
        raise FileNotFoundError(f"Dataset not found at: {DATASET_PATH}")
    
    # Load CSV
    df = pd.read_csv(DATASET_PATH)
    
    print(f"Total samples loaded: {len(df)}")
    print(f"Columns: {df.columns.tolist()}")
    
    # Check for required columns
    if 'resume_text' not in df.columns or 'category' not in df.columns:
        raise ValueError("Dataset must have 'resume_text' and 'category' columns")
    
    # Clean text data
    df['resume_text'] = df['resume_text'].apply(preprocess_text)
    
    # Remove empty rows
    df = df[df['resume_text'].str.len() > 50]
    
    print(f"\nCategory distribution:")
    print(df['category'].value_counts())
    
    texts = df['resume_text'].tolist()
    labels = df['category'].tolist()
    
    return texts, labels


def get_all_categories():
    """Get list of all classification categories from dataset"""
    if os.path.exists(DATASET_PATH):
        df = pd.read_csv(DATASET_PATH)
        return sorted(df['category'].unique().tolist())
    return []


def train_model():
    """Train and save the resume classification model"""
    print("=" * 60)
    print("RESUME CLASSIFIER TRAINING")
    print("=" * 60)
    
    # Load data
    texts, labels = load_dataset()
    
    print(f"\nTotal samples: {len(texts)}")
    print(f"Categories: {len(set(labels))}")
    
    # Split data - 80% train, 20% test
    X_train, X_test, y_train, y_test = train_test_split(
        texts, labels, test_size=0.2, random_state=42, stratify=labels
    )
    
    print(f"\nTraining samples: {len(X_train)}")
    print(f"Test samples: {len(X_test)}")
    
    # Create pipeline with TF-IDF + Logistic Regression
    print("\n" + "-" * 40)
    print("Training model...")
    print("-" * 40)
    
    pipeline = Pipeline([
        ('tfidf', TfidfVectorizer(
            max_features=10000,  # Increased for larger dataset
            ngram_range=(1, 3),  # Include trigrams for better context
            stop_words='english',
            min_df=2,  # Minimum document frequency
            max_df=0.95,
            sublinear_tf=True  # Apply sublinear tf scaling
        )),
        ('clf', LogisticRegression(
            max_iter=2000,  # Increased for convergence
            class_weight='balanced',
            random_state=42,
            C=1.0,  # Regularization strength
            solver='lbfgs'
        ))
    ])
    
    # Train the model
    pipeline.fit(X_train, y_train)
    
    # Evaluate on test set
    print("\n" + "=" * 60)
    print("MODEL EVALUATION")
    print("=" * 60)
    
    y_pred = pipeline.predict(X_test)
    print("\nClassification Report:")
    print(classification_report(y_test, y_pred))
    
    # Calculate overall accuracy
    accuracy = (y_pred == y_test).mean()
    print(f"\nOverall Accuracy: {accuracy:.2%}")
    
    # Save model
    model_path = os.path.join(os.path.dirname(__file__), 'resume_classifier.joblib')
    joblib.dump(pipeline, model_path)
    print(f"\n✓ Model saved to: {model_path}")
    
    # Print categories the model can classify
    print("\nCategories the model can classify:")
    for i, cat in enumerate(sorted(set(labels)), 1):
        print(f"  {i}. {cat}")
    
    print("\n" + "=" * 60)
    print("TRAINING COMPLETE!")
    print("=" * 60)
    
    return pipeline


if __name__ == "__main__":
    train_model()
