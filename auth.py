import streamlit as st
import hashlib

# Kredensial admin
ADMIN_CREDENTIALS = {
    "admin": "240be518fabd2724ddb6f04eeb1da5967448d7e831c08c8fa822809f74c720a9"  # password: admin123
}

def hash_password(password):
    """Hash password menggunakan SHA256"""
    return hashlib.sha256(password.encode()).hexdigest()

def verify_admin_password(password):
    """Verifikasi password admin"""
    return ADMIN_CREDENTIALS["admin"] == hash_password(password)

def admin_login_form():
    """Tampilkan form login admin dengan styling yang menarik"""
    
    # CSS untuk styling login form
    st.markdown("""
    <style>
        .admin-login-container {
            max-width: 350px;
            margin: 2rem auto;
            padding: 2rem;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            border-radius: 20px;
            box-shadow: 0 15px 35px rgba(0, 0, 0, 0.1);
            backdrop-filter: blur(10px);
            border: 1px solid rgba(255, 255, 255, 0.2);
        }
        
        .admin-login-title {
            text-align: center;
            color: white;
            font-size: 2rem;
            font-weight: bold;
            margin-bottom: 1.5rem;
            text-shadow: 2px 2px 4px rgba(0, 0, 0, 0.3);
        }
        
        .admin-login-subtitle {
            text-align: center;
            color: rgba(255, 255, 255, 0.8);
            font-size: 1rem;
            margin-bottom: 1.5rem;
        }
        
        .slide-in-admin {
            animation: slideInAdmin 0.6s ease-out;
        }
        
        @keyframes slideInAdmin {
            from {
                transform: translateY(-50px);
                opacity: 0;
            }
            to {
                transform: translateY(0);
                opacity: 1;
            }
        }
        
        .stTextInput > div > div > input {
            background: rgba(255, 255, 255, 0.1);
            border: 1px solid rgba(255, 255, 255, 0.3);
            border-radius: 10px;
            color: white;
            padding: 12px;
        }
        
        .stTextInput > div > div > input::placeholder {
            color: rgba(255, 255, 255, 0.7);
        }
        
        .stButton > button {
            background: linear-gradient(45deg, #ff6b6b, #ee5a24);
            color: white;
            border: none;
            border-radius: 25px;
            padding: 12px 30px;
            font-weight: bold;
            font-size: 1rem;
            width: 100%;
            transition: all 0.3s ease;
            box-shadow: 0 4px 15px rgba(238, 90, 36, 0.4);
        }
        
        .stButton > button:hover {
            transform: translateY(-2px);
            box-shadow: 0 6px 20px rgba(238, 90, 36, 0.6);
        }
    </style>
    """, unsafe_allow_html=True)
    
    # Container untuk form login admin
    st.markdown('<div class="admin-login-container slide-in-admin">', unsafe_allow_html=True)
    
    st.markdown('<h1 class="admin-login-title">🔐 Admin Login</h1>', unsafe_allow_html=True)
    st.markdown('<p class="admin-login-subtitle">Masuk untuk melihat statistik dan dashboard</p>', unsafe_allow_html=True)
    
    # Form login admin
    with st.form("admin_login_form"):
        password = st.text_input("🔑 Password Admin", type="password", placeholder="Masukkan password admin")
        
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            login_button = st.form_submit_button("🚀 Masuk")
        
        if login_button:
            if password:
                if verify_admin_password(password):
                    st.session_state.admin_logged_in = True
                    st.success("✅ Login admin berhasil!")
                    st.rerun()
                else:
                    st.error("❌ Password admin salah!")
            else:
                st.warning("⚠️ Mohon masukkan password admin!")
    
    st.markdown('</div>', unsafe_allow_html=True)

def admin_logout():
    """Fungsi untuk logout admin"""
    st.session_state.admin_logged_in = False
    st.rerun()

def is_admin_logged_in():
    """Cek apakah admin sudah login"""
    return st.session_state.get("admin_logged_in", False)
