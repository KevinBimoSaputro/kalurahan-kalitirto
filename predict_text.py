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
