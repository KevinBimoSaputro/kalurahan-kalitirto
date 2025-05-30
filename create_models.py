import joblib
import numpy as np
import pandas as pd
from sklearn.naive_bayes import MultinomialNB
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, classification_report
import string
import nltk
from nltk.corpus import stopwords

def create_dummy_models():
    """Buat model sentiment analysis menggunakan metodologi yang sama dengan analisis Jupyter"""
    
    try:
        # Download stopwords jika belum ada
        try:
            nltk.download('stopwords')
            stop_words = set(stopwords.words('indonesian'))
        except:
            print("⚠️ Gagal mengunduh stopwords, menggunakan daftar minimal")
            # Daftar minimal stopwords bahasa Indonesia jika download gagal
            stop_words = {'yang', 'dan', 'di', 'dengan', 'untuk', 'pada', 'adalah', 'ini', 'dari', 'dalam'}
        
        # Fungsi preprocessing yang sama persis
        def preprocess_text(text):
            """Fungsi untuk preprocessing teks: lowercase, hapus tanda baca, hapus stopwords"""
            # Mengubah teks menjadi huruf kecil
            text = str(text).lower()
            # Menghapus tanda baca
            text = text.translate(str.maketrans('', '', string.punctuation))
            # Menghapus stopwords
            text = ' '.join([word for word in text.split() if word not in stop_words])
            return text
        
        # Membuat dataset simulasi yang mirip dengan dataset asli
        texts = [
            # Positif (rating 8-10)
            'Pelayanan di kelurahan cukup memuaskan, petugasnya ramah dan membantu',
            'Proses pengurusan KTP di kelurahan sangat cepat, tidak perlu menunggu lama',
            'Saya senang dengan pelayanan kelurahan yang selalu membantu pengurusan dokumen',
            'Pelayanan sangat baik dan petugas sangat ramah',
            'Fasilitas lengkap dan bersih, petugas juga informatif',
            'Proses cepat dan tidak berbelit-belit, sangat efisien',
            'Pelayanan prima, petugas kompeten dan ramah',
            'Sangat puas dengan layanan yang diberikan',
            'Pengurusan dokumen cepat dan mudah',
            'Petugas sangat membantu dan menjelaskan dengan detail',
            
            # Negatif (rating 1-4)
            'Ruang tunggu di kelurahan kurang nyaman, sering penuh dan panas',
            'Petugas kelurahan kurang responsif terhadap pertanyaan yang saya ajukan',
            'Pelayanan lambat dan berbelit-belit',
            'Petugas tidak ramah dan sering tidak ada di tempat',
            'Fasilitas kurang memadai dan kotor',
            'Proses pengurusan dokumen sangat lama',
            'Informasi yang diberikan tidak jelas dan membingungkan',
            'Antrian selalu panjang dan tidak teratur',
            'Pelayanan buruk dan mengecewakan',
            'Sistem sering error dan harus datang berkali-kali',
            
            # Netral (rating 5-7)
            'Pelayanan standar seperti kelurahan pada umumnya',
            'Waktu pelayanan cukup wajar, tidak terlalu cepat atau lambat',
            'Fasilitas cukup memadai meskipun ada beberapa yang perlu diperbaiki',
            'Petugas melayani dengan cukup baik',
            'Sistem pelayanan sudah terkomputerisasi tapi kadang lambat',
            'Ruang tunggu cukup nyaman tapi sering penuh',
            'Pelayanan biasa saja, tidak istimewa',
            'Proses pengurusan dokumen sesuai prosedur standar',
            'Petugas cukup membantu meskipun tidak selalu ramah',
            'Informasi yang diberikan cukup jelas'
        ]
        
        sentimen = [
            # Positif (10)
            'Positif', 'Positif', 'Positif', 'Positif', 'Positif',
            'Positif', 'Positif', 'Positif', 'Positif', 'Positif',
            
            # Negatif (10)
            'Negatif', 'Negatif', 'Negatif', 'Negatif', 'Negatif',
            'Negatif', 'Negatif', 'Negatif', 'Negatif', 'Negatif',
            
            # Netral (10)
            'Netral', 'Netral', 'Netral', 'Netral', 'Netral',
            'Netral', 'Netral', 'Netral', 'Netral', 'Netral'
        ]
        
        # Buat DataFrame seperti di notebook
        data = pd.DataFrame({'teks': texts, 'sentimen': sentimen})
        
        # Terapkan preprocessing ke dataset
        data['teks_preprocessed'] = data['teks'].apply(preprocess_text)
        
        # Menyiapkan fitur (teks) dan label - sama seperti kode Anda
        X = data['teks_preprocessed']
        y = data['sentimen']
        
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
        
        # Buat classification report
        report = classification_report(y_test, y_pred)
        
        # Save model dan vectorizer
        joblib.dump(model, 'model.pkl')
        joblib.dump(vectorizer, 'vectorizer.pkl')
        
        print("✅ Model berhasil dibuat dengan metodologi yang sama!")
        print("📁 File tersimpan: model.pkl, vectorizer.pkl")
        print(f"🎯 Akurasi model: {accuracy:.2%}")
        print("\n📊 Classification Report:")
        print(report)
        
        # Test model dengan beberapa contoh
        test_texts = [
            "Pelayanan sudah baik, tetap dipertahankan.",
            "Sarana prasarana perlu ditingkatkan, terutama ruang tunggu.",
            "Petugas sebaiknya lebih ramah dan mempercepat proses pelayanan.",
            "Layanan yang didapatkan sudah baik dan cepat.",
            "Harus banyak perbaikan, terutama dalam hal kecepatan dan keramahan petugas."
        ]
        
        print("\n🧪 Contoh Prediksi:")
        for test_text in test_texts:
            processed_test = preprocess_text(test_text)
            test_vector = vectorizer.transform([processed_test])
            prediction = model.predict(test_vector)
            print(f"'{test_text}' -> {prediction[0]}")
            
        # Simpan akurasi untuk ditampilkan di dashboard
        with open('model_accuracy.txt', 'w') as f:
            f.write(str(round(accuracy * 100, 1)))
            
        return True
        
    except Exception as e:
        print(f"❌ Error creating models: {e}")
        return False

if __name__ == "__main__":
    create_dummy_models()
