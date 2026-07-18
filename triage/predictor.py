"""
Loads the trained triage model once and exposes a simple predict function.
"""
import os
import joblib
from django.conf import settings

MODEL_PATH = os.path.join(settings.BASE_DIR, 'ml_data', 'triage_model.joblib')
VECTORIZER_PATH = os.path.join(settings.BASE_DIR, 'ml_data', 'tfidf_vectorizer.joblib')

# Below this probability, we treat the prediction as unreliable rather
# than confidently naming a disease the model isn't actually sure about.
# Tuned by comparing probability scores on clear vs. out-of-scope inputs.
CONFIDENCE_THRESHOLD = 0.08

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

_model = joblib.load(MODEL_PATH)
_vectorizer = joblib.load(VECTORIZER_PATH)


def predict_disease(symptom_text: str) -> dict:
    """
    Takes free-text symptoms, returns predicted disease + department,
    or a low-confidence flag if the input doesn't clearly match
    anything the model was trained on.
    """
    vec = _vectorizer.transform([symptom_text])
    probs = _model.predict_proba(vec)[0]
    top_score = max(probs)
    predicted_disease = _model.predict(vec)[0]

    if top_score < CONFIDENCE_THRESHOLD:
        return {
            'disease': None,
            'department': 'General Physician',
            'confident': False,
        }

    department = DISEASE_TO_DEPARTMENT.get(predicted_disease, 'General Physician')
    return {
        'disease': predicted_disease,
        'department': department,
        'confident': True,
    }