"""
Trains a symptom-to-specialty triage classifier.

Pipeline: TF-IDF (text -> numeric features) -> Logistic Regression (classifier)

This model predicts a DISEASE from free-text symptom description,
then we map that disease to a medical DEPARTMENT using a fixed
lookup table below. The LLM (Groq) is only used later to explain
this prediction in natural language — it never makes the actual
classification decision. That separation is the whole point.
"""

import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report, accuracy_score
import joblib
import os

# ---- Paths ----
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_PATH = os.path.join(BASE_DIR, 'ml_data', 'Symptom2Disease.csv')
MODEL_OUTPUT_PATH = os.path.join(BASE_DIR, 'ml_data', 'triage_model.joblib')
VECTORIZER_OUTPUT_PATH = os.path.join(BASE_DIR, 'ml_data', 'tfidf_vectorizer.joblib')

# ---- Disease -> Department mapping ----
# This is domain knowledge we're encoding ourselves, not something
# the model learns. Editable/extensible as we add more diseases later.
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


def main():
    print("Loading dataset...")
    df = pd.read_csv(DATA_PATH)
    print(f"Loaded {len(df)} rows, {df['label'].nunique()} unique diseases.")

    # Sanity check: make sure every disease in the CSV has a department mapping
    missing = set(df['label'].unique()) - set(DISEASE_TO_DEPARTMENT.keys())
    if missing:
        raise ValueError(f"These diseases have no department mapping: {missing}")

    X = df['text']
    y = df['label']

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42, stratify=y
    )

    print("Vectorizing text with TF-IDF...")
    vectorizer = TfidfVectorizer(max_features=3000, ngram_range=(1, 2), stop_words='english')
    X_train_vec = vectorizer.fit_transform(X_train)
    X_test_vec = vectorizer.transform(X_test)

    print("Training Logistic Regression classifier...")
    model = LogisticRegression(max_iter=1000)
    model.fit(X_train_vec, y_train)

    y_pred = model.predict(X_test_vec)
    acc = accuracy_score(y_test, y_pred)
    print(f"\nTest accuracy: {acc:.2%}\n")
    print(classification_report(y_test, y_pred))

    # Save both the model and the vectorizer — we need both at inference time
    joblib.dump(model, MODEL_OUTPUT_PATH)
    joblib.dump(vectorizer, VECTORIZER_OUTPUT_PATH)
    print(f"Saved model to {MODEL_OUTPUT_PATH}")
    print(f"Saved vectorizer to {VECTORIZER_OUTPUT_PATH}")


if __name__ == '__main__':
    main()