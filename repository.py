import connection as conn
import streamlit as st

def get_db():
    """Get database connection with error handling"""
    try:
        db = conn.load_database()
        if db is None:
            return None
        return db
    except Exception as e:
        return None

def insert_data(data):
    try:
        db = get_db()
        if db:
            result = db.insert(data).execute()
            # Clear cache after insert
            get_count_by_prediction.clear()
            get_feedback_history.clear()
            return True
        else:
            return False
    except Exception as e:
        st.error(f"❌ Gagal menyimpan feedback: {e}")
        return False

@st.cache_data
def get_count_by_prediction(prediction, start_date, end_date):
    try:
        db = get_db()
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
        return 0

@st.cache_data
def get_feedback_history(start_date, end_date):
    try:
        db = get_db()
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
        return []

@st.cache_data
def get_total_records():
    """Get total number of records in database"""
    try:
        db = get_db()
        if db:
            data = db.select("*", count="exact").limit(1).execute()
            return data.count
        else:
            return 0
    except Exception as e:
        return 0

@st.cache_data  
def get_connection_status():
    """Check if database connection is working"""
    try:
        db = get_db()
        if db:
            # Test with a simple query
            test = db.select("*").limit(1).execute()
            return True
        else:
            return False
    except Exception as e:
        return False
