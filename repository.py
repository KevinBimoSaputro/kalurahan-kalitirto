import connection as conn
import streamlit as st

def get_db():
    """Get database connection with error handling"""
    try:
        db = conn.load_database()
        if db is None:
            st.error("❌ Database not available")
            return None
        return db
    except Exception as e:
        st.error(f"❌ Database connection failed: {e}")
        return None

def insert_data(data):
    try:
        db = get_db()
        if db:
            result = db.insert(data).execute()
            st.write(f"✅ Data inserted: {result}")
            # Clear cache after insert
            get_count_by_prediction.clear()
            get_feedback_history.clear()
            return True
        else:
            st.error("Database connection not available")
            return False
    except Exception as e:
        st.error(f"Error inserting data: {e}")
        st.write(f"🔍 Full error: {str(e)}")
        return False

@st.cache_data
def get_count_by_prediction(prediction, start_date, end_date):
    try:
        db = get_db()
        if db:
            st.write(f"🔍 Querying count for {prediction} from {start_date} to {end_date}")
            
            data = db.select("*", count="exact") \
                .eq("prediction", prediction) \
                .gte("created_at", start_date) \
                .lte("created_at", end_date) \
                .limit(1) \
                .execute()
            
            st.write(f"✅ Count query successful for {prediction}: {data.count}")
            return data.count
        else:
            st.write(f"❌ No database connection for {prediction}")
            return 0
    except Exception as e:
        st.error(f"Error getting count for {prediction}: {e}")
        st.write(f"🔍 Full error: {str(e)}")
        return 0

@st.cache_data
def get_feedback_history(start_date, end_date):
    try:
        db = get_db()
        if db:
            st.write(f"🔍 Querying feedback history from {start_date} to {end_date}")
            
            data = db.select("feedback, prediction, created_at") \
                .gte("created_at", start_date) \
                .lte("created_at", end_date) \
                .order("created_at", desc=False) \
                .execute()
            
            st.write(f"✅ History query successful: {len(data.data)} records")
            return data.data
        else:
            st.write("❌ No database connection for history")
            return []
    except Exception as e:
        st.error(f"Error getting feedback history: {e}")
        st.write(f"🔍 Full error: {str(e)}")
        return []
