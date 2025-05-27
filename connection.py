import streamlit as st
import joblib
from supabase import create_client
import os

@st.cache_resource 
def load_database():
    try:
        # Use the correct URL and key
        url = "https://gtxzselygjujqkhigggu.supabase.co"
        key = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6Imd0eHpzZWx5Z2p1anFraGlnZ2d1Iiwicm9sZSI6ImFub24iLCJpYXQiOjE3NDY4NDg2ODgsImV4cCI6MjA2MjQyNDY4OH0.WOfZ90ejJBDBtg14Z_5kV_at1nqcp2617jI6uQRRUV8"
        table = "mst_feedback"
        
        # Create client
        client = create_client(url, key)
        
        # Test connection with a simple query
        test_result = client.table(table).select("*").limit(1).execute()
        
        return client.table(table)
        
    except Exception as e:
        st.error(f"❌ Database connection error: {e}")
        return None

@st.cache_resource 
def load_model():
    try:
        if not os.path.exists('model.pkl'):
            return None
        return joblib.load('model.pkl')
    except Exception as e:
        print(f"Error loading model: {e}")
        return None

@st.cache_resource 
def load_vectorizer():
    try:
        if not os.path.exists('vectorizer.pkl'):
            return None
        return joblib.load('vectorizer.pkl')
    except Exception as e:
        print(f"Error loading vectorizer: {e}")
        return None
