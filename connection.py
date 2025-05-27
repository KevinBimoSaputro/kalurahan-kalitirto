import streamlit as st
import joblib
from supabase import create_client
import os

@st.cache_resource 
def load_database():
    try:
        # Debug: Print what we're trying to connect to
        url = st.secrets["supabase"]["url"]
        key = st.secrets["supabase"]["key"]
        table = st.secrets["supabase"]["table"]
        
        st.write(f"🔍 Connecting to: {url}")
        st.write(f"🔍 Table: {table}")
        
        # Create client
        client = create_client(url, key)
        
        # Test connection with a simple query
        test_result = client.table(table).select("count", count="exact").limit(1).execute()
        st.write(f"✅ Connection test successful. Records: {test_result.count}")
        
        return client.table(table)
        
    except Exception as e:
        st.error(f"❌ Database connection error: {e}")
        st.write(f"🔍 Error type: {type(e)}")
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
