import string
import nltk
from nltk.corpus import stopwords

# Unduh stopwords bahasa Indonesia (hanya sekali di awal)
nltk.download('stopwords')
stop_words = set(stopwords.words('indonesian'))

def preprocess_text(text):
    """
    Fungsi untuk preprocessing teks:
    - Lowercase
    - Hapus tanda baca
    - Hapus stopwords
    """
    if not isinstance(text, str):
        return ""

    # Lowercase
    text = text.lower()

    # Hapus tanda baca
    text = text.translate(str.maketrans('', '', string.punctuation))

    # Tokenisasi dan hapus stopwords
    text = ' '.join([word for word in text.split() if word not in stop_words])

    return text
