import joblib
import numpy as np
from sklearn.naive_bayes import MultinomialNB
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
import string

def preprocess_text(text):
    """Simple preprocessing function"""
    text = text.lower()
    text = text.translate(str.maketrans('', '', string.punctuation))
    return text

def create_dummy_models():
    """Buat model dummy untuk sentiment analysis dengan setup yang sama"""
    
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
        'layanan prima dan berkualitas',
        'sangat senang dengan pelayanan',
        'petugas ramah dan informatif',
        'proses mudah dan tidak ribet',
        'fasilitas memadai dan nyaman',
        
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
        'layanan mengecewakan dan lambat',
        'tidak puas dengan pelayanan',
        'petugas kurang responsif',
        'proses rumit dan membingungkan',
        'fasilitas tidak memadai',
        
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
        'pelayanan sesuai standar',
        'layanan cukup memuaskan',
        'tidak ada yang istimewa',
        'petugas cukup membantu',
        'proses berjalan lancar',
        'fasilitas cukup memadai'
    ]
    
    labels = [
        # Positif (15)
        'positif', 'positif', 'positif', 'positif', 'positif',
        'positif', 'positif', 'positif', 'positif', 'positif',
        'positif', 'positif', 'positif', 'positif', 'positif',
        
        # Negatif (15)
        'negatif', 'negatif', 'negatif', 'negatif', 'negatif',
        'negatif', 'negatif', 'negatif', 'negatif', 'negatif',
        'negatif', 'negatif', 'negatif', 'negatif', 'negatif',
        
        # Netral (15)
        'netral', 'netral', 'netral', 'netral', 'netral',
        'netral', 'netral', 'netral', 'netral', 'netral',
        'netral', 'netral', 'netral', 'netral', 'netral'
    ]
    
    try:
        # Preprocess texts
        processed_texts = [preprocess_text(text) for text in texts]
        
        # Menyiapkan fitur (teks) dan label - sama seperti kode Anda
        X = processed_texts
        y = labels
        
        # Membagi data menjadi data latih dan data uji - sama seperti kode Anda
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
        
        # Mengubah teks menjadi fitur vektor menggunakan CountVectorizer - sama seperti kode Anda
        vectorizer = CountVectorizer()
        X_train_vect = vectorizer.fit_transform(X_train)
        X_test_vect = vectorizer.transform(X_test)
        
        # Inisialisasi model Naïve Bayes - sama seperti kode Anda
        model = MultinomialNB()
        
        # Melatih model - sama seperti kode Anda
        model.fit(X_train_vect, y_train)
        
        # Memprediksi data uji - sama seperti kode Anda
        y_pred = model.predict(X_test_vect)
        
        # Hitung akurasi
        accuracy = accuracy_score(y_test, y_pred)
        
        # Save model dan vectorizer
        joblib.dump(model, 'model.pkl')
        joblib.dump(vectorizer, 'vectorizer.pkl')
        
        print("✅ Model berhasil dibuat dengan setup yang sama!")
        print("📁 File tersimpan: model.pkl, vectorizer.pkl")
        print(f"🎯 Akurasi model: {accuracy:.1%}")
        
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
