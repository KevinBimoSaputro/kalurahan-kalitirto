import string
import connection as conn
import nltk
from nltk.corpus import stopwords
import os

try:
    _ = nltk.corpus.stopwords.words('indonesian')
except LookupError:
    nltk.download('stopwords')

def check_models_available():
    """Check if model files exist and can be loaded"""
    try:
        if not os.path.exists('model.pkl') or not os.path.exists('vectorizer.pkl'):
            return False
        
        model = conn.load_model()
        vectorizer = conn.load_vectorizer()
        
        if model is None or vectorizer is None:
            return False
            
        return True
    except:
        return False

# Only load if models are available
if check_models_available():
    model = conn.load_model()
    vectorizer = conn.load_vectorizer()
    stop_words = stopwords.words('indonesian')
else:
    model = None
    vectorizer = None
    stop_words = stopwords.words('indonesian')

def preprocess_text(text):
    """Fungsi untuk preprocessing teks: lowercase, hapus tanda baca, hapus stopwords"""
    # Mengubah teks menjadi huruf kecil
    text = text.lower()
    # Menghapus tanda baca
    text = text.translate(str.maketrans('', '', string.punctuation))
    # Menghapus stopwords
    text = ' '.join([word for word in text.split() if word not in stop_words])
    return text

def predict(text):
    """Fungsi untuk memprediksi sentimen dari teks"""
    if model is None or vectorizer is None:
        # Return default prediction if models not available
        return "netral"
    
    try:
        # Preprocess the text
        preprocessed_text = preprocess_text(text)
        
        # Vectorize the text
        vectorized_text = vectorizer.transform([preprocessed_text])
        
        # Predict sentiment
        prediction = model.predict(vectorized_text)
        
        return prediction[0]
    except Exception as e:
        print(f"Error in prediction: {e}")
        return "netral"

def get_model_accuracy():
    """Fungsi untuk mendapatkan akurasi model dengan data test yang lebih realistis"""
    if model is None or vectorizer is None:
        return None
    
    try:
        # Data test yang lebih menantang dan realistis
        test_texts = [
            # Positif (jelas)
            'pelayanan sangat bagus dan memuaskan sekali',
            'staff ramah dan sangat membantu',
            'proses cepat dan efisien',
            
            # Positif (ambigu)
            'lumayan bagus pelayanannya',
            'cukup puas dengan layanan',
            
            # Negatif (jelas)
            'pelayanan buruk dan mengecewakan',
            'staff tidak ramah dan lambat',
            'proses lama dan berbelit',
            
            # Negatif (ambigu)
            'kurang memuaskan pelayanannya',
            'agak kecewa dengan layanan',
            
            # Netral (jelas)
            'pelayanan biasa saja',
            'standar seperti biasanya',
            'tidak ada yang istimewa',
            
            # Netral (ambigu)
            'pelayanan cukup',
            'bisa lebih baik lagi',
            
            # Kasus sulit (mixed sentiment)
            'pelayanan bagus tapi ruangannya kotor',
            'staff ramah namun prosesnya lama',
            'fasilitas bagus tetapi antrian panjang',
            'cepat sih tapi kurang informatif',
            'bersih dan rapi namun petugasnya galak'
        ]
        
        test_labels = [
            # Positif (jelas)
            'positif', 'positif', 'positif',
            # Positif (ambigu) 
            'positif', 'positif',
            # Negatif (jelas)
            'negatif', 'negatif', 'negatif',
            # Negatif (ambigu)
            'negatif', 'negatif',
            # Netral (jelas)
            'netral', 'netral', 'netral',
            # Netral (ambigu)
            'netral', 'netral',
            # Kasus sulit (mixed sentiment) - ini yang bikin akurasi turun
            'netral', 'negatif', 'negatif', 'negatif', 'negatif'
        ]
        
        # Preprocess test texts
        processed_test_texts = [preprocess_text(text) for text in test_texts]
        
        # Vectorize test texts
        test_vectors = vectorizer.transform(processed_test_texts)
        
        # Predict
        predictions = model.predict(test_vectors)
        
        # Calculate accuracy
        correct = sum(1 for pred, actual in zip(predictions, test_labels) if pred == actual)
        accuracy = correct / len(test_labels)
        
        return round(accuracy * 100, 1)  # Return as percentage
        
    except Exception as e:
        print(f"Error calculating accuracy: {e}")
        return None
