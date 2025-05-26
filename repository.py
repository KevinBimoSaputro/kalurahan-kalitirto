import connection as conn
import streamlit as st

db = conn.load_database()

def insert_data(data):
    try:
        if db:
            db.insert(data).execute()
            get_count_by_prediction.clear()
            get_feedback_history.clear()
            return True
        else:
            st.error("Database connection not available")
            return False
    except Exception as e:
        st.error(f"Error inserting data: {e}")
        return False

@st.cache_data
def get_count_by_prediction(prediction, start_date, end_date):
    try:
        if db:
            data = db.select("*", count="exact") \
                .eq("prediction", prediction) \
                .gte("created_at", start_date) \
                .lte("created_at", end_date) \
                .limit(1) \
                .execute()
            return data.count
        else:
            return 0
    except Exception as e:
        st.error(f"Error getting count: {e}")
        return 0

@st.cache_data
def get_feedback_history(start_date, end_date):
    try:
        if db:
            data = db.select("feedback, prediction, created_at") \
                .gte("created_at", start_date) \
                .lte("created_at", end_date) \
                .order("created_at", desc=False) \
                .execute()
            return data.data
        else:
            return []
    except Exception as e:
        st.error(f"Error getting feedback history: {e}")
        return []
