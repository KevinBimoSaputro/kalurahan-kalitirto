import pandas as pd
import streamlit as st
import pytz
import plotly.express as px

def process_feedback_history(data):
    df = pd.DataFrame(data)

    jakarta_tz = pytz.timezone('Asia/Jakarta')
    df['date'] = pd.to_datetime(df['created_at']).dt.tz_convert(jakarta_tz).dt.strftime('%Y-%m-%d %H:%M:%S')

    df.drop(columns=['created_at'], inplace=True)
    df.insert(0, 'no', range(1, len(df) + 1))
    
    # Rename columns for better display
    df.columns = ['No', 'Feedback', 'Sentimen', 'Tanggal']
    
    return df

def set_markdown():
    return st.markdown("""
    <style>
        .stMetricValue-positif {
            background-color: #28a745;
            color: white;
            border-radius: 10px;
            padding: 8px;
            text-align: center;
            font-size: 18px;
            font-weight: bold;
        }
        .stMetricValue-negatif {
            background-color: #dc3545;
            color: white;
            border-radius: 10px;
            padding: 8px;
            text-align: center;
            font-size: 18px;
            font-weight: bold;
        }
        .stMetricValue-netral {
            background-color: #ffc107;
            color: #212529;
            border-radius: 10px;
            padding: 8px;
            text-align: center;
            font-size: 18px;
            font-weight: bold;
        }
        .stMetricLabel {
            font-size: 16px;
            font-weight: bold;
        }
        
        /* Custom button styling */
        .stButton > button {
            border-radius: 8px;
            border: 1px solid #ddd;
            transition: all 0.3s ease;
        }
        
        .stButton > button:hover {
            transform: translateY(-2px);
            box-shadow: 0 4px 8px rgba(0,0,0,0.1);
        }
        
        /* Chat input styling */
        .stChatInput > div > div > textarea {
            border-radius: 20px;
        }
    </style>
    """, unsafe_allow_html=True)

def create_chart(positive, neutral, negative):
    labels = ['Positif', 'Netral', 'Negatif']
    values = [positive, neutral, negative]

    fig = px.pie(
        names=labels,
        values=values,
        color=['Positif', 'Netral', 'Negatif'],
        color_discrete_map={
            'Positif': '#28a745',
            'Netral': '#ffc107',
            'Negatif': '#dc3545'
        },
        title="Distribusi Sentimen Feedback"
    )

    fig.update_traces(
        textinfo='label+percent+value',
        insidetextorientation='auto',
        hoverinfo='label+percent+value',
        textfont_size=12
    )
    
    fig.update_layout(
        showlegend=True,
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=-0.2,
            xanchor="center",
            x=0.5
        ),
        margin=dict(t=50, b=50, l=50, r=50)
    )
    
    st.plotly_chart(fig, use_container_width=True)
