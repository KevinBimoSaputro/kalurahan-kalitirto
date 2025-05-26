import joblib
import numpy as np
from sklearn.naive_bayes import MultinomialNB
from sklearn.feature_extraction.text import CountVectorizer

def create_dummy_models():
    """Buat model dummy untuk sentiment analysis"""
    
    # Data training dummy
    texts = [
        'pelayanan sangat bagus dan memuaskan',
        'staff ramah dan profesional',
        'fasilitas lengkap dan bersih',
        'proses cepat dan efisien',
        'sangat puas dengan layanan',
        'pelayanan buruk dan mengecewakan',
        'staff tidak ramah dan lambat',
        'fasilitas kotor dan tidak terawat',
        'proses lama dan berbelit',
        'sangat tidak puas',
        'pelayanan biasa saja',
        'staff cukup baik',
        'fasilitas standar',
        'proses normal',
        'tidak ada keluhan khusus'
    ]
    
    labels = [
        'positif', 'positif', 'positif', 'positif', 'positif',
        'negatif', 'negatif', 'negatif', 'negatif', 'negatif',
        'netral', 'netral', 'netral', 'netral', 'netral'
    ]
    
    # Buat dan train model
    vectorizer = CountVectorizer()
    model = MultinomialNB()
    
    # Fit vectorizer dan model
    X = vectorizer.fit_transform(texts)
    model.fit(X, labels)
    
    # Save model dan vectorizer
    joblib.dump(model, 'model.pkl')
    joblib.dump(vectorizer, 'vectorizer.pkl')
    
    print("✅ Model dummy berhasil dibuat!")
    print("📁 File tersimpan: model.pkl, vectorizer.pkl")
    
    # Test model
    test_text = "pelayanan sangat bagus"
    test_vector = vectorizer.transform([test_text])
    prediction = model.predict(test_vector)
    print(f"🧪 Test prediction: '{test_text}' -> {prediction[0]}")

if __name__ == "__main__":
    create_dummy_models()
