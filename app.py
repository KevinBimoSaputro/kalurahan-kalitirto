import streamlit as st
from datetime import datetime, date, time
import repository as repo
import utils as utils
import predict_text as predict

# Initialize session state
if 'is_admin' not in st.session_state:
    st.session_state.is_admin = False
if 'show_login' not in st.session_state:
    st.session_state.show_login = False

markdown = utils.set_markdown()

# Admin login function
def admin_login():
    st.title("🔐 Login Admin")
    
    with st.form("login_form"):
        password = st.text_input("Password", type="password", placeholder="Masukkan password admin")
        submit_button = st.form_submit_button("Login")
        
        if submit_button:
            if password == "admin123":
                st.session_state.is_admin = True
                st.session_state.show_login = False
                st.success("Login berhasil! Redirecting...")
                st.rerun()
            else:
                st.error("Password salah!")
    
    if st.button("← Kembali ke Form Feedback"):
        st.session_state.show_login = False
        st.rerun()

# User feedback form
def user_feedback_form():
    st.title("📝 Form Kritik dan Saran")
    
    with st.container(border=False):
        st.write("Silakan isi form di bawah ini untuk memberikan kritik dan saran Anda. " \
        "Kami sangat menghargai masukan Anda untuk meningkatkan pelayanan kami. Terima kasih atas partisipasi Anda!")
        st.container(height=5, border=False)
        
        user_input = st.chat_input("Tulis kritik dan saran Anda di sini...")
        if user_input:
            st.toast("Terima kasih atas kritik dan saran Anda!")
            prediction = predict.predict(user_input).lower()
            data = {
                "feedback": user_input,
                "prediction": prediction,
            }
            repo.insert_data(data)
    
    st.divider()
    
    # Admin login button
    col1, col2, col3 = st.columns([1, 1, 1])
    with col2:
        if st.button("🔑 Login Admin", use_container_width=True):
            st.session_state.show_login = True
            st.rerun()

# Admin dashboard
def admin_dashboard():
    # Header with logout button
    col1, col2 = st.columns([3, 1])
    with col1:
        st.title("📊 Dashboard Admin - Kritik dan Saran")
    with col2:
        if st.button("🚪 Logout", use_container_width=True):
            st.session_state.is_admin = False
            st.session_state.show_login = False
            st.success("Logout berhasil!")
            st.rerun()
    
    # Feedback input section for admin
    st.subheader("📝 Input Feedback Baru")
    with st.container(border=True):
        user_input = st.chat_input("Admin juga bisa input feedback di sini...")
        if user_input:
            st.toast("Feedback berhasil ditambahkan!")
            prediction = predict.predict(user_input).lower()
            data = {
                "feedback": user_input,
                "prediction": prediction,
            }
            repo.insert_data(data)
    
    st.divider()
    
    # Statistics section
    today = date.today()
    start_date, end_date = None, None

    col1, col2 = st.columns([2, 1])
    with col1:
        st.subheader("📈 Statistik Sentimen")
    with col2:
        filter_date = st.date_input("Pilih tanggal", value=(today, today), format="DD.MM.YYYY", label_visibility="collapsed")            

    if len(filter_date) > 1:
        start_date = datetime.combine(filter_date[0], time.min).isoformat()
        end_date = datetime.combine(filter_date[1], time.max).isoformat()
        range_days = (filter_date[1] - filter_date[0]).days
        
        if range_days > 30:
            st.warning("⚠️ Maksimal rentang waktu adalah 1 bulan.")
        elif start_date and end_date:
            positive = repo.get_count_by_prediction("positif", start_date, end_date)
            neutral = repo.get_count_by_prediction("netral", start_date, end_date)
            negative = repo.get_count_by_prediction("negatif", start_date, end_date)

            if positive + neutral + negative == 0:
                st.warning("📭 Tidak ada data untuk tanggal ini.")
            else:
                utils.create_chart(positive, neutral, negative)

                col1, col2, col3 = st.columns(3)
                with col1:
                    st.metric(label="😊 Positif", value=positive, delta=None, help="Feedback positif")
                    st.markdown('<div class="stMetricValue-positif"></div>', unsafe_allow_html=True)
                with col2:  
                    st.metric(label="😐 Netral", value=neutral, delta=None, help="Feedback netral")
                    st.markdown('<div class="stMetricValue-netral"></div>', unsafe_allow_html=True)
                with col3:
                    st.metric(label="😞 Negatif", value=negative, delta=None, help="Feedback negatif")
                    st.markdown('<div class="stMetricValue-negatif"></div>', unsafe_allow_html=True)

                st.container(height=30, border=False)

                # Feedback history table
                st.subheader("📋 Riwayat Feedback")
                feedback_history = repo.get_feedback_history(start_date, end_date)
                data = utils.process_feedback_history(feedback_history)
                st.dataframe(data, use_container_width=True, hide_index=True, height=400)

# Main app logic
def main():
    # Show login form if requested
    if st.session_state.show_login and not st.session_state.is_admin:
        admin_login()
    # Show admin dashboard if logged in
    elif st.session_state.is_admin:
        admin_dashboard()
    # Show user feedback form by default
    else:
        user_feedback_form()

if __name__ == "__main__":
    main()
