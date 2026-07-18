"""
Loads the trained triage model once and exposes a simple predict function.
Keeping this separate from views.py means the model-loading logic
can be tested/reused independent of Django's request/response cycle.
"""
import os
import joblib
from django.conf import settings

MODEL_PATH = os.path.join(settings.BASE_DIR, 'ml_data', 'triage_model.joblib')
VECTORIZER_PATH = os.path.join(settings.BASE_DIR, 'ml_data', 'tfidf_vectorizer.joblib')

# Same mapping used during training — must match ml/train_triage_model.py
DISEASE_TO_DEPARTMENT = {
    'Psoriasis': 'Dermatologist',
    'Acne': 'Dermatologist',
    'Impetigo': 'Dermatologist',
    'Fungal infection': 'Dermatologist',
    'Varicose Veins': 'Cardiologist',
    'Hypertension': 'Cardiologist',
    'Typhoid': 'General Physician',
    'Malaria': 'General Physician',
    'Dengue': 'General Physician',
    'Common Cold': 'General Physician',
    'Chicken pox': 'General Physician',
    'Pneumonia': 'Pulmonologist',
    'Bronchial Asthma': 'Pulmonologist',
    'Dimorphic Hemorrhoids': 'Gastroenterologist',
    'peptic ulcer disease': 'Gastroenterologist',
    'gastroesophageal reflux disease': 'Gastroenterologist',
    'Jaundice': 'Gastroenterologist',
    'Arthritis': 'Orthopedic Surgeon',
    'Cervical spondylosis': 'Orthopedic Surgeon',
    'Migraine': 'Neurologist',
    'urinary tract infection': 'Urologist',
    'allergy': 'General Physician',
    'drug reaction': 'General Physician',
    'diabetes': 'Endocrinologist',
}

# Load once at import time (i.e. once when Django starts)
_model = joblib.load(MODEL_PATH)
_vectorizer = joblib.load(VECTORIZER_PATH)


def predict_disease(symptom_text: str) -> dict:
    """
    Takes free-text symptoms, returns predicted disease + department.
    """
    vec = _vectorizer.transform([symptom_text])
    predicted_disease = _model.predict(vec)[0]
    department = DISEASE_TO_DEPARTMENT.get(predicted_disease, 'General Physician')

    return {
        'disease': predicted_disease,
        'department': department,
    }