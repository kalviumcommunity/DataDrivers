import streamlit as st
import pandas as pd
import plotly.express as px

# --------------------------------------
# PAGE CONFIG
# --------------------------------------
st.set_page_config(
    page_title="Hotel Revenue Cockpit",
    page_icon="🏨",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --------------------------------------
# GLOBAL PREMIUM EFFECTS & ANIMATIONS
# --------------------------------------
def apply_premium_effects():
    """Injects high-end UI animations, glassmorphism, and gradient styling globally."""
    st.markdown("""
        <style>
        /* 1. Keyframe Engines */
        @keyframes fadeSlideUp {
            from { opacity: 0; transform: translateY(40px) scale(0.98); }
            to { opacity: 1; transform: translateY(0) scale(1); }
        }
        @keyframes gradientFlow {
            0% { background-position: 0% 50%; }
            50% { background-position: 100% 50%; }
            100% { background-position: 0% 50%; }
        }
        @keyframes pulseLive {
            0% { box-shadow: 0 0 5px #00D4AA; opacity: 1; }
            50% { box-shadow: 0 0 20px #00D4AA; opacity: 0.4; }
            100% { box-shadow: 0 0 5px #00D4AA; opacity: 1; }
        }
        
        /* 2. Global Deep Space Background */
        .stApp {
            background: radial-gradient(circle at 10% 20%, #0A1128 0%, #030408 100%) !important;
        }
        
        /* 3. Sidebar Glassmorphism */
        [data-testid="stSidebar"] {
            background: rgba(14, 17, 23, 0.4) !important;
            backdrop-filter: blur(20px) !important;
            border-right: 1px solid rgba(255, 255, 255, 0.05);
        }
        
        /* 4. Massive Header Typography */
        .hdr-title, .sv-header-title {
            font-size: 46px !important; 
            font-weight: 900 !important;
            letter-spacing: -1.5px;
            text-shadow: 0 10px 40px rgba(0, 212, 170, 0.25);
            margin-bottom: 4px; padding-top: 10px;
        }
        
        /* Apply text gradient only to text spans so Emojis remain visible! */
        .gradient-text {
            background: linear-gradient(90deg, #00D4AA, #3B82F6, #8B5CF6, #00D4AA);
            background-size: 300% auto;
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            animation: gradientFlow 6s ease infinite;
        }
        
        /* Live Blinking Dot */
        .live-dot {
            height: 14px;
            width: 14px;
            background-color: #00D4AA;
            border-radius: 50%;
            display: inline-block;
            margin-right: 6px;
            animation: pulseLive 1.5s infinite ease-in-out;
        }
        
        /* 5. Fluid Responsive Cards - Entrance Animation & Structural Layering */
        .kpi-card, .insight-card, div[data-testid="stPlotlyChart"], .findings-card {
            background: linear-gradient(145deg, rgba(27, 36, 51, 0.85) 0%, rgba(15, 20, 31, 0.95) 100%) !important;
            backdrop-filter: blur(16px) !important;
            border: 1px solid rgba(255, 255, 255, 0.08) !important;
            animation: fadeSlideUp 0.8s cubic-bezier(0.16, 1, 0.3, 1) both;
            transition: all 0.4s cubic-bezier(0.175, 0.885, 0.32, 1.275) !important;
            position: relative;
            
            /* Crucial fix for chart scrollbars overflowing the bounds */
            box-sizing: border-box !important;
            overflow: hidden !important; 
        }
        
        /* Staggered Loading - Targets Streamlit's inner block layouts */
        div[data-testid="stVerticalBlock"] > div:nth-child(1) { animation-delay: 0.1s; }
        div[data-testid="stVerticalBlock"] > div:nth-child(2) { animation-delay: 0.2s; }
        div[data-testid="stVerticalBlock"] > div:nth-child(3) { animation-delay: 0.3s; }
        div[data-testid="stVerticalBlock"] > div:nth-child(4) { animation-delay: 0.4s; }
        div[data-testid="stVerticalBlock"] > div:nth-child(5) { animation-delay: 0.5s; }
        
        /* 6. Extruded Hover States (Increased Lift and Shadow for Final Polish) */
        .kpi-card:hover, .insight-card:hover, div[data-testid="stPlotlyChart"]:hover, .findings-card:hover {
            transform: translateY(-10px) scale(1.03) !important;
            box-shadow: 0 25px 50px rgba(0, 0, 0, 0.5), 0 0 0 1.5px #00D4AA !important;
            z-index: 99;
        }
        
        /* 110% Font Setup for all KPIs */
        .kpi-value {
             font-size: 35px !important; 
        }
        
        /* Subtle Diagonal Glare Sweep on cards */
        .kpi-card::after, .insight-card::after {
            content: '';
            position: absolute;
            top: 0; left: -100%;
            width: 50%; height: 100%;
            background: linear-gradient(90deg, transparent, rgba(255,255,255,0.06), transparent);
            transform: skewX(-20deg);
            transition: 0.7s;
        }
        .kpi-card:hover::after, .insight-card:hover::after {
            left: 200%;
        }
        
        /* 7. Button Overhaul (Holographic feel applied to both regular and downloads) */
        div.stButton > button, div.stDownloadButton > button {
            background: linear-gradient(270deg, #00D4AA, #3B82F6, #8B5CF6, #00D4AA) !important;
            background-size: 300% 300% !important;
            border: none !important;
            border-radius: 50px !important; /* Pill shape */
            color: white !important;
            font-weight: 800 !important;
            padding: 0.4rem 1.8rem !important;
            box-shadow: 0 6px 15px rgba(0, 212, 170, 0.3) !important;
            transition: transform 0.3s ease, box-shadow 0.3s ease !important;
            width: 100% !important;
        }
        div.stButton > button:hover, div.stDownloadButton > button:hover {
            animation: gradientFlow 3s ease infinite !important;
            transform: translateY(-4px) scale(1.05) !important;
            box-shadow: 0 12px 25px rgba(0, 212, 170, 0.6) !important;
        }
        </style>
    """, unsafe_allow_html=True)

apply_premium_effects()

# --------------------------------------
# SIDEBAR STYLING
# --------------------------------------
st.markdown("""
<style>

/* Sidebar Width */
[data-testid="stSidebar"]{
    width:250px;
    background:#0E1117;
}

[data-testid="stSidebarContent"]{
    padding:25px 20px;
}

/* Remove extra top padding */
.block-container{
    padding-top:1rem;
}

/* Navigation Buttons */
div.stButton > button{
    width:100%;
    border-radius:10px;
    padding:12px;
    background:#1B2433;
    color:white;
    border:none;
    text-align:left;
    font-weight:600;
    transition:0.2s;
}

div.stButton > button:hover{
    background:#00D4AA;
    color:black;
}

/* Badge */
.badge{
    background:#233A74;
    color:white;
    text-align:center;
    padding:12px;
    border-radius:10px;
    font-weight:bold;
    margin-top:20px;
}

</style>
""", unsafe_allow_html=True)

# --------------------------------------
# SIDEBAR
# --------------------------------------
with st.sidebar:

    st.markdown(
        "<h2 style='text-align:center;'>🏨</h2>",
        unsafe_allow_html=True
    )

    st.markdown(
        """
        <h3 style='color:#00D4AA;
        text-align:center;
        margin-bottom:0px;'>
        REVENUE COCKPIT
        </h3>
        """,
        unsafe_allow_html=True
    )

    st.markdown(
        """
        <p style='color:#9CA3AF;
        text-align:center;
        margin-top:0px;'>
        Internal Analytics
        </p>
        """,
        unsafe_allow_html=True
    )

    st.markdown("---")

    page = st.radio(
        "",
        [
            "📊 Executive Summary",
            "📈 Segment Volatility Analyzer"
        ],
        label_visibility="collapsed"
    )

    st.markdown("<br>", unsafe_allow_html=True)

    st.markdown("---")



# --------------------------------------
# HEADER MODULE
# --------------------------------------
def render_header():
    """
    Renders the main dashboard header section.
    """
    st.markdown("""
        <style>
        /* Header specific typography and spacing */
        .hdr-title { 
            font-size: 36px; 
            font-weight: bold; 
            color: #FFFFFF; 
            margin-bottom: 5px; 
            padding-top: 20px; 
            line-height: 1.2;
        }
        .hdr-subtitle { 
            font-size: 15px; 
            color: #9CA3AF; 
            margin-bottom: 20px; 
        }
        .hdr-live-status { 
            color: #00D4AA; 
            font-weight: bold; 
            text-align: right; 
            font-size: 16px; 
            margin-bottom: 5px; 
            padding-top: 28px; 
        }
        .hdr-refresh { 
            color: #9CA3AF; 
            font-size: 13px; 
            text-align: right; 
        }
        </style>
    """, unsafe_allow_html=True)

    # Use Streamlit columns for 75% / 25% width splitting
    col1, col2 = st.columns([0.75, 0.25])

    with col1:
        st.markdown('<div class="hdr-title"><span style="-webkit-text-fill-color: initial;">🏨</span> <span class="gradient-text">Hotel Revenue Cockpit</span></div>', unsafe_allow_html=True)
        

    with col2:
        st.markdown('<div class="hdr-live-status"><span class="live-dot"></span>LIVE</div>', unsafe_allow_html=True)
        st.markdown('<div class="hdr-refresh">Last Refresh: Today</div>', unsafe_allow_html=True)

    # Divider below the header
    st.markdown("---")


# --------------------------------------
# KPI CARDS MODULE
# --------------------------------------
def render_kpi_cards(occupancy="68.4%", occupancy_mom="▼ -2.1% MoM", volatil_segment="Corporate", revenue_lost="$1.2M"):
    """
    Renders 3 styled KPI cards utilizing dynamic metrics.
    """
    st.markdown("""
        <style>
        /* Shared Container Profile */
        .kpi-card {
            background-color: #1B2433;
            border-radius: 16px;
            padding: 20px;
            box-shadow: 0 4px 6px rgba(0, 0, 0, 0.15);
            transition: transform 0.25s ease, box-shadow 0.25s ease;
            height: 100%;
        }
        /* Hover Effect */
        .kpi-card:hover {
            transform: translateY(-4px);
            box-shadow: 0 10px 15px rgba(0, 0, 0, 0.25);
        }
        /* Typography Layering */
        .kpi-title {
            font-size: 11px;
            text-transform: uppercase;
            color: #9CA3AF;
            font-weight: 700;
            letter-spacing: 0.5px;
            margin-bottom: 12px;
        }
        .kpi-value {
            font-size: 32px;
            font-weight: 800;
            color: #FFFFFF;
            margin-bottom: 6px;
            line-height: 1;
        }
        .kpi-subtitle {
            font-size: 13px;
            color: #6B7280;
        }
        
        /* Precise Accent Top Borders */
        .card-accent-1 { border-top: 3px solid #00D4AA; }
        .card-accent-2 { border-top: 3px solid #F59E0B; }
        .card-accent-3 { border-top: 3px solid #EF4444; }
        </style>
    """, unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown(f'''
            <div class="kpi-card card-accent-1">
                <div class="kpi-title">GLOBAL OCCUPANCY RATE</div>
                <div class="kpi-value">{occupancy}</div>
                <div class="kpi-subtitle">{occupancy_mom}</div>
            </div>
        ''', unsafe_allow_html=True)
        
    with col2:
        st.markdown(f'''
            <div class="kpi-card card-accent-2">
                <div class="kpi-title">HIGHEST VOLATILITY SEGMENT</div>
                <div class="kpi-value">{volatil_segment}</div>
                <div class="kpi-subtitle">Responsible for sudden cancellations</div>
            </div>
        ''', unsafe_allow_html=True)
        
    with col3:
        st.markdown(f'''
            <div class="kpi-card card-accent-3">
                <div class="kpi-title">REVENUE LOST</div>
                <div class="kpi-value">{revenue_lost}</div>
                <div class="kpi-subtitle">Current Quarter</div>
            </div>
        ''', unsafe_allow_html=True)
        
    # Spacer margin below cards
    st.markdown("<br>", unsafe_allow_html=True)


# --------------------------------------
# CHARTS MODULE
# --------------------------------------
def render_charts():
    """
    Renders the occupancy and revenue lost charts cleanly inside dashboard cards.
    """
    
    st.markdown("""
        <style>
        div[data-testid="stPlotlyChart"] {
            background-color: #1B2433;
            border-radius: 16px;
            box-shadow: 0 4px 6px rgba(0, 0, 0, 0.15);
            padding: 24px 34px 30px 34px !important; /* Increased Internal Padding */
            margin-top: 24px;
        }
        </style>
    """, unsafe_allow_html=True)
    
    chart_data = {
        "customer_segment": ["Direct", "Corporate", "Online TA", "Offline TA/TO", "Groups", "Other"],
        "occupancy_rate": [75, 82, 65, 50, 45, 30],
        "revenue_lost": [15000, 5000, 45000, 30000, 80000, 2000]
    }
    df = pd.DataFrame(chart_data)
    
    segment_colors = {
        "Direct": "#00D4AA", "Corporate": "#3B82F6", "Online TA": "#F59E0B",
        "Offline TA/TO": "#EF4444", "Groups": "#8B5CF6", "Other": "#22C55E"
    }
    
    col1, col2 = st.columns(2, gap="large")
    
    with col1:
        # Horizontal Bar Chart for Occupancy
        df_occ = df.sort_values(by="occupancy_rate", ascending=True)
        fig1 = px.bar(
            df_occ, x="occupancy_rate", y="customer_segment", orientation='h',
            text="occupancy_rate", color="customer_segment", color_discrete_map=segment_colors
        )
        
        fig1.update_traces(
            texttemplate='%{text}%', textposition='outside', 
            textfont=dict(color='white', size=14), cliponaxis=False,
            hovertemplate="<b>%{y}</b><br>Occupancy Rate: %{x}%<extra></extra>"
        )
        
        fig1.update_layout(
            height=430, # Increased Height
            title=dict(
                text="<b>Occupancy Rate by Customer Segment</b><br><span style='font-size:14px; color:#9CA3AF;'></span>",
                x=0.5, xanchor='center', font=dict(size=18, color="white")
            ),
            template="plotly_dark", paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)',
            showlegend=False, margin=dict(t=80, l=10, r=40, b=30),
            xaxis=dict(title="Occupancy (%)", showgrid=False, tickfont=dict(color="#9CA3AF", size=13)),
            yaxis=dict(title="", showgrid=False, tickfont=dict(size=14))
        )
        st.plotly_chart(fig1, use_container_width=True, config={'displayModeBar': False})

    with col2:
        # Donut Chart for Revenue Loss
        fig2 = px.pie(
            df, values="revenue_lost", names="customer_segment", hole=0.55,
            color="customer_segment", color_discrete_map=segment_colors
        )
        
        fig2.update_traces(
            textposition='outside', textinfo='percent+label',
            textfont=dict(color='white', size=13),
            hovertemplate="<b>%{label}</b><br>Revenue Loss: $%{value:,.0f}<br>Contribution: %{percent}<extra></extra>"
        )
        
        fig2.update_layout(
            height=430,
            title=dict(
                text="<b>Revenue Lost by Customer Segment</b><br><span style='font-size:14px; color:#9CA3AF;'>Current Quarter</span>",
                x=0.5, xanchor='center', font=dict(size=18, color="white")
            ),
            template="plotly_dark", paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)',
            showlegend=True, legend=dict(orientation="v", yanchor="middle", y=0.5, xanchor="left", x=1.05),
            margin=dict(t=80, l=10, r=10, b=30)
        )
        st.plotly_chart(fig2, use_container_width=True, config={'displayModeBar': False})


# --------------------------------------
# PHASE 5: ADDITIONAL MODULES
# --------------------------------------
def render_executive_insights():
    """Renders the executive insights card section."""
    st.markdown("""
        <style>
        .section-title {
            font-size: 22px;
            font-weight: 700;
            color: #FFFFFF;
            margin: 40px 0 20px 0;
            letter-spacing: 0.5px;
        }
        .insight-card {
            background-color: #1B2433;
            border: 1px solid rgba(255, 255, 255, 0.05);
            border-radius: 12px;
            padding: 24px;
            margin-bottom: 20px;
            height: calc(100% - 20px);
            box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
            transition: transform 0.2s;
        }
        .insight-card:hover {
            transform: translateY(-2px);
        }
        .insight-header {
            font-size: 16px;
            font-weight: 700;
            color: #FFFFFF;
            margin-bottom: 10px;
        }
        .insight-desc {
            font-size: 14px;
            color: #9CA3AF;
            line-height: 1.5;
        }
        </style>
        <div class="section-title">Executive Insights</div>
    """, unsafe_allow_html=True)
    
    c1, c2 = st.columns(2)
    with c1:
        st.markdown('''
            <div class="insight-card">
                <div class="insight-header" style="color: #22C55E;">🟢 Occupancy Performance</div>
                <div class="insight-desc">Overall occupancy remains positive at 68.4%.</div>
            </div>
            <div class="insight-card">
                <div class="insight-header" style="color: #22C55E;">📈 Best Performing Segment</div>
                <div class="insight-desc">Corporate bookings maintain the highest occupancy levels.</div>
            </div>
        ''', unsafe_allow_html=True)
    with c2:
        st.markdown('''
            <div class="insight-card">
                <div class="insight-header" style="color: #EF4444;">⚠ Revenue Risk</div>
                <div class="insight-desc">Online TA contributes the highest volume of revenue loss.</div>
            </div>
            <div class="insight-card">
                <div class="insight-header" style="color: #3B82F6;">💡 Recommendation</div>
                <div class="insight-desc">Increase direct bookings and reduce high-risk OTA dependency.</div>
            </div>
        ''', unsafe_allow_html=True)

def render_key_metrics():
    """Renders the Key Business Metrics row of 4 cards."""
    st.markdown('<div class="section-title">Key Business Metrics</div>', unsafe_allow_html=True)
    cols = st.columns(4)
    metrics = [
        ("🏨 Total Properties", "14"),
        ("📅 Active Bookings", "4,291"),
        ("👥 Customer Segments", "6"),
    ]
    
    for col, (title, val) in zip(cols, metrics):
        with col:
            st.markdown(f'''
                <div class="kpi-card" style="box-shadow: none; border: 1px solid rgba(255, 255, 255, 0.05); padding: 18px; margin-bottom: 10px;">
                    <div class="kpi-title" style="margin-bottom: 8px;">{title}</div>
                    <div class="kpi-value" style="font-size: 24px;">{val}</div>
                </div>
            ''', unsafe_allow_html=True)

def render_business_summary():
    """Renders the full-width contextual business summary paragraph."""
    st.markdown("""
        <div class="section-title">Business Summary</div>
        <div class="kpi-card" style="border: 1px solid rgba(255, 255, 255, 0.05); box-shadow: none;">
            <p style="color: #E5E7EB; font-size: 15px; line-height: 1.6; margin: 0;">
                The hotel portfolio achieved an overall occupancy of <strong>68.4%</strong>. 
                Corporate customers continue to deliver the strongest occupancy performance 
                while Online Travel Agencies contribute the largest share of revenue loss. 
                Diversifying booking channels and encouraging direct reservations can 
                significantly improve profitability.
            </p>
        </div>
    """, unsafe_allow_html=True)

def render_footer():
    """Renders the dashboard footer using pandas dynamically for date."""
    current_date = pd.Timestamp.now().strftime("%B %d, %Y")
    
    st.markdown(f"""
        <hr style="border: none; border-top: 1px solid rgba(255, 255, 255, 0.1); margin: 40px 0 20px 0;" />
        <div style="display: flex; justify-content: space-between; align-items: center; padding-bottom: 20px;">
            <div style="color: #6B7280; font-size: 13px; font-weight: 500;">Hotel Revenue Cockpit Dashboard</div>
            <div style="color: #6B7280; font-size: 13px;">Built with Streamlit + Plotly</div>
            <div style="color: #6B7280; font-size: 13px;">Last Updated : {current_date}</div>
        </div>
    """, unsafe_allow_html=True)


# --------------------------------------
# PHASE 6: SEGMENT VOLATILITY MODULES
# --------------------------------------

def get_volatility_data():
    """Generates working logical dataset for the Segment Volatility Analyzer"""
    return pd.DataFrame({
        "customer_segment": ["Direct", "Corporate", "Online TA", "Offline TA/TO", "Groups", "Other"],
        "occupancy_rate": [75, 82, 65, 50, 45, 30],
        "revenue_lost": [15000, 5000, 45000, 30000, 80000, 2000],
        "volatility_score": [3.2, 1.1, 7.8, 6.5, 9.2, 2.0],
        "cancellation_rate": [5.0, 2.5, 18.2, 12.0, 25.4, 4.1]
    })

def render_sv_styles():
    """Ensures UI styles are globally rendered when hitting the Volatility page"""
    st.markdown("""
        <style>
        .sv-header-title { font-size: 34px; font-weight: 700; color: #FFFFFF; margin-bottom: 4px; padding-top: 10px;}
        .sv-header-subtitle { font-size: 15px; color: #9CA3AF; margin-bottom: 30px; }
        
        .kpi-card {
            background-color: #1B2433; border-radius: 12px; padding: 20px;
            box-shadow: 0 4px 6px rgba(0, 0, 0, 0.15); transition: transform 0.2s;
            border: 1px solid rgba(255, 255, 255, 0.05); height: 100%;
        }
        .kpi-card:hover { transform: translateY(-3px); }
        .kpi-title { font-size: 11px; text-transform: uppercase; color: #9CA3AF; font-weight: 700; margin-bottom: 8px;}
        .kpi-value { font-size: 28px; font-weight: 800; color: white; }
        
        .section-title { font-size: 20px; font-weight: 700; color: white; margin: 32px 0 20px 0; }
        
        div[data-testid="stPlotlyChart"] {
            background-color: #1B2433; border-radius: 16px;
            box-shadow: 0 4px 6px rgba(0,0,0,0.15); padding: 10px 20px 20px 20px; margin-top: 10px;
        }
        
        .findings-card {
            background-color: #1B2433; border-radius: 12px; padding: 24px;
            border: 1px solid rgba(255, 255, 255, 0.05); margin-bottom: 20px;
        }
        .finding-item { font-size: 15px; color: #E5E7EB; margin-bottom: 12px; display: flex; gap: 10px; align-items:flex-start; }
        </style>
    """, unsafe_allow_html=True)

def render_segment_volatility_page():
    render_sv_styles()
    
    # 1. HEADER (Isolating the emoji from the text gradient so it's fully visible)
    st.markdown('<div class="sv-header-title"><span style="-webkit-text-fill-color: initial;">📈</span> <span class="gradient-text">Segment Volatility Analyzer</span></div>', unsafe_allow_html=True)
    st.markdown('<div class="sv-header-subtitle">Analyze customer segment volatility, cancellations and revenue impact.</div>', unsafe_allow_html=True)
    
    df = get_volatility_data()
    
    # 2. FILTER SECTION (State management)
    if 'sv_seg' not in st.session_state: st.session_state.sv_seg = 'All'
    if 'sv_sort' not in st.session_state: st.session_state.sv_sort = 'Volatility Score'
    
    def reset_filters():
        st.session_state.sv_seg = 'All'
        st.session_state.sv_sort = 'Volatility Score'

    st.markdown("---")
    fc1, fc2, fc3, fc4 = st.columns([1.5, 1.5, 1, 4])
    with fc1:
        seg_options = ["All"] + list(df['customer_segment'].unique())
        seg_filter = st.selectbox("Customer Segment", seg_options, key='sv_seg')
    with fc2:
        sort_by = st.selectbox("Sort By", ["Volatility Score", "Occupancy Rate", "Revenue Lost"], key='sv_sort')
    with fc3:
        st.markdown("<div style='height: 28px;'></div>", unsafe_allow_html=True)
        st.button("Reset Filters", on_click=reset_filters, use_container_width=True)
    
    st.markdown("<br>", unsafe_allow_html=True)

    # Apply Filtering
    if st.session_state.sv_seg != "All":
        df = df[df["customer_segment"] == st.session_state.sv_seg]
        
    sort_keys = {"Volatility Score": "volatility_score", "Occupancy Rate": "occupancy_rate", "Revenue Lost": "revenue_lost"}
    df = df.sort_values(by=sort_keys[st.session_state.sv_sort], ascending=False)
    
    # 3. KPI ROW
    if not df.empty:
        max_vol_score = df["volatility_score"].max()
        risk_seg = df.loc[df["volatility_score"].idxmax()]["customer_segment"]
        avg_occ = df["occupancy_rate"].mean()
        tot_rev_lost = df["revenue_lost"].sum()
    else:
        max_vol_score, risk_seg, avg_occ, tot_rev_lost = 0, "N/A", 0, 0
        
    kc1, kc2, kc3, kc4 = st.columns(4)
    kpis = [
        ("Highest Volatility Score", f"{max_vol_score:.1f}", "#EF4444"),
        ("Highest Risk Segment", risk_seg, "#F59E0B"),
        ("Average Occupancy", f"{avg_occ:.1f}%", "#00D4AA"),
        ("Total Revenue Lost", f"${tot_rev_lost:,.0f}", "#EF4444")
    ]
    for c, (title, val, color) in zip([kc1, kc2, kc3, kc4], kpis):
        with c:
             st.markdown(f'''
                <div class="kpi-card" style="border-top: 3px solid {color}">
                    <div class="kpi-title">{title}</div>
                    <div class="kpi-value">{val}</div>
                </div>
            ''', unsafe_allow_html=True)
            
    # Universal Segment Palette 
    segment_colors = {"Direct": "#00D4AA", "Corporate": "#3B82F6", "Online TA": "#F59E0B", "Offline TA/TO": "#EF4444", "Groups": "#8B5CF6", "Other": "#22C55E"}
            
    # 4. CHART SECTION (ROW 1 - Volatility Metrics)
    st.markdown('<div class="section-title">Segment Volatility Metrics</div>', unsafe_allow_html=True)
    c1, c2 = st.columns(2, gap="large")
    
    with c1:
        # Horizonatal Bar
        df_h = df.sort_values(by="volatility_score", ascending=True) 
        fig1 = px.bar(df_h, x="volatility_score", y="customer_segment", color="customer_segment", orientation='h', text="volatility_score", color_discrete_map=segment_colors)
        fig1.update_traces(
            textposition='outside', textfont=dict(color='white', size=13), cliponaxis=False,
            hovertemplate="<b>%{y}</b><br>Volatility Score: %{x}<extra></extra>"
        )
        fig1.update_layout(
            height=430,
            title=dict(text="<b>Volatility Score by Customer Segment</b>", x=0.5, xanchor='center', font=dict(size=18, color="white")),
            template="plotly_dark", paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', showlegend=False,
            margin=dict(t=80, l=10, r=40, b=30), 
            xaxis=dict(showgrid=False, range=[0, (df['volatility_score'].max() or 1) * 1.2], showticklabels=False, title=""), 
            yaxis=dict(showgrid=False, title="", tickfont=dict(size=14))
        )
        st.plotly_chart(fig1, use_container_width=True, config={'displayModeBar': False})
        
    with c2:
        # Revenue Loss transformed to Donut Chart
        fig2 = px.pie(
            df, values="revenue_lost", names="customer_segment", hole=0.55,
            color="customer_segment", color_discrete_map=segment_colors
        )
        
        fig2.update_traces(
            textposition='outside', textinfo='percent+label',
            textfont=dict(color='white', size=13),
            hovertemplate="<b>%{label}</b><br>Revenue Loss: $%{value:,.0f}<br>Contribution: %{percent}<extra></extra>"
        )
        fig2.update_layout(
            height=430,
            title=dict(
                text="<b>Revenue Loss Distribution</b>",
                x=0.5, xanchor='center', font=dict(size=18, color="white")
            ),
            template="plotly_dark", paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', showlegend=True,
            legend=dict(orientation="v", yanchor="middle", y=0.5, xanchor="left", x=1.05),
            margin=dict(t=80, l=10, r=10, b=30)
        )
        st.plotly_chart(fig2, use_container_width=True, config={'displayModeBar': False})

    # 5. SECOND CHART ROW
    c3, c4 = st.columns(2, gap="large")
    with c3:
        # Horizontal Bar for Cancellation Rate
        df_cancel = df.sort_values(by="cancellation_rate", ascending=True)
        fig3 = px.bar(
            df_cancel, x="cancellation_rate", y="customer_segment", orientation='h',
            text="cancellation_rate", color="cancellation_rate", color_continuous_scale="Reds"
        )
        fig3.update_traces(
            texttemplate='%{text}%', textposition='outside', textfont=dict(color='white', size=14), cliponaxis=False,
            hovertemplate="<b>%{y}</b><br>Cancel Rate: %{x}%<extra></extra>"
        )
        fig3.update_layout(
            height=430,
            title=dict(text="<b>Cancellation Rate by Segment</b>", x=0.5, xanchor='center', font=dict(size=18, color="white")),
            template="plotly_dark", paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', showlegend=False,
            coloraxis_showscale=False,
            margin=dict(t=80, l=10, r=40, b=30), 
            yaxis=dict(showgrid=False, title="", tickfont=dict(size=14)), 
            xaxis=dict(showgrid=False, title="Cancellation Rate (%)", tickfont=dict(color="#9CA3AF", size=13))
        )
        st.plotly_chart(fig3, use_container_width=True, config={'displayModeBar': False})
        
    with c4:
        # Heavily Enhanced Scatter Plot with Quadrants
        avg_occ = df["occupancy_rate"].mean() if not df.empty else 0
        avg_vol = df["volatility_score"].mean() if not df.empty else 0
        
        fig4 = px.scatter(
            df, x="occupancy_rate", y="volatility_score", size="revenue_lost", color="customer_segment", 
            size_max=35, # Increased bubble visibility
            color_discrete_map=segment_colors, hover_name="customer_segment",
            hover_data={"customer_segment": False, "occupancy_rate": True, "revenue_lost": True, "volatility_score": True}
        )
        
        # Enforce advanced Tooltip data string
        fig4.update_traces(hovertemplate="<b>%{hovertext}</b><br>Occupancy: %{x}%<br>Volatility: %{y}<br>Loss: %{marker.size}<extra></extra>")
        
        # Inject Quadrant Lines
        if not df.empty:
            fig4.add_vline(x=avg_occ, line_dash="dash", line_color="rgba(255,255,255,0.25)")
            fig4.add_hline(y=avg_vol, line_dash="dash", line_color="rgba(255,255,255,0.25)")
            
            # Quadrant Annotations (High Level Mapping)
            x_min, x_max = df['occupancy_rate'].min(), df['occupancy_rate'].max()
            y_min, y_max = df['volatility_score'].min(), df['volatility_score'].max()
            
            fig4.add_annotation(x=x_min, y=y_max, text="High Risk", showarrow=False, font=dict(color="#EF4444", size=12), align="left", xanchor="left")
            fig4.add_annotation(x=x_max, y=y_max, text="High Opportunity", showarrow=False, font=dict(color="#F59E0B", size=12), align="right", xanchor="right")
            fig4.add_annotation(x=x_min, y=y_min, text="Low Performance", showarrow=False, font=dict(color="#9CA3AF", size=12), align="left", xanchor="left")
            fig4.add_annotation(x=x_max, y=y_min, text="Stable Segment", showarrow=False, font=dict(color="#00D4AA", size=12), align="right", xanchor="right")
        
        fig4.update_layout(
            height=430,
            title=dict(text="<b>Occupancy vs Volatility Matrix</b>", x=0.5, xanchor='center', font=dict(size=18, color="white")),
            template="plotly_dark", paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', showlegend=False,
            margin=dict(t=80, l=10, r=10, b=30), 
            yaxis=dict(showgrid=True, gridcolor='rgba(255,255,255,0.1)', title="Volatility Score", tickfont=dict(color="#9CA3AF", size=13)), 
            xaxis=dict(showgrid=True, gridcolor='rgba(255,255,255,0.1)', title="Occupancy Rate (%)", tickfont=dict(color="#9CA3AF", size=13))
        )
        st.plotly_chart(fig4, use_container_width=True, config={'displayModeBar': False})

    # 6. INSIGHTS PANEL
    st.markdown('<div class="section-title">Key Findings</div>', unsafe_allow_html=True)
    if not df.empty:
        high_vol = df.loc[df["volatility_score"].idxmax()]
        low_occ = df.loc[df["occupancy_rate"].idxmin()]
        high_rev = df.loc[df["revenue_lost"].idxmax()]
        stable_seg = df.loc[df["volatility_score"].idxmin()]
        
        st.markdown(f'''
            <div class="findings-card">
                <div class="finding-item"><span>⚠</span> <span><b>Highest volatility segment:</b> {high_vol["customer_segment"]} is displaying extreme fluctuation patterns.</span></div>
                <div class="finding-item"><span>📉</span> <span><b>Lowest occupancy:</b> {low_occ["customer_segment"]} struggles with only {low_occ["occupancy_rate"]}%.</span></div>
                <div class="finding-item"><span>💸</span> <span><b>Highest revenue loss:</b> {high_rev["customer_segment"]} trails negatively with ${high_rev["revenue_lost"]:,.0f} lost.</span></div>
                <div class="finding-item"><span>🛡</span> <span><b>Most stable segment:</b> {stable_seg["customer_segment"]} anchors the floor with a low {stable_seg["volatility_score"]} volatility score.</span></div>
                <div class="finding-item"><span>💡</span> <span><b>Recommended action:</b> Implement rigid cancellation limits on {high_vol["customer_segment"]} and re-target {stable_seg["customer_segment"]} for safe baseload.</span></div>
            </div>
        ''', unsafe_allow_html=True)
    
    # 7. DATA TABLE
    with st.expander("Detailed Segment Metrics", expanded=False):
        st.dataframe(df, use_container_width=True, hide_index=True)
        
    st.markdown("<br>", unsafe_allow_html=True)
        
    # 8. EXPORT SECTION (Fixed un-styled button and dead click)
    ec1, ec2, _ = st.columns([1, 1.2, 5])
    with ec1:
        csv_data = df.to_csv(index=False).encode('utf-8')
        st.download_button("Download CSV", data=csv_data, file_name="segment_metrics.csv", use_container_width=True)
    with ec2:
        # Dynamically generate a readable text report so it isn't an invalid PDF byte-stream
        report_text = f"HOTEL REVENUE COCKPIT : SEGMENT VOLATILITY REPORT\n"
        report_text += f"Generated: {pd.Timestamp.now().strftime('%B %d, %Y - %H:%M:%S')}\n"
        report_text += "="*50 + "\n\n"
        report_text += "--- EXECUTIVE SUMMARY ---\n"
        report_text += f"Total Revenue Lost: ${df['revenue_lost'].sum():,.0f}\n"
        report_text += f"Average Occupancy: {df['occupancy_rate'].mean():.1f}%\n"
        report_text += f"Highest Risk Segment: {df.loc[df['volatility_score'].idxmax()]['customer_segment']}\n\n"
        report_text += "--- DETAILED METRICS ---\n"
        for _, row in df.iterrows():
            report_text += f" • {row['customer_segment'].ljust(15)} | Occ: {row['occupancy_rate']}% | Loss: ${row['revenue_lost']:,.0f} | Volatility: {row['volatility_score']}\n"
        report_text += "\n--- RECOMMENDATION ---\n"
        report_text += f"Implement exposure limits on {df.loc[df['volatility_score'].idxmax()]['customer_segment']} to prevent further margin leaks.\n"

        st.download_button("Download Dashboard Report", data=report_text.encode('utf-8'), file_name="dashboard_report.txt", use_container_width=True)
    
    render_footer()


# --------------------------------------
# MAIN DASHBOARD VIEW
# --------------------------------------
if page == "📊 Executive Summary":
    render_header()
    render_kpi_cards()
    render_charts()
    render_executive_insights()
    render_key_metrics()
    render_business_summary()
    render_footer()
elif page == "📈 Segment Volatility Analyzer":
    render_segment_volatility_page()