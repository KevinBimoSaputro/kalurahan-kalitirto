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

def smart_truncate(text, max_length=60):
    """Smart text truncation that tries to break at word boundaries"""
    if len(text) <= max_length:
        return text
    
    # Find the last space within the limit
    truncated = text[:max_length]
    last_space = truncated.rfind(' ')
    
    if last_space > max_length * 0.7:  # If space is reasonably close to the end
        return text[:last_space] + "..."
    else:
        return text[:max_length-3] + "..."

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
        doc = SimpleDocTemplate(buffer, pagesize=A4, topMargin=1*inch, bottomMargin=1*inch)
        styles = getSampleStyleSheet()
        
        # Custom styles
        title_style = ParagraphStyle(
            'CustomTitle',
            parent=styles['Heading1'],
            fontSize=20,
            spaceAfter=20,
            alignment=TA_CENTER,
            textColor=colors.darkblue,
            fontName='Helvetica-Bold'
        )
        
        subtitle_style = ParagraphStyle(
            'CustomSubtitle',
            parent=styles['Normal'],
            fontSize=14,
            spaceAfter=30,
            alignment=TA_CENTER,
            textColor=colors.grey,
            fontName='Helvetica'
        )
        
        heading_style = ParagraphStyle(
            'CustomHeading',
            parent=styles['Heading2'],
            fontSize=16,
            spaceAfter=15,
            spaceBefore=20,
            textColor=colors.darkblue,
            fontName='Helvetica-Bold'
        )
        
        normal_style = ParagraphStyle(
            'CustomNormal',
            parent=styles['Normal'],
            fontSize=11,
            spaceAfter=10,
            fontName='Helvetica'
        )
        
        # Story elements
        story = []
        
        # Title
        story.append(Paragraph("LAPORAN STATISTIK SENTIMEN FEEDBACK", title_style))
        story.append(Paragraph("Kelurahan Kalitirto", subtitle_style))
        
        # Date range info
        start_dt = datetime.fromisoformat(start_date.replace('Z', '+00:00'))
        end_dt = datetime.fromisoformat(end_date.replace('Z', '+00:00'))
        
        jakarta_tz = pytz.timezone('Asia/Jakarta')
        start_local = start_dt.astimezone(jakarta_tz)
        end_local = end_dt.astimezone(jakarta_tz)
        
        if start_local.date() == end_local.date():
            date_range = f"Tanggal: {start_local.strftime('%d %B %Y')}"
        else:
            date_range = f"Periode: {start_local.strftime('%d %B %Y')} - {end_local.strftime('%d %B %Y')}"
        
        story.append(Paragraph(date_range, normal_style))
        story.append(Paragraph(f"Dibuat: {datetime.now().strftime('%d %B %Y, %H:%M WIB')}", normal_style))
        story.append(Spacer(1, 30))
        
        # Summary statistics
        story.append(Paragraph("RINGKASAN STATISTIK", heading_style))
        
        # Statistics table with better formatting
        stats_data = [
            ['Kategori', 'Jumlah', 'Persentase'],
            ['Positif', str(positive), f"{(positive/total*100):.1f}%" if total > 0 else "0%"],
            ['Netral', str(neutral), f"{(neutral/total*100):.1f}%" if total > 0 else "0%"],
            ['Negatif', str(negative), f"{(negative/total*100):.1f}%" if total > 0 else "0%"],
            ['TOTAL', str(total), "100%" if total > 0 else "0%"]
        ]
        
        stats_table = Table(stats_data, colWidths=[2.5*inch, 1.5*inch, 1.5*inch])
        stats_table.setStyle(TableStyle([
            # Header styling
            ('BACKGROUND', (0, 0), (-1, 0), colors.darkblue),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 12),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 15),
            ('TOPPADDING', (0, 0), (-1, 0), 15),
            
            # Data rows
            ('BACKGROUND', (0, 1), (-1, -2), colors.lightgrey),
            ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),
            ('FONTSIZE', (0, 1), (-1, -1), 11),
            ('TOPPADDING', (0, 1), (-1, -1), 8),
            ('BOTTOMPADDING', (0, 1), (-1, -1), 8),
            
            # Total row
            ('BACKGROUND', (0, -1), (-1, -1), colors.darkgrey),
            ('TEXTCOLOR', (0, -1), (-1, -1), colors.whitesmoke),
            ('FONTNAME', (0, -1), (-1, -1), 'Helvetica-Bold'),
            
            # Borders
            ('GRID', (0, 0), (-1, -1), 1, colors.black),
            ('LINEBELOW', (0, 0), (-1, 0), 2, colors.darkblue),
        ]))
        
        story.append(stats_table)
        story.append(Spacer(1, 30))
        
        # Feedback history
        if feedback_history:
            story.append(Paragraph("RIWAYAT FEEDBACK", heading_style))
            story.append(Paragraph(f"Menampilkan {min(len(feedback_history), 30)} feedback dari periode yang dipilih", normal_style))
            story.append(Spacer(1, 15))
            
            # Prepare feedback data for table with improved column widths
            feedback_data = [['No', 'Feedback', 'Sentimen', 'Tanggal']]
            
            for i, item in enumerate(feedback_history[:30], 1):  # Limit to 30 items for better formatting
                # Smart truncate feedback text
                feedback_text = smart_truncate(item['feedback'], 55)
                created_at = pd.to_datetime(item['created_at']).astimezone(jakarta_tz).strftime('%d/%m/%Y %H:%M')
                
                feedback_data.append([
                    str(i),
                    feedback_text,
                    item['prediction'].title(),
                    created_at
                ])
            
            # Improved column widths for better layout
            feedback_table = Table(feedback_data, colWidths=[0.4*inch, 3.2*inch, 0.8*inch, 1.2*inch])
            feedback_table.setStyle(TableStyle([
                # Header
                ('BACKGROUND', (0, 0), (-1, 0), colors.darkblue),
                ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                ('ALIGN', (0, 0), (0, -1), 'CENTER'),  # No column center
                ('ALIGN', (1, 0), (1, -1), 'LEFT'),    # Feedback column left
                ('ALIGN', (2, 0), (2, -1), 'CENTER'),  # Sentimen column center
                ('ALIGN', (3, 0), (3, -1), 'CENTER'),  # Date column center
                ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                ('FONTSIZE', (0, 0), (-1, 0), 9),      # Reduced header font size
                ('TOPPADDING', (0, 0), (-1, 0), 8),    # Reduced padding
                ('BOTTOMPADDING', (0, 0), (-1, 0), 8),
                ('LEFTPADDING', (0, 0), (-1, -1), 4),  # Consistent left padding
                ('RIGHTPADDING', (0, 0), (-1, -1), 4), # Consistent right padding
                
                # Data rows
                ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),
                ('FONTSIZE', (0, 1), (-1, -1), 8),     # Reduced data font size
                ('TOPPADDING', (0, 1), (-1, -1), 4),   # Reduced padding
                ('BOTTOMPADDING', (0, 1), (-1, -1), 4),
                ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
                
                # Borders
                ('GRID', (0, 0), (-1, -1), 0.5, colors.black),
                ('LINEBELOW', (0, 0), (-1, 0), 2, colors.darkblue),
                ('VALIGN', (0, 0), (-1, -1), 'TOP'),
                
                # Word wrap for feedback column
                ('WORDWRAP', (1, 1), (1, -1), True),
            ]))
            
            story.append(feedback_table)
        else:
            story.append(Paragraph("RIWAYAT FEEDBACK", heading_style))
            story.append(Paragraph("Tidak ada feedback untuk periode yang dipilih.", normal_style))
        
        # Footer
        story.append(Spacer(1, 40))
        story.append(Paragraph("KELURAHAN KALITIRTO", heading_style))
        story.append(Paragraph("Jalan Tanjungtirto, Kalitirto, Berbah, Sleman, 55573", normal_style))
        story.append(Paragraph("Telepon: (0274) 4986086", normal_style))
        story.append(Paragraph("Email: kalitirtokalurahan@gmail.com", normal_style))
        story.append(Paragraph("Website: www.kalitirtosid.slemankab.go.id", normal_style))
        
        # Build PDF
        doc.build(story)
        buffer.seek(0)
        
        return buffer.getvalue()
        
    except Exception as e:
        st.error(f"Error generating PDF: {e}")
        return None
