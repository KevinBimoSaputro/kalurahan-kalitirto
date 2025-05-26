import joblib
import numpy as np
from sklearn.naive_bayes import MultinomialNB
from sklearn.feature_extraction.text import CountVectorizer
import string

def preprocess_text(text):
    """Simple preprocessing function"""
    text = text.lower()
    text = text.translate(str.maketrans('', '', string.punctuation))
    return text

def create_dummy_models():
    """Buat model dummy untuk sentiment analysis"""
    
    # Data training yang lebih lengkap
    texts = [
        # Positif
        'pelayanan sangat bagus dan memuaskan sekali',
        'staff ramah dan profesional dalam melayani',
        'fasilitas lengkap dan bersih terawat',
        'proses cepat dan efisien tidak berbelit',
        'sangat puas dengan layanan yang diberikan',
        'terima kasih pelayanannya sangat baik',
        'petugas sangat membantu dan sabar',
        'ruangan nyaman dan bersih',
        'sistem sudah bagus dan modern',
        'pelayanan memuaskan dan cepat',
        
        # Negatif  
        'pelayanan buruk dan mengecewakan sekali',
        'staff tidak ramah dan lambat melayani',
        'fasilitas kotor dan tidak terawat dengan baik',
        'proses lama dan berbelit ribet',
        'sangat tidak puas dengan layanan ini',
        'pelayanan mengecewakan dan lambat',
        'petugas tidak membantu dan kasar',
        'ruangan kotor dan tidak nyaman',
        'sistem masih manual dan ribet',
        'pelayanan buruk dan tidak profesional',
        
        # Netral
        'pelayanan biasa saja tidak istimewa',
        'staff cukup baik dalam melayani',
        'fasilitas standar seperti biasanya',
        'proses normal tidak ada masalah',
        'tidak ada keluhan khusus untuk layanan',
        'pelayanan cukup memadai',
        'petugas biasa saja',
        'ruangan standar',
        'sistem berjalan normal',
        'pelayanan sesuai standar'
    ]
    
    labels = [
        # Positif (10)
        'positif', 'positif', 'positif', 'positif', 'positif',
        'positif', 'positif', 'positif', 'positif', 'positif',
        
        # Negatif (10)
        'negatif', 'negatif', 'negatif', 'negatif', 'negatif',
        'negatif', 'negatif', 'negatif', 'negatif', 'negatif',
        
        # Netral (10)
        'netral', 'netral', 'netral', 'netral', 'netral',
        'netral', 'netral', 'netral', 'netral', 'netral'
    ]
    
    try:
        # Preprocess texts
        processed_texts = [preprocess_text(text) for text in texts]
        
        # Buat dan train model
        vectorizer = CountVectorizer(max_features=1000, ngram_range=(1, 2))
        model = MultinomialNB(alpha=1.0)
        
        # Fit vectorizer dan model
        X = vectorizer.fit_transform(processed_texts)
        model.fit(X, labels)
        
        # Save model dan vectorizer
        joblib.dump(model, 'model.pkl')
        joblib.dump(vectorizer, 'vectorizer.pkl')
        
        print("✅ Model dummy berhasil dibuat!")
        print("📁 File tersimpan: model.pkl, vectorizer.pkl")
        
        # Test model
        test_texts = [
            "pelayanan sangat bagus",
            "pelayanan buruk sekali", 
            "pelayanan biasa saja"
        ]
        
        for test_text in test_texts:
            processed_test = preprocess_text(test_text)
            test_vector = vectorizer.transform([processed_test])
            prediction = model.predict(test_vector)
            print(f"🧪 Test: '{test_text}' -> {prediction[0]}")
            
        return True
        
    except Exception as e:
        print(f"❌ Error creating models: {e}")
        return False

if __name__ == "__main__":
    create_dummy_models()
