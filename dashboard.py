# =====================================================
# Funded 2026 - Interactive Dashboard
# Client: VC Advisory Partners LLP
# Analyst: Remsha Ansari
# Tech: Streamlit + Plotly
# =====================================================

import streamlit as st
import pandas as pd
import plotly.express as px
from io import BytesIO
from fpdf import FPDF
from docx import Document

# ==================== 1. PAGE CONFIG ====================
st.set_page_config(
    page_title="Funded 2026 | Remsha Ansari",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="collapsed" # Sidebar band by default
)

# ==================== 2. DARK/LIGHT MODE COMPATIBLE CSS ====================
st.markdown("""
<style>
    /* Universal Font */
    html, body, [class*="css"] {
        font-family: 'Times New Roman', Times, serif;
    }
    
    /* Adaptive Background - Works in Dark & Light Mode */
   .stApp {
        background-color: var(--background-color);
    }
    
    /* Main Title */
   .main-title {
        font-size: 28px!important;
        font-weight: bold;
        text-align: center;
        padding: 10px;
        margin: 5px 0;
        border-bottom: 3px solid #5B9BD5;
    }
    
    /* Author Strip */
   .author-strip {
        text-align: center;
        font-size: 12px;
        padding: 5px;
        margin-bottom: 10px;
        opacity: 0.8;
    }
   .author-strip a {
        margin: 0 8px;
        text-decoration: none;
    }
    
    /* KPI Cards - Adaptive */
    div[data-testid="metric-container"] {
        background-color: rgba(128, 128, 128, 0.1);
        border: 1px solid rgba(128, 128, 128, 0.2);
        padding: 10px;
        border-radius: 5px;
        border-left: 4px solid #5B9BD5;
    }
    div[data-testid="metric-container"] label {
        font-size: 12px!important;
    }
    
    /* Top Nav Slicers - Compact */
   .stMultiSelect,.stSlider {
        font-size: 12px!important;
    }
   .stMultiSelect div[data-baseweb="select"] {
        min-height: 28px!important;
        font-size: 11px!important;
    }
    
    /* Sidebar - Only Downloads & Profile */
    section[data-testid="stSidebar"] {
        width: 250px!important;
    }
    section[data-testid="stSidebar"] h1 {
        font-size: 18px!important;
        text-align: center;
        padding-bottom: 8px;
        border-bottom: 2px solid #5B9BD5;
    }
    
    /* Reduce padding everywhere */
   .block-container {
        padding-top: 1rem!important;
        padding-bottom: 0rem!important;
    }
    
    /* Chart containers */
   .chart-container {
        padding: 5px;
        border-radius: 5px;
        background-color: rgba(128, 128, 128, 0.05);
    }
    
    /* Hide Streamlit branding */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
</style>
""", unsafe_allow_html=True)

# ==================== 3. LOAD DATA ====================
@st.cache_data
def load_data():
    df = pd.read_csv('data/funding_data_2026_cleaned.csv')
    return df

df = load_data()

# ==================== 4. TOP NAV BAR - SLICERS ====================
st.markdown('<p class="main-title">Funded of 2026 - India Startup Funding Dashboard</p>', unsafe_allow_html=True)

# Author Strip
st.markdown(f"""
<div class="author-strip">
<b>Analyst:</b> Remsha Ansari | 
<b>Records:</b> {len(df)} | 
<a href="https://remsha-ansari.lovable.app/" target="_blank">Portfolio</a> |
<a href="https://github.com/remsha-work" target="_blank">GitHub</a> |
<a href="https://www.linkedin.com/in/ansari-remsha-/" target="_blank">LinkedIn</a> |
<a href="mailto:remsha.work@gmail.com">Email</a>
</div>
""", unsafe_allow_html=True)

# Slicers in Top Nav Bar - 4 Columns
st.markdown("**Filters:**")
col1, col2, col3, col4 = st.columns(4)

with col1:
    month_filter = st.multiselect(
        "Month",
        options=df['Month'].unique(),
        default=df['Month'].unique(),
        label_visibility="collapsed",
        placeholder="Month"
    )

with col2:
    type_filter = st.multiselect(
        "Funding Type",
        options=sorted(df['Funding Type'].unique()),
        default=[],
        label_visibility="collapsed",
        placeholder="Funding Type"
    )

with col3:
    industry_filter = st.multiselect(
        "Industry",
        options=sorted(df['Primary Industry'].unique()),
        default=[],
        label_visibility="collapsed",
        placeholder="Industry"
    )

with col4:
    min_amt, max_amt = st.slider(
        "Amount (USD M)",
        min_value=0,
        max_value=int(df['Funding Amount (USD)'].max() / 1e6) + 10,
        value=(0, int(df['Funding Amount (USD)'].max() / 1e6)),
        label_visibility="collapsed"
    )

st.markdown("---")

# ==================== 5. FILTER DATA ====================
df_filtered = df[df['Month'].isin(month_filter)]
if type_filter:
    df_filtered = df_filtered[df_filtered['Funding Type'].isin(type_filter)]
if industry_filter:
    df_filtered = df_filtered[df_filtered['Primary Industry'].isin(industry_filter)]
df_filtered = df_filtered[
    (df_filtered['Funding Amount (USD)'] >= min_amt * 1e6) & 
    (df_filtered['Funding Amount (USD)'] <= max_amt * 1e6)
]

# ==================== 6. KPI CARDS - COMPACT ROW ====================
total_funding = df_filtered['Funding Amount (USD)'].sum()
total_deals = len(df_filtered)
avg_deal = df_filtered[df_filtered['Funding Amount (USD)'] > 0]['Funding Amount (USD)'].mean()
undisclosed_pct = df_filtered['Is_Undisclosed'].sum() / len(df_filtered) * 100 if len(df_filtered) > 0 else 0

kpi1, kpi2, kpi3, kpi4, kpi5 = st.columns(5)
kpi1.metric("Total Funding", f"${total_funding/1e6:.1f}M")
kpi2.metric("Total Deals", f"{total_deals}")
kpi3.metric("Avg Deal", f"${avg_deal/1e6:.2f}M" if avg_deal > 0 else "$0M")
kpi4.metric("% Undisclosed", f"{undisclosed_pct:.1f}%")
kpi5.metric("Filtered Records", f"{len(df_filtered)}/100")

# ==================== 7. CHARTS - 2x2 GRID - ALL VISIBLE ====================
chart_col1, chart_col2 = st.columns(2)

# Chart 1: Bar Chart - Top 5 Sectors
with chart_col1:
    st.markdown("##### Top 5 Sectors by Funding")
    top_sectors = df_filtered.groupby('Primary Industry').agg({
        'Funding Amount (USD)': 'sum'
    }).nlargest(5, 'Funding Amount (USD)').reset_index()
    
    fig_bar = px.bar(
        top_sectors, 
        x='Primary Industry', 
        y='Funding Amount (USD)',
        text='Funding Amount (USD)',
        color='Primary Industry',
        color_discrete_sequence=px.colors.qualitative.Bold
    )
    fig_bar.update_traces(texttemplate='$%{text:.2s}', textposition='outside')
    fig_bar.update_layout(
        font=dict(family="Times New Roman", size=10),
        showlegend=False,
        height=280,
        margin=dict(l=10, r=10, t=10, b=10),
        yaxis_title="",
        xaxis_title="",
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)'
    )
    st.plotly_chart(fig_bar, use_container_width=True)

# Chart 2: Donut Chart - Funding Type
with chart_col2:
    st.markdown("##### Funding Type Breakdown")
    type_breakdown = df_filtered['Funding Type'].value_counts().reset_index()
    fig_donut = px.pie(
        type_breakdown, 
        names='Funding Type', 
        values='count',
        hole=0.5,
        color_discrete_sequence=px.colors.qualitative.Set3
    )
    fig_donut.update_layout(
        font=dict(family="Times New Roman", size=10),
        height=280,
        margin=dict(l=10, r=10, t=10, b=10),
        showlegend=True,
        legend=dict(orientation="v", font=dict(size=9)),
        paper_bgcolor='rgba(0,0,0,0)'
    )
    st.plotly_chart(fig_donut, use_container_width=True)

chart_col3, chart_col4 = st.columns(2)

# Chart 3: Line Chart - Jan vs Feb
with chart_col3:
    st.markdown("##### Jan vs Feb 2026 Trend")
    monthly = df_filtered.groupby('Month')['Funding Amount (USD)'].sum().reset_index()
    fig_line = px.line(
        monthly, 
        x='Month', 
        y='Funding Amount (USD)',
        markers=True,
        text='Funding Amount (USD)'
    )
    fig_line.update_traces(
        texttemplate='$%{text:.2s}', 
        textposition='top center',
        line=dict(color='#5B9BD5', width=3), 
        marker=dict(size=8)
    )
    fig_line.update_layout(
        font=dict(family="Times New Roman", size=10),
        height=280,
        margin=dict(l=10, r=10, t=10, b=10),
        yaxis_title="",
        xaxis_title="",
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)'
    )
    st.plotly_chart(fig_line, use_container_width=True)

# Chart 4: Table - Top 10 Deals
with chart_col4:
    st.markdown("##### Top 10 Deals")
    top_deals = df_filtered.nlargest(10, 'Funding Amount (USD)')[
        ['Name', 'Funding Amount (USD)', 'Primary Industry']
    ].copy()
    top_deals['Funding Amount (USD)'] = top_deals['Funding Amount (USD)'].apply(lambda x: f"${x/1e6:.1f}M")
    top_deals.columns = ['Startup', 'Amount', 'Sector']
    st.dataframe(
        top_deals, 
        use_container_width=True, 
        height=280, 
        hide_index=True
    )

# ==================== 8. INSIGHTS - COMPACT ROW ====================
st.markdown("##### Key Insights")
ins1, ins2, ins3 = st.columns(3)

early_stage_pct = df_filtered[df_filtered['Stage_Group']=='Early Stage']['Funding Amount (USD)'].sum() / total_funding * 100 if total_funding > 0 else 0
ins1.caption(f"**Early Stage:** {early_stage_pct:.1f}% funding to Pre-Seed + Seed")

jan_sum = df_filtered[df_filtered['Month']=='Jan-2026']['Funding Amount (USD)'].sum()
feb_sum = df_filtered[df_filtered['Month']=='Feb-2026']['Funding Amount (USD)'].sum()
growth = ((feb_sum - jan_sum) / jan_sum * 100) if jan_sum > 0 else 0
ins2.caption(f"**Growth:** Feb {growth:.1f}% {'↑' if growth>0 else '↓'} vs Jan")

top_industry = df_filtered.groupby('Primary Industry')['Funding Amount (USD)'].sum().nlargest(1)
if not top_industry.empty:
    ins3.caption(f"**Leader:** {top_industry.index[0]} - ${top_industry.values[0]/1e6:.1f}M")

# ==================== 9. SIDEBAR - ONLY DOWNLOADS & PROFILE ====================
with st.sidebar:
    st.markdown("# 📥 Downloads")
    
    def create_pdf():
        pdf = FPDF()
        pdf.add_page()
        pdf.set_font("Times", 'B', 16)
        pdf.cell(0, 10, "Funded 2026 - Executive Summary", ln=True, align='C')
        pdf.set_font("Times", '', 12)
        pdf.ln(5)
        pdf.cell(0, 10, f"Analyst: Remsha Ansari", ln=True)
        pdf.cell(0, 10, f"Total Funding: ${total_funding/1e6:.1f}M | Deals: {total_deals}", ln=True)
        return pdf.output(dest='S').encode('latin-1')
    
    def create_word():
        doc = Document()
        doc.add_heading('Funded 2026 - Report', 0)
        doc.add_paragraph(f'Analyst: Remsha Ansari | Total: ${total_funding/1e6:.1f}M | Deals: {total_deals}')
        doc.add_heading('Notes:', level=1)
        doc.add_paragraph('Add comments here...')
        buffer = BytesIO()
        doc.save(buffer)
        return buffer.getvalue()
    
    st.download_button(
        "📄 PDF Report",
        create_pdf(),
        "Funded-2026.pdf",
        "application/pdf",
        use_container_width=True
    )
    
    excel_buffer = BytesIO()
    df_filtered.to_excel(excel_buffer, index=False)
    st.download_button(
        "📊 Excel Data",
        excel_buffer.getvalue(),
        "Funded-2026.xlsx",
        "application/vnd.ms-excel",
        use_container_width=True
    )
    
    st.download_button(
        "📝 Word Report",
        create_word(),
        "Funded-2026.docx",
        "application/vnd.openxmlformats-officedocument.wordprocessingml.document",
        use_container_width=True
    )
    
    st.markdown("---")
    st.markdown("### 👩‍💻 Remsha Ansari")
    st.markdown("[🌐 Portfolio](https://remsha-ansari.lovable.app/)")
    st.markdown("[💻 GitHub](https://github.com/remsha-work)")
    st.markdown("[💼 LinkedIn](https://www.linkedin.com/in/ansari-remsha-/)")
    st.markdown("[📧 Email](mailto:remsha.work@email.com)")