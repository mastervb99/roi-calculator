"""
UI Styles for ROI Calculator
"""

import streamlit as st
from config.defaults import BITSCOPIC_COLORS

def load_css():
    """Load custom CSS styles with high contrast for accessibility"""
    st.markdown(f"""
    <style>
        /* Main App Styling - High Contrast */
        .stApp {{
            background-color: {BITSCOPIC_COLORS['background']};
            color: {BITSCOPIC_COLORS['text']};
        }}
        
        /* Ensure all text is readable */
        p, span, div, label {{
            color: {BITSCOPIC_COLORS['text']} !important;
            font-size: 1.05em;
            line-height: 1.6;
        }}
        
        /* Header Styling - Solid colors for better contrast */
        .main-header {{
            background: {BITSCOPIC_COLORS['primary']};
            color: white;
            padding: 35px;
            border-radius: 10px;
            margin-bottom: 30px;
            text-align: center;
            box-shadow: 0 4px 8px rgba(0,0,0,0.2);
            border: 3px solid {BITSCOPIC_COLORS['primary']};
        }}
        
        .header-title {{
            font-size: 2.8em;
            font-weight: 900;
            margin-bottom: 10px;
            color: white !important;
            text-shadow: 2px 2px 4px rgba(0,0,0,0.3);
        }}
        
        .header-subtitle {{
            font-size: 1.4em;
            font-weight: 600;
            color: white !important;
        }}
        
        /* Metric Cards - High Contrast */
        .metric-card {{
            background: white;
            border-radius: 8px;
            padding: 28px;
            text-align: center;
            box-shadow: 0 3px 6px rgba(0,0,0,0.15);
            border: 2px solid {BITSCOPIC_COLORS['primary']};
            border-left: 6px solid {BITSCOPIC_COLORS['orange']};
            transition: all 0.3s ease;
            height: 100%;
        }}
        
        .metric-card:hover {{
            transform: translateY(-3px);
            box-shadow: 0 6px 12px rgba(0,0,0,0.25);
            border-color: {BITSCOPIC_COLORS['orange']};
        }}
        
        .metric-value {{
            font-size: 2.8em;
            font-weight: 900;
            color: {BITSCOPIC_COLORS['primary']};
            margin-bottom: 8px;
        }}
        
        .metric-label {{
            font-size: 1.1em;
            color: {BITSCOPIC_COLORS['dark_text']};
            text-transform: uppercase;
            letter-spacing: 0.5px;
            font-weight: 700;
        }}
        
        .metric-delta {{
            font-size: 0.85em;
            margin-top: 8px;
            padding: 4px 8px;
            border-radius: 12px;
            display: inline-block;
        }}
        
        .metric-positive {{
            color: {BITSCOPIC_COLORS['accent']};
            background: rgba(0, 195, 137, 0.1);
        }}
        
        .metric-negative {{
            color: {BITSCOPIC_COLORS['danger']};
            background: rgba(220, 53, 69, 0.1);
        }}
        
        /* Section Headers */
        .section-header {{
            color: {BITSCOPIC_COLORS['primary']};
            font-size: 1.8em;
            font-weight: 600;
            margin: 40px 0 25px 0;
            padding-bottom: 10px;
            border-bottom: 3px solid {BITSCOPIC_COLORS['orange']};
        }}
        
        /* Info Boxes - High Contrast */
        .info-box {{
            background: white;
            border: 2px solid {BITSCOPIC_COLORS['secondary']};
            border-left: 6px solid {BITSCOPIC_COLORS['secondary']};
            border-radius: 8px;
            padding: 24px;
            margin: 20px 0;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        }}
        
        .info-box-title {{
            font-weight: 800;
            color: {BITSCOPIC_COLORS['primary']};
            margin-bottom: 12px;
            font-size: 1.3em;
        }}
        
        .info-box-content {{
            color: {BITSCOPIC_COLORS['text']};
            line-height: 1.8;
            font-size: 1.1em;
            font-weight: 500;
        }}
        
        /* Charts Section */
        .chart-container {{
            background: white;
            border-radius: 12px;
            padding: 25px;
            margin: 20px 0;
            box-shadow: 0 2px 4px rgba(0,0,0,0.08);
        }}
        
        .chart-title {{
            font-size: 1.4em;
            font-weight: 600;
            color: {BITSCOPIC_COLORS['primary']};
            margin-bottom: 20px;
            text-align: center;
        }}
        
        /* Tabs Styling */
        .stTabs [data-baseweb="tab-list"] {{
            gap: 8px;
            background-color: white;
            border-radius: 10px;
            padding: 4px;
        }}
        
        .stTabs [data-baseweb="tab"] {{
            border-radius: 8px;
            color: {BITSCOPIC_COLORS['neutral']};
            font-weight: 500;
        }}
        
        .stTabs [aria-selected="true"] {{
            background-color: {BITSCOPIC_COLORS['orange']};
            color: white;
        }}
        
        /* Buttons - High Contrast */
        .stButton > button {{
            background: {BITSCOPIC_COLORS['primary']};
            color: white !important;
            border: 2px solid {BITSCOPIC_COLORS['primary']};
            border-radius: 6px;
            padding: 12px 28px;
            font-weight: 700;
            font-size: 1.1em;
            transition: all 0.3s ease;
            box-shadow: 0 3px 6px rgba(0,0,0,0.2);
        }}
        
        .stButton > button:hover {{
            background: {BITSCOPIC_COLORS['orange']};
            border-color: {BITSCOPIC_COLORS['orange']};
            transform: translateY(-2px);
            box-shadow: 0 5px 10px rgba(0,0,0,0.3);
        }}
        
        .stButton > button:focus {{
            outline: 3px solid {BITSCOPIC_COLORS['warning']};
            outline-offset: 2px;
        }}
        
        /* Sidebar Styling - Better Contrast */
        .css-1d391kg {{
            background-color: #f0f0f0;
        }}
        
        /* Sidebar text */
        .css-1d391kg p, .css-1d391kg label, .css-1d391kg span {{
            color: {BITSCOPIC_COLORS['text']} !important;
            font-size: 1.1em !important;
            font-weight: 500;
        }}
        
        /* Input fields - Better visibility */
        .stTextInput > div > div > input,
        .stNumberInput > div > div > input,
        .stSelectbox > div > div > select {{
            font-size: 1.15em !important;
            padding: 10px !important;
            border: 2px solid {BITSCOPIC_COLORS['primary']} !important;
            background-color: white !important;
            color: {BITSCOPIC_COLORS['text']} !important;
            font-weight: 500;
        }}
        
        .stTextInput > div > div > input:focus,
        .stNumberInput > div > div > input:focus,
        .stSelectbox > div > div > select:focus {{
            border-color: {BITSCOPIC_COLORS['orange']} !important;
            outline: 3px solid rgba(211, 84, 0, 0.2) !important;
            outline-offset: 2px;
        }}
        
        /* Sliders - Better visibility */
        .stSlider > div > div > div > div {{
            background-color: {BITSCOPIC_COLORS['primary']} !important;
        }}
        
        .stSlider label {{
            font-size: 1.1em !important;
            font-weight: 600 !important;
            color: {BITSCOPIC_COLORS['text']} !important;
        }}
        
        /* Parameter Groups */
        .param-group {{
            background: white;
            border-radius: 10px;
            padding: 20px;
            margin-bottom: 20px;
            box-shadow: 0 1px 3px rgba(0,0,0,0.08);
        }}
        
        .param-group-title {{
            font-weight: 600;
            color: {BITSCOPIC_COLORS['primary']};
            margin-bottom: 15px;
            font-size: 1.1em;
            display: flex;
            align-items: center;
            gap: 10px;
        }}
        
        .param-impact-high {{
            border-left: 4px solid {BITSCOPIC_COLORS['danger']};
        }}
        
        .param-impact-medium {{
            border-left: 4px solid {BITSCOPIC_COLORS['warning']};
        }}
        
        .param-impact-low {{
            border-left: 4px solid {BITSCOPIC_COLORS['accent']};
        }}
        
        /* Summary Cards Grid */
        .summary-grid {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
            gap: 20px;
            margin: 30px 0;
        }}
        
        /* Welcome Section */
        .welcome-header {{
            text-align: center;
            margin: 40px 0;
            animation: fadeIn 0.8s ease-in;
        }}
        
        @keyframes fadeIn {{
            from {{ opacity: 0; transform: translateY(20px); }}
            to {{ opacity: 1; transform: translateY(0); }}
        }}
        
        /* Comparison Table */
        .comparison-table {{
            background: white;
            border-radius: 10px;
            overflow: hidden;
            box-shadow: 0 2px 4px rgba(0,0,0,0.08);
        }}
        
        .comparison-table th {{
            background: {BITSCOPIC_COLORS['primary']};
            color: white;
            padding: 12px;
            text-align: left;
            font-weight: 600;
        }}
        
        .comparison-table td {{
            padding: 12px;
            border-bottom: 1px solid #e9ecef;
        }}
        
        .comparison-table tr:hover {{
            background-color: #f8f9fa;
        }}
        
        /* Alert Boxes - High Contrast */
        .alert-success {{
            background: white;
            border: 2px solid {BITSCOPIC_COLORS['accent']};
            border-left: 6px solid {BITSCOPIC_COLORS['accent']};
            color: #003d00;
            padding: 18px 24px;
            border-radius: 8px;
            margin: 15px 0;
            font-weight: 600;
            font-size: 1.1em;
        }}
        
        .alert-info {{
            background: white;
            border: 2px solid {BITSCOPIC_COLORS['secondary']};
            border-left: 6px solid {BITSCOPIC_COLORS['secondary']};
            color: #002040;
            padding: 18px 24px;
            border-radius: 8px;
            margin: 15px 0;
            font-weight: 600;
            font-size: 1.1em;
        }}
        
        .alert-warning {{
            background: white;
            border: 2px solid {BITSCOPIC_COLORS['warning']};
            border-left: 6px solid {BITSCOPIC_COLORS['warning']};
            color: #4d2800;
            padding: 18px 24px;
            border-radius: 8px;
            margin: 15px 0;
            font-weight: 600;
            font-size: 1.1em;
        }}
        
        /* Loading Animation */
        .loading-spinner {{
            width: 50px;
            height: 50px;
            border: 4px solid #f3f3f3;
            border-top: 4px solid {BITSCOPIC_COLORS['orange']};
            border-radius: 50%;
            animation: spin 1s linear infinite;
            margin: 20px auto;
        }}
        
        @keyframes spin {{
            0% {{ transform: rotate(0deg); }}
            100% {{ transform: rotate(360deg); }}
        }}
        
        /* Responsive Design */
        @media (max-width: 768px) {{
            .summary-grid {{
                grid-template-columns: 1fr;
            }}
            
            .header-title {{
                font-size: 2em;
            }}
            
            .metric-value {{
                font-size: 2em;
            }}
        }}
    </style>
    """, unsafe_allow_html=True)