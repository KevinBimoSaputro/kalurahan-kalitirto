# 📝 Sistem Feedback Kelurahan Kalitirto

Aplikasi web untuk mengumpulkan kritik dan saran dari masyarakat dengan analisis sentimen otomatis.

## ✨ Fitur

### 👥 **Mode User**
- Form feedback tanpa perlu login
- Input kritik dan saran langsung
- Feedback tersimpan otomatis ke database
- Interface yang user-friendly

### 👨‍💼 **Mode Admin**
- Login dengan password
- Dashboard statistik lengkap
- Analisis sentimen real-time
- Riwayat feedback dengan filter tanggal
- Visualisasi data dengan charts

## 🚀 **Instalasi**

### 1. **Clone Repository**
\`\`\`bash
git clone https://github.com/KevinBimoSaputro/feedback.git
cd feedback
\`\`\`

### 2. **Install Dependencies**
\`\`\`bash
pip install -r requirements.txt
\`\`\`

### 3. **Generate Model ML**
\`\`\`bash
python create_models.py
\`\`\`

### 4. **Setup Database**
- Buat akun di [Supabase](https://supabase.com)
- Buat tabel `mst_feedback` dengan struktur:
  \`\`\`sql
  CREATE TABLE mst_feedback (
      id SERIAL PRIMARY KEY,
      feedback TEXT NOT NULL,
      prediction TEXT NOT NULL,
      created_at TIMESTAMP DEFAULT NOW()
  );
  \`\`\`
- Update file `.streamlit/secrets.toml` dengan kredensial Anda

### 5. **Jalankan Aplikasi**
\`\`\`bash
streamlit run app.py
\`\`\`

## 🔐 **Kredensial Admin**

- **Password**: `admin123`

## 🌐 **Deploy ke Streamlit Cloud**

1. Push repository ke GitHub
2. Buka [share.streamlit.io](https://share.streamlit.io)
3. Connect repository
4. Set main file: `app.py`
5. Tambahkan secrets di dashboard
6. Deploy!

## 📊 **Struktur Database**

\`\`\`sql
CREATE TABLE mst_feedback (
    id SERIAL PRIMARY KEY,
    feedback TEXT NOT NULL,
    prediction TEXT NOT NULL,
    created_at TIMESTAMP DEFAULT NOW()
);
\`\`\`

## 🎯 **Cara Penggunaan**

### **User Biasa:**
1. Buka aplikasi
2. Ketik feedback di chat input
3. Tekan Enter - feedback tersimpan!

### **Admin:**
1. Klik "👨‍💼 Mode Admin"
2. Masukkan password: `admin123`
3. Lihat dashboard dan statistik

## 🛠️ **Development**

### **Struktur File:**
\`\`\`
feedback/
├── app.py              # Main application
├── auth.py             # Authentication system
├── connection.py       # Database connection
├── repository.py       # Database operations
├── utils.py            # Utility functions
├── predict_text.py     # ML prediction
├── create_models.py    # Generate ML models
├── requirements.txt    # Dependencies
├── .streamlit/
│   └── secrets.toml    # Configuration
└── README.md          # Documentation
\`\`\`

### **Menambah Fitur:**
1. Edit file yang sesuai
2. Test di local: `streamlit run app.py`
3. Push ke GitHub untuk auto-deploy

## 📞 **Kontak**

- **Email**: kelurahan.kalitirto@gmail.com
- **Telepon**: (0274) 123-4567
- **Alamat**: Jl. Kalitirto No. 123, Yogyakarta

## 📄 **License**

MIT License - bebas digunakan dan dimodifikasi.
