import streamlit as st
import pandas as pd
import pytz
import plotly.express as px

def process_feedback_history(data):
    df = pd.DataFrame(data)
    jakarta_tz = pytz.timezone('Asia/Jakarta')
    df['date'] = pd.to_datetime(df['created_at']).dt.tz_convert(jakarta_tz).dt.strftime('%Y-%m-%d %H:%M:%S')
    df.drop(columns=['created_at'], inplace=True)
    df.insert(0, 'no', range(1, len(df) + 1))
    return df

def set_markdown():
    return st.markdown("""
    <style>
        .stMetricValue-positif {
            background: linear-gradient(45deg, #28a745, #20c997);
            color: white;
            border-radius: 15px;
            padding: 10px;
            text-align: center;
            font-size: 20px;
            box-shadow: 0 4px 15px rgba(40, 167, 69, 0.3);
            transition: transform 0.3s ease;
        }
        .stMetricValue-positif:hover {
            transform: translateY(-2px);
        }
        .stMetricValue-negatif {
            background: linear-gradient(45deg, #dc3545, #e74c3c);
            color: white;
            border-radius: 15px;
            padding: 10px;
            text-align: center;
            font-size: 20px;
            box-shadow: 0 4px 15px rgba(220, 53, 69, 0.3);
            transition: transform 0.3s ease;
        }
        .stMetricValue-negatif:hover {
            transform: translateY(-2px);
        }
        .stMetricValue-netral {
            background: linear-gradient(45deg, #ffc107, #f39c12);
            color: white;
            border-radius: 15px;
            padding: 10px;
            text-align: center;
            font-size: 20px;
            box-shadow: 0 4px 15px rgba(255, 193, 7, 0.3);
            transition: transform 0.3s ease;
        }
        .stMetricValue-netral:hover {
            transform: translateY(-2px);
        }
        .stMetricLabel {
            font-size: 16px;
            font-weight: bold;
        }
        
        /* Animasi untuk dataframe */
        .stDataFrame {
            animation: fadeInUp 0.6s ease-out;
        }
        
        @keyframes fadeInUp {
            from {
                opacity: 0;
                transform: translateY(30px);
            }
            to {
                opacity: 1;
                transform: translateY(0);
            }
        }
    </style>
    """, unsafe_allow_html=True)

def create_chart(positive, neutral, negative):
    # Pastikan urutan dan nama yang konsisten
    labels = ['Positif', 'Netral', 'Negatif']
    values = [positive, neutral, negative]
    
    # Definisi warna yang konsisten dengan metric cards
    colors = ['#28a745', '#ffc107', '#dc3545']  # Hijau, Kuning, Merah
    
    fig = px.pie(
        values=values, 
        names=labels,
        color_discrete_sequence=colors  # Gunakan sequence untuk memastikan urutan
    )
    
    # Update layout untuk memastikan konsistensi
    fig.update_traces(
        textinfo='label+percent',
        insidetextorientation='auto',
        hoverinfo='skip',
        hovertemplate=None,
        marker=dict(
            colors=colors,  # Pastikan warna sesuai urutan
            line=dict(color='#FFFFFF', width=2)
        )
    )
    
    # Update layout
    fig.update_layout(
        showlegend=True,
        legend=dict(
            orientation="v",
            yanchor="middle",
            y=0.5,
            xanchor="left",
            x=1.01
        ),
        margin=dict(t=0, b=0, l=0, r=0)
    )
    
    st.plotly_chart(fig, use_container_width=True)
