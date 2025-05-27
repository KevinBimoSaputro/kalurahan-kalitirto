import streamlit as st
import pandas as pd
import pytz
import plotly.express as px
from datetime import datetime, date, time
import repository as repo
from io import BytesIO
from reportlab.lib.pagesizes import A4
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER, TA_LEFT

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
        /* Colored box styling for metrics */
        .stMetric {
            background: transparent !important;
            padding: 0 !important;
        }
        
        .metric-box-positif {
            background: linear-gradient(135deg, #28a745, #20c997);
            color: white !important;
            border-radius: 15px;
            padding: 1.5rem;
            text-align: center;
            box-shadow: 0 4px 15px rgba(40, 167, 69, 0.3);
            transition: transform 0.3s ease;
            margin-bottom: 1rem;
        }
        .metric-box-positif:hover {
            transform: translateY(-3px);
            box-shadow: 0 6px 20px rgba(40, 167, 69, 0.4);
        }
        
        .metric-box-negatif {
            background: linear-gradient(135deg, #dc3545, #e74c3c);
            color: white !important;
            border-radius: 15px;
            padding: 1.5rem;
            text-align: center;
            box-shadow: 0 4px 15px rgba(220, 53, 69, 0.3);
            transition: transform 0.3s ease;
            margin-bottom: 1rem;
        }
        .metric-box-negatif:hover {
            transform: translateY(-3px);
            box-shadow: 0 6px 20px rgba(220, 53, 69, 0.4);
        }
        
        .metric-box-netral {
            background: linear-gradient(135deg, #ffc107, #f39c12);
            color: white !important;
            border-radius: 15px;
            padding: 1.5rem;
            text-align: center;
            box-shadow: 0 4px 15px rgba(255, 193, 7, 0.3);
            transition: transform 0.3s ease;
            margin-bottom: 1rem;
        }
        .metric-box-netral:hover {
            transform: translateY(-3px);
            box-shadow: 0 6px 20px rgba(255, 193, 7, 0.4);
        }
        
        .metric-box-total {
            background: linear-gradient(135deg, #6c757d, #5a6268);
            color: white !important;
            border-radius: 15px;
            padding: 1.5rem;
            text-align: center;
            box-shadow: 0 4px 15px rgba(108, 117, 125, 0.3);
            transition: transform 0.3s ease;
            margin-bottom: 1rem;
        }
        .metric-box-total:hover {
            transform: translateY(-3px);
            box-shadow: 0 6px 20px rgba(108, 117, 125, 0.4);
        }
        
        .metric-label {
            font-size: 1.1rem;
            font-weight: 600;
            margin-bottom: 0.5rem;
            color: white !important;
        }
        
        .metric-value {
            font-size: 2.5rem;
            font-weight: 700;
            color: white !important;
            margin: 0;
        }
        
        /* Hide default streamlit metric styling */
        .stMetric > div {
            background: transparent !important;
            border: none !important;
            padding: 0 !important;
        }
        
        .stMetric label {
            display: none !important;
        }
        
        .stMetric [data-testid="metric-container"] {
            background: transparent !important;
            border: none !important;
            padding: 0 !important;
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

def generate_pdf_report(start_date=None, end_date=None, positive=0, neutral=0, negative=0):
    """Generate PDF report of feedback statistics for selected date range"""
    try:
        # If no dates provided, use today
        if not start_date or not end_date:
            today = date.today()
            start_date = datetime.combine(today, time.min).isoformat()
            end_date = datetime.combine(today, time.max).isoformat()
        
        # Get feedback history for the selected period
        feedback_history = repo.get_feedback_history(start_date, end_date)
        total = positive + neutral + negative
        
        # Create PDF
        buffer = BytesIO()
        doc = SimpleDocTemplate(buffer, pagesize=A4)
        styles = getSampleStyleSheet()
        
        # Custom styles
        title_style = ParagraphStyle(
            'CustomTitle',
            parent=styles['Heading1'],
            fontSize=18,
            spaceAfter=30,
            alignment=TA_CENTER,
            textColor=colors.darkblue
        )
        
        heading_style = ParagraphStyle(
            'CustomHeading',
            parent=styles['Heading2'],
            fontSize=14,
            spaceAfter=12,
            textColor=colors.darkblue
        )
        
        # Story elements
        story = []
        
        # Title
        story.append(Paragraph("📊 LAPORAN STATISTIK SENTIMEN FEEDBACK", title_style))
        story.append(Paragraph("Kelurahan Kalitirto", styles['Normal']))
        story.append(Spacer(1, 20))
        
        # Date range info
        start_dt = datetime.fromisoformat(start_date.replace('Z', '+00:00'))
        end_dt = datetime.fromisoformat(end_date.replace('Z', '+00:00'))
        
        jakarta_tz = pytz.timezone('Asia/Jakarta')
        start_local = start_dt.astimezone(jakarta_tz)
        end_local = end_dt.astimezone(jakarta_tz)
        
        if start_local.date() == end_local.date():
            date_range = f"📅 Tanggal: {start_local.strftime('%d %B %Y')}"
        else:
            date_range = f"📅 Periode: {start_local.strftime('%d %B %Y')} - {end_local.strftime('%d %B %Y')}"
        
        story.append(Paragraph(date_range, styles['Normal']))
        story.append(Paragraph(f"🕒 Dibuat: {datetime.now().strftime('%d %B %Y, %H:%M WIB')}", styles['Normal']))
        story.append(Spacer(1, 20))
        
        # Summary statistics
        story.append(Paragraph("📈 RINGKASAN STATISTIK", heading_style))
        
        # Statistics table
        stats_data = [
            ['Kategori', 'Jumlah', 'Persentase'],
            ['😊 Positif', str(positive), f"{(positive/total*100):.1f}%" if total > 0 else "0%"],
            ['😐 Netral', str(neutral), f"{(neutral/total*100):.1f}%" if total > 0 else "0%"],
            ['😞 Negatif', str(negative), f"{(negative/total*100):.1f}%" if total > 0 else "0%"],
            ['📊 Total', str(total), "100%" if total > 0 else "0%"]
        ]
        
        stats_table = Table(stats_data, colWidths=[2*inch, 1*inch, 1*inch])
        stats_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 12),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
            ('GRID', (0, 0), (-1, -1), 1, colors.black)
        ]))
        
        story.append(stats_table)
        story.append(Spacer(1, 20))
        
        # Feedback history
        if feedback_history:
            story.append(Paragraph("📝 RIWAYAT FEEDBACK", heading_style))
            story.append(Paragraph(f"Menampilkan semua {len(feedback_history)} feedback dari periode yang dipilih", styles['Normal']))
            story.append(Spacer(1, 10))
            
            # Prepare feedback data for table
            feedback_data = [['No', 'Feedback', 'Sentimen', 'Tanggal']]
            
            for i, item in enumerate(feedback_history, 1):  # Show ALL items
                feedback_text = item['feedback'][:60] + "..." if len(item['feedback']) > 60 else item['feedback']
                created_at = pd.to_datetime(item['created_at']).astimezone(jakarta_tz).strftime('%d/%m/%Y %H:%M')
                
                feedback_data.append([
                    str(i),
                    feedback_text,
                    item['prediction'].title(),
                    created_at
                ])
            
            feedback_table = Table(feedback_data, colWidths=[0.4*inch, 3.5*inch, 0.8*inch, 1.3*inch])
            feedback_table.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
                ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
                ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                ('FONTSIZE', (0, 0), (-1, 0), 10),
                ('FONTSIZE', (0, 1), (-1, -1), 7),
                ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
                ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
                ('GRID', (0, 0), (-1, -1), 1, colors.black),
                ('VALIGN', (0, 0), (-1, -1), 'TOP')
            ]))
            
            story.append(feedback_table)
        else:
            story.append(Paragraph("📝 RIWAYAT FEEDBACK", heading_style))
            story.append(Paragraph("Tidak ada feedback untuk periode yang dipilih.", styles['Normal']))
        
        # Footer
        story.append(Spacer(1, 30))
        story.append(Paragraph("📍 Kelurahan Kalitirto", styles['Normal']))
        story.append(Paragraph("📞 (0274) 123-4567 | ✉️ kelurahan.kalitirto@gmail.com", styles['Normal']))
        story.append(Paragraph("🏠 Jl. Kalitirto No. 123, Yogyakarta", styles['Normal']))
        
        # Build PDF
        doc.build(story)
        buffer.seek(0)
        
        return buffer.getvalue()
        
    except Exception as e:
        st.error(f"Error generating PDF: {e}")
        return None
