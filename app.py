import streamlit as st
import pandas as pd
import joblib
import matplotlib.pyplot as plt
from utils import preprocess_text  # pastikan utils.py berisi fungsi preprocess_text

# Load model dan vectorizer
model = joblib.load("model.pkl")
vectorizer = joblib.load("vectorizer.pkl")

st.set_page_config(page_title="Analisis Sentimen Kalurahan Kalitirto", layout="centered")
st.title("📊 Aplikasi Analisis Sentimen Kalurahan Kalitirto")

st.markdown("""
Silakan unggah file `.csv` berisi kolom **`teks`** yang akan dianalisis.
""")

# Upload file
uploaded_file = st.file_uploader("Unggah file CSV", type=["csv"])

if uploaded_file is not None:
    try:
        df = pd.read_csv(uploaded_file)
        if 'teks' not in df.columns:
            st.error("❌ Kolom 'teks' tidak ditemukan dalam file CSV.")
        else:
            st.success("✅ File berhasil dimuat!")

            # Preprocessing teks
            df['teks_preprocessed'] = df['teks'].apply(preprocess_text)

            # Vektorisasi dan prediksi
            X_vect = vectorizer.transform(df['teks_preprocessed'])
            df['prediksi_sentimen'] = model.predict(X_vect)

            # Tampilkan hasil
            st.subheader("📄 Hasil Analisis Sentimen")
            st.dataframe(df[['teks', 'prediksi_sentimen']])

            # Visualisasi Pie Chart
            st.subheader("📊 Visualisasi Sentimen")
            counts = df['prediksi_sentimen'].value_counts()
            colors = ['#99ff99', '#FFFF00', '#ff9999']  # Positif, Netral, Negatif
            plt.figure(figsize=(5, 5))
            plt.pie(counts, labels=counts.index, autopct='%1.1f%%', colors=colors, startangle=90)
            plt.title('Distribusi Sentimen')
            st.pyplot(plt)

            # Tombol download
            st.download_button("📥 Unduh Hasil CSV", df.to_csv(index=False).encode(), "hasil_analisis.csv", "text/csv")

    except Exception as e:
        st.error(f"Terjadi kesalahan: {e}")
else:
    st.info("📌 Belum ada file yang diunggah.")
