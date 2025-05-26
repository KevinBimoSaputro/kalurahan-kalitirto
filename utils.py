import streamlit as st

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
