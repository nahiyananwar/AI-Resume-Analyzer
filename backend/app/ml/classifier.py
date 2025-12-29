"""
Resume Classifier Service
Loads trained model and provides classification functions
"""
import os
import joblib
from typing import Tuple
from .train_classifier import train_model, get_all_categories as _get_all_categories


# Path to the trained model
MODEL_PATH = os.path.join(os.path.dirname(__file__), 'resume_classifier.joblib')


def get_classifier():
    """Load or train the classifier model"""
    if os.path.exists(MODEL_PATH):
        return joblib.load(MODEL_PATH)
    else:
        # Train if model doesn't exist
        print("Model not found. Training new model...")
        return train_model()


# Load model at module import (singleton pattern)
_classifier = None


def classify_resume(text: str) -> Tuple[str, float]:
    """
    Classify a resume into a job category
    
    Args:
        text: Resume text content
        
    Returns:
        Tuple of (category, confidence)
    """
    global _classifier
    
    if _classifier is None:
        _classifier = get_classifier()
    
    # Get prediction
    prediction = _classifier.predict([text])[0]
    
    # Get confidence (probability of predicted class)
    probabilities = _classifier.predict_proba([text])[0]
    confidence = max(probabilities)
    
    return prediction, round(confidence, 2)


def get_experience_level(years: float) -> str:
    """
    Determine experience level based on years of experience
    
    Args:
        years: Total years of experience
        
    Returns:
        Experience level string: Junior, Mid, or Senior
    """
    if years < 2:
        return "Junior"
    elif years < 5:
        return "Mid"
    else:
        return "Senior"


def get_all_categories() -> list:
    """Get list of all classification categories from dataset"""
    return _get_all_categories()
