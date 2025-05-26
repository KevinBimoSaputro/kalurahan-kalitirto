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
   """Form login admin sederhana"""
   
   st.subheader("🔐 Admin Login")
   st.write("Masuk untuk mengakses dashboard administrasi")
   
   # Form login
   with st.form("admin_login_form"):
       password = st.text_input("🔑 Password Admin", type="password", placeholder="Masukkan password admin")
       login_button = st.form_submit_button("🚀 Masuk")
       
       if login_button:
           if password:
               if verify_admin_password(password):
                   st.session_state.admin_logged_in = True
                   st.success("✅ Login berhasil!")
                   st.rerun()
               else:
                   st.error("❌ Password tidak valid!")
           else:
               st.warning("⚠️ Masukkan password!")
   
   st.info("💡 **Tip:** Hubungi administrator jika lupa password")

def admin_logout():
   """Fungsi untuk logout admin"""
   st.session_state.admin_logged_in = False
   st.success("👋 Logout berhasil!")
   st.rerun()

def is_admin_logged_in():
   """Cek apakah admin sudah login"""
   return st.session_state.get("admin_logged_in", False)
