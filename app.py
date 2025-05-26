import streamlit as st
from datetime import datetime, date, time
import repository as repo
import utils as utils
import predict_text as predict
import auth

# Konfigurasi halaman
st.set_page_config(
    page_title="Sistem Feedback Kelurahan Kalitirto",
    page_icon="📝",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Inisialisasi session state
if "admin_logged_in" not in st.session_state:
    st.session_state.admin_logged_in = False
if "show_admin_login" not in st.session_state:
    st.session_state.show_admin_login = False

# CSS untuk styling
st.markdown("""
<style>
    .main-content {
        animation: fadeIn 0.8s ease-out;
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
    
    .header-container {
        background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
        padding: 2rem;
        border-radius: 15px;
        margin-bottom: 2rem;
        color: white;
        text-align: center;
        box-shadow: 0 10px 30px rgba(0, 0, 0, 0.1);
    }
    
    .user-feedback-container {
        background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
        padding: 2rem;
        border-radius: 15px;
        margin-bottom: 2rem;
        color: white;
        box-shadow: 0 10px 30px rgba(0, 0, 0, 0.1);
    }
    
    .admin-panel {
        background: linear-gradient(135deg, #4facfe 0%, #00f2fe 100%);
        padding: 1.5rem;
        border-radius: 15px;
        margin-bottom: 2rem;
        color: white;
        box-shadow: 0 10px 30px rgba(0, 0, 0, 0.1);
    }
    
    /* Hide Streamlit branding */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
</style>
""", unsafe_allow_html=True)

# Logika tampilan berdasarkan status
if st.session_state.show_admin_login and not auth.is_admin_logged_in():
    # Tampilkan form login admin
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        if st.button("← Kembali ke Form Feedback", key="back_to_user"):
            st.session_state.show_admin_login = False
            st.rerun()
    
    auth.admin_login_form()

elif auth.is_admin_logged_in():
    # Dashboard Admin
    st.markdown('<div class="main-content">', unsafe_allow_html=True)
    
    # Header admin dengan tombol logout
    col1, col2 = st.columns([4, 1])
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
                    st.warning("📭 Tidak ada data untuk tanggal ini.")
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
                st.error(f"Error loading statistics: {e}")
    
    st.markdown('</div>', unsafe_allow_html=True)

else:
    # Tampilan User Biasa - Form Feedback
    st.markdown('<div class="main-content">', unsafe_allow_html=True)
    
    # Header untuk user
    st.markdown("""
    <div class="header-container">
        <h1>📝 Form Kritik dan Saran</h1>
        <h2>Kelurahan Kalitirto</h2>
        <p style="font-size: 1.1rem; margin-top: 1rem;">
            Kami menghargai setiap masukan Anda untuk meningkatkan pelayanan kami
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    # Form feedback untuk user
    st.markdown("""
    <div class="user-feedback-container">
        <h2>💬 Berikan Kritik dan Saran Anda</h2>
        <p>Silakan tuliskan kritik, saran, atau masukan Anda di bawah ini. 
        Feedback Anda sangat berharga untuk meningkatkan kualitas pelayanan kami.</p>
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
    
    # Informasi tambahan
    st.markdown("""
    ---
    ### 📋 Informasi
    - **Feedback Anda anonim** - Tidak perlu login atau registrasi
    - **Semua masukan dihargai** - Baik kritik maupun saran konstruktif
    - **Respon cepat** - Tim kami akan menindaklanjuti feedback Anda
    
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
