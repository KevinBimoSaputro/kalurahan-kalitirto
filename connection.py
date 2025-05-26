import streamlit as st
import joblib
from supabase import create_client
import os

@st.cache_resource 
def load_database():
    try:
        url = st.secrets["supabase"]["url"]
        key = st.secrets["supabase"]["key"]
        client = create_client(url, key)
        table = st.secrets["supabase"]["table"]
        return client.table(table)
    except Exception as e:
        st.error(f"Error connecting to database: {e}")
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
