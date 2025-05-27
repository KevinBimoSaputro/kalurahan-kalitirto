import streamlit as st

# MUST be the first Streamlit command
st.set_page_config(
    page_title="Sistem Feedback Kelurahan Kalitirto",
    page_icon="📝",
    layout="wide",
    initial_sidebar_state="collapsed"
)

from datetime import datetime, date, time
import repository as repo
import utils as utils
import predict_text as predict
import auth

# Inisialisasi session state
if "admin_logged_in" not in st.session_state:
    st.session_state.admin_logged_in = False
if "show_admin_login" not in st.session_state:
    st.session_state.show_admin_login = False

# CSS untuk styling dengan background
st.markdown("""
<style>
    /* Background Image */
    .stApp {
        background: linear-gradient(rgba(255, 255, 255, 0.9), rgba(255, 255, 255, 0.9)), 
                    url('/images/kelurahan-bg.png');
        background-size: cover;
        background-position: center;
        background-attachment: fixed;
        background-repeat: no-repeat;
    }
    
    /* Alternative: Jika ingin background lebih subtle */
    .main-content {
        animation: fadeIn 0.8s ease-out;
        background: rgba(255, 255, 255, 0.95);
        border-radius: 15px;
        padding: 2rem;
        margin: 1rem;
        box-shadow: 0 10px 30px rgba(0, 0, 0, 0.1);
        backdrop-filter: blur(10px);
    }
    
    @keyframes fadeIn {
        from {
            opacity: 0;
            transform: translateY(20px);
        }
        to {
            opacity: 1;
            transform: translateY(0);
        }
    }
    
    .header-section {
        padding: 0.5rem 0;
        margin-bottom: 1.5rem;
        color: #2c3e50;
        text-align: center;
        background: rgba(255, 255, 255, 0.9);
        border-radius: 15px;
        padding: 2rem;
        box-shadow: 0 5px 15px rgba(0, 0, 0, 0.1);
    }
    
    .header-section h1 {
        font-size: 2.5rem;
        font-weight: 700;
        margin-bottom: 0.3rem;
        color: #2c3e50;
        text-shadow: 2px 2px 4px rgba(0, 0, 0, 0.1);
    }
    
    .header-section h2 {
        font-size: 1.8rem;
        font-weight: 500;
        margin-bottom: 1rem;
        color: #34495e;
    }
    
    .header-section hr {
        border: none;
        height: 2px;
        background: linear-gradient(90deg, transparent, #4facfe, transparent);
        margin: 1.5rem auto;
        width: 60%;
    }
    
    .header-section h3 {
        font-size: 1.6rem;
        font-weight: 600;
        margin-bottom: 0.8rem;
        color: #2c3e50;
        width: 100%;
        margin-left: 0;
        margin-right: 0;
        padding: 0;
        text-align: left;
    }
    
    .header-section .support-text {
        font-size: 1rem;
        color: #6c757d;
        line-height: 1.6;
        width: 100%;
        margin: 0;
        padding: 0;
        text-align: justify;
        margin-bottom: 1rem;
    }
    
    .admin-panel {
        background: linear-gradient(135deg, #4facfe 0%, #00f2fe 100%);
        padding: 1.5rem;
        border-radius: 15px;
        margin-bottom: 2rem;
        color: white;
        box-shadow: 0 10px 30px rgba(79, 172, 254, 0.3);
        backdrop-filter: blur(10px);
    }
    
    .status-card {
        background: rgba(248, 249, 250, 0.95);
        padding: 1rem;
        border-radius: 10px;
        border-left: 4px solid #28a745;
        margin-bottom: 1rem;
        backdrop-filter: blur(10px);
        box-shadow: 0 5px 15px rgba(0, 0, 0, 0.1);
    }
    
    /* Chat Input Styling */
    .stChatInput {
        background: rgba(255, 255, 255, 0.95);
        border-radius: 15px;
        backdrop-filter: blur(10px);
        box-shadow: 0 5px 15px rgba(0, 0, 0, 0.1);
    }
    
    /* Cards and containers */
    .stContainer {
        background: rgba(255, 255, 255, 0.9);
        border-radius: 15px;
        padding: 1rem;
        backdrop-filter: blur(10px);
    }
    
    /* Metrics styling */
    .stMetric {
        background: rgba(255, 255, 255, 0.9);
        padding: 1rem;
        border-radius: 10px;
        box-shadow: 0 5px 15px rgba(0, 0, 0, 0.1);
        backdrop-filter: blur(10px);
    }
    
    /* Hide Streamlit branding */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    
    /* Responsive design */
    @media (max-width: 768px) {
        .stApp {
            background-attachment: scroll;
        }
        
        .main-content {
            margin: 0.5rem;
            padding: 1rem;
        }
        
        .header-section {
            padding: 1rem;
        }
        
        .header-section h1 {
            font-size: 2rem;
            margin-bottom: 0.2rem;
        }
        
        .header-section h2 {
            font-size: 1.5rem;
            margin-bottom: 0.8rem;
        }
        
        .header-section hr {
            margin: 1rem auto;
        }
        
        .header-section h3 {
            font-size: 1.4rem;
            text-align: left;
            margin-bottom: 0.6rem;
        }
        
        .header-section .support-text {
            font-size: 0.95rem;
            text-align: center;
            margin-bottom: 0.8rem;
        }
    }
</style>
""", unsafe_allow_html=True)

# Check if models are available
try:
    model_available = predict.check_models_available()
except:
    model_available = False

if not model_available:
    # Enhanced model generation page
    st.markdown('<div class="main-content">', unsafe_allow_html=True)
    st.markdown("""
    <div style="text-align: center; padding: 3rem;">
        <h1>🤖 Setup Model Machine Learning</h1>
        <p style="font-size: 1.2rem; color: #666; margin: 2rem 0;">
            Sistem memerlukan model AI untuk analisis sentimen feedback.<br>
            Klik tombol di bawah untuk membuat model secara otomatis.
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        if st.button("🔧 Generate Models", key="generate_models", help="Klik untuk membuat model ML"):
            with st.spinner("🔄 Sedang membuat model ML... Mohon tunggu..."):
                try:
                    import create_models
                    success = create_models.create_dummy_models()
                    if success:
                        st.success("✅ Model berhasil dibuat! Aplikasi akan dimuat ulang...")
                        st.balloons()
                        # Clear cache and rerun
                        st.cache_resource.clear()
                        st.rerun()
                    else:
                        st.error("❌ Gagal membuat model. Silakan coba lagi.")
                except Exception as e:
                    st.error(f"❌ Error: {e}")
    
    st.markdown("""
    ---
    ### ℹ️ Informasi
    - **Proses ini hanya dilakukan sekali** saat pertama kali setup
    - **Model akan tersimpan otomatis** untuk penggunaan selanjutnya  
    - **Waktu proses**: sekitar 10-30 detik
    - **Tidak memerlukan internet** - semua proses lokal
    """)
    st.markdown('</div>', unsafe_allow_html=True)
    st.stop()

# Logika tampilan berdasarkan status
if st.session_state.show_admin_login and not auth.is_admin_logged_in():
    st.markdown('<div class="main-content">', unsafe_allow_html=True)
    # Tombol kembali di tengah atas dengan spacing yang lebih baik
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        if st.button("← Kembali ke Form Feedback", key="back_to_user", use_container_width=True):
            st.session_state.show_admin_login = False
            st.rerun()
    
    # Spacing antara tombol dan form
    st.markdown('<div style="height: 1rem;"></div>', unsafe_allow_html=True)
    
    # Form login admin tanpa column wrapper - langsung ke kiri
    auth.admin_login_form()
    st.markdown('</div>', unsafe_allow_html=True)

elif auth.is_admin_logged_in():
    # Dashboard Admin
    st.markdown('<div class="main-content">', unsafe_allow_html=True)
    
    # Header admin dengan tombol logout
    col1, col2 = st.columns([3, 1])
    with col1:
        st.markdown("""
        <div class="admin-panel">
            <h1>👨‍💼 Dashboard Admin</h1>
            <p>Selamat datang di panel administrasi sistem feedback Kelurahan Kalitirto</p>
        </div>
        """, unsafe_allow_html=True)

    with col2:
        if st.button("🚪 Logout", key="admin_logout_btn"):
            auth.admin_logout()
        if st.button("👤 Mode User", key="back_to_user_mode"):
            st.session_state.show_admin_login = False
            st.session_state.admin_logged_in = False
            st.rerun()
        if st.button("🔄 Clear Cache", key="clear_cache"):
            st.cache_resource.clear()
            st.cache_data.clear()
            st.success("✅ Cache cleared!")
            st.rerun()
    
    # Status Connection (Simple)
    connection_status = repo.get_connection_status()
    total_records = repo.get_total_records()
    
    if connection_status:
        st.markdown(f"""
        <div class="status-card">
            <strong>📊 Status Sistem</strong><br>
            ✅ Database terhubung | 📝 Total feedback: {total_records} data
        </div>
        """, unsafe_allow_html=True)
    else:
        st.error("❌ Database tidak terhubung. Periksa konfigurasi.")
    
    # Konten admin - Statistik dan Analytics
    markdown = utils.set_markdown()
    
    today = date.today()
    start_date, end_date = None, None

    col1, col2 = st.columns([2, 1])
    with col1:
        st.subheader("📊 Statistik Sentimen")
    with col2:
        filter_date = st.date_input("Pilih tanggal", value=(today, today), format="DD.MM.YYYY", label_visibility="collapsed")            

    if len(filter_date) > 1:
        start_date = datetime.combine(filter_date[0], time.min).isoformat()
        end_date = datetime.combine(filter_date[1], time.max).isoformat()
        range_days = (filter_date[1] - filter_date[0]).days
        if range_days > 30:
            st.warning("⚠️ Maksimal rentang waktu adalah 1 bulan.")
        elif start_date and end_date:
            try:
                positive = repo.get_count_by_prediction("positif", start_date, end_date)
                neutral = repo.get_count_by_prediction("netral", start_date, end_date)
                negative = repo.get_count_by_prediction("negatif", start_date, end_date)

                if positive + neutral + negative == 0:
                    st.warning("📭 Tidak ada data untuk periode ini.")
                    st.info(f"💡 **Tip:** Coba ubah rentang tanggal. Total data tersedia: {total_records} feedback")
                else:
                    utils.create_chart(positive, neutral, negative)

                    col1, col2, col3 = st.columns(3)
                    with col1:
                        st.metric(label="😊 Positif", value=positive, delta=None, help="Positive feedback")
                        st.markdown('<div class="stMetricValue-positif"></div>', unsafe_allow_html=True)
                    with col2:  
                        st.metric(label="😐 Netral", value=neutral, delta=None, help="Netral feedback")
                        st.markdown('<div class="stMetricValue-netral"></div>', unsafe_allow_html=True)
                    with col3:
                        st.metric(label="😞 Negatif", value=negative, delta=None, help="Negative feedback")
                        st.markdown('<div class="stMetricValue-negatif"></div>', unsafe_allow_html=True)

                    st.container(height=30, border=False)

                    feedback_history = repo.get_feedback_history(start_date, end_date)
                    if feedback_history:
                        data = utils.process_feedback_history(feedback_history)
                        st.subheader("📝 Riwayat Feedback")
                        st.dataframe(data, use_container_width=True, hide_index=True, height=400)
                    else:
                        st.info("📝 Belum ada riwayat feedback untuk periode ini.")
            except Exception as e:
                st.error(f"❌ Error loading statistics: {e}")
    
    st.markdown('</div>', unsafe_allow_html=True)

else:
    # Tampilan User Biasa - Form Feedback
    st.markdown('<div class="main-content">', unsafe_allow_html=True)
    
    # Header dengan background
    st.markdown("""
    <div class="header-section">
        <h1>📝 Form Kritik dan Saran</h1>
        <h2>Kelurahan Kalitirto</h2>
        <hr>
        <h3>💬 Berikan Kritik dan Saran Anda</h3>
        <p class="support-text">
            Kami menghargai setiap masukan Anda. Silakan tuliskan kritik, saran, atau masukan di bawah ini. 
            Feedback Anda sangat berharga untuk meningkatkan kualitas pelayanan kami.
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    with st.container():
        user_input = st.chat_input("💭 Ketik kritik dan saran Anda di sini...")
        if user_input:
            try:
                prediction = predict.predict(user_input).lower()
                data = {
                    "feedback": user_input,
                    "prediction": prediction,
                }
                success = repo.insert_data(data)
                if success:
                    st.success("✅ Terima kasih atas kritik dan saran Anda! Masukan Anda telah tersimpan.")
                    st.balloons()
                else:
                    st.error("❌ Gagal menyimpan feedback. Silakan coba lagi.")
            except Exception as e:
                st.error(f"Terjadi kesalahan: {e}")
                st.toast("❌ Terjadi kesalahan. Silakan coba lagi.")
    
    # Kontak dengan background
    st.markdown("""
    ---
    ### 📞 Kontak
    Jika ada pertanyaan mendesak, hubungi:
    - **Telepon**: (0274) 123-4567
    - **Email**: kelurahan.kalitirto@gmail.com
    - **Alamat**: Jl. Kalitirto No. 123, Yogyakarta
    """)
    
    # Tombol admin di pojok kanan bawah
    if st.button("👨‍💼 Mode Admin", key="admin_toggle", help="Klik untuk masuk ke dashboard admin"):
        st.session_state.show_admin_login = True
        st.rerun()
    
    st.markdown('</div>', unsafe_allow_html=True)
