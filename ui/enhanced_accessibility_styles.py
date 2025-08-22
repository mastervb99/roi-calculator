"""
Enhanced Accessibility Styles for ROI Calculator
Optimized for visual impairment and WCAG AAA compliance
"""

import streamlit as st

def load_enhanced_css():
    """Load enhanced CSS with maximum accessibility"""
    st.markdown("""
    <style>
        /* Global Reset for Maximum Readability */
        * {
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Arial, sans-serif !important;
        }
        
        /* Root variables - Light backgrounds with dark text */
        :root {
            --primary-dark: #000080;  /* Navy blue for text */
            --primary: #1a1a5e;       /* Dark blue for text */
            --secondary: #8b0000;     /* Dark red for accents */
            --accent: #004d00;        /* Dark green for success */
            --warning: #cc3300;       /* Dark orange for warnings */
            --danger: #8b0000;        /* Dark red for errors */
            --success: #006400;       /* Dark green */
            --bg-white: #ffffff;      /* Pure white background */
            --bg-light: #f5f5f5;      /* Light gray background */
            --bg-lighter: #fafafa;    /* Very light gray */
            --text-black: #000000;    /* Pure black text */
            --text-navy: #000080;     /* Navy blue text */
            --text-darkred: #8b0000;  /* Dark red text */
            --border-dark: #2c2c2c;   /* Dark gray borders */
            --shadow: rgba(0, 0, 0, 0.2);
        }
        
        /* Main App - Pure White Background */
        .stApp {
            background-color: var(--bg-white) !important;
        }
        
        /* All Text - Maximum Contrast */
        p, span, div, label, h1, h2, h3, h4, h5, h6, li {
            color: var(--text-black) !important;
            font-weight: 500 !important;
            letter-spacing: 0.3px !important;
        }
        
        /* Section Headers with Icons - Force dark text on white */
        h3:has-text("📈"), h3:has-text("🎯"), h3:has-text("📊"),
        h3:contains("Financial Projection"),
        h3:contains("Component Breakdown"),
        h3:contains("Module Performance"),
        [data-testid="stMarkdownContainer"] h3 {
            color: #000080 !important;
            background-color: transparent !important;
            background: transparent !important;
        }
        
        /* Headers - Extra Bold */
        h1 { font-size: 2.5rem !important; font-weight: 900 !important; }
        h2 { font-size: 2rem !important; font-weight: 800 !important; }
        h3 { font-size: 1.75rem !important; font-weight: 700 !important; }
        h4 { font-size: 1.5rem !important; font-weight: 700 !important; }
        
        /* Main Header Block - Light background */
        .main-header {
            background: var(--bg-light) !important;
            color: var(--text-navy) !important;
            padding: 40px !important;
            border-radius: 8px !important;
            margin-bottom: 30px !important;
            border: 3px solid var(--text-navy) !important;
            box-shadow: 0 6px 12px var(--shadow) !important;
        }
        
        .header-title {
            font-size: 3rem !important;
            font-weight: 900 !important;
            color: var(--text-navy) !important;
            margin-bottom: 15px !important;
        }
        
        .header-subtitle {
            font-size: 1.5rem !important;
            font-weight: 600 !important;
            color: var(--text-darkred) !important;
        }
        
        /* Streamlit Specific Elements */
        
        /* Buttons - Light background with dark text - OVERRIDE ALL */
        .stButton > button,
        button[kind="primary"],
        button[kind="secondary"],
        .stButton button,
        div[data-testid="stHorizontalBlock"] button,
        div[data-testid="column"] button {
            background-color: var(--bg-light) !important;
            background-image: none !important;
            color: var(--text-navy) !important;
            border: 3px solid var(--text-navy) !important;
            padding: 16px 32px !important;
            font-size: 1.25rem !important;
            font-weight: 800 !important;
            border-radius: 8px !important;
            box-shadow: 0 4px 8px var(--shadow) !important;
            transition: all 0.3s ease !important;
            min-height: 60px !important;
        }
        
        .stButton > button:hover,
        button[kind="primary"]:hover,
        button[kind="secondary"]:hover,
        .stButton button:hover,
        div[data-testid="stHorizontalBlock"] button:hover,
        div[data-testid="column"] button:hover {
            background-color: var(--bg-white) !important;
            background-image: none !important;
            color: var(--text-darkred) !important;
            border-color: var(--text-darkred) !important;
            transform: translateY(-2px) !important;
            box-shadow: 0 6px 12px var(--shadow) !important;
        }
        
        .stButton > button:focus,
        button[kind="primary"]:focus,
        button[kind="secondary"]:focus {
            outline: 4px solid #ffcc00 !important;
            outline-offset: 3px !important;
        }
        
        /* Override Streamlit's default button text colors */
        .stButton > button p,
        .stButton > button span,
        .stButton > button div {
            color: var(--text-navy) !important;
        }
        
        .stButton > button:hover p,
        .stButton > button:hover span,
        .stButton > button:hover div {
            color: var(--text-darkred) !important;
        }
        
        /* Select Boxes - Enhanced visibility */
        .stSelectbox > div > div {
            border: 3px solid var(--text-navy) !important;
            border-radius: 8px !important;
            background-color: #ffffff !important;
            min-height: 50px !important;
            color: #000000 !important;
        }
        
        .stSelectbox label {
            font-size: 1.2rem !important;
            font-weight: 700 !important;
            color: var(--text-navy) !important;
            margin-bottom: 8px !important;
        }
        
        /* Dropdown menu items - CRITICAL FIX */
        .stSelectbox [data-baseweb="select"] {
            background-color: #ffffff !important;
            color: #000000 !important;
        }
        
        .stSelectbox [role="listbox"],
        .stSelectbox [role="option"],
        [data-baseweb="menu"],
        [data-baseweb="list-item"] {
            background-color: #ffffff !important;
            color: #000000 !important;
            font-weight: 600 !important;
            font-size: 1.1rem !important;
        }
        
        /* Dropdown selected item */
        .stSelectbox [aria-selected="true"],
        [data-baseweb="list-item"]:hover {
            background-color: #e6f2ff !important;
            color: #000080 !important;
            font-weight: 700 !important;
        }
        
        /* Selectbox input field text */
        .stSelectbox input,
        .stSelectbox [data-baseweb="input"] {
            color: #000000 !important;
            background-color: #ffffff !important;
            font-size: 1.2rem !important;
            font-weight: 600 !important;
        }
        
        /* Input Fields - FORCE WHITE BACKGROUNDS */
        .stTextInput > div > div > input,
        .stNumberInput > div > div > input,
        .stNumberInput input,
        input[type="number"],
        input[type="text"] {
            font-size: 1.25rem !important;
            padding: 12px 16px !important;
            border: 3px solid var(--text-navy) !important;
            border-radius: 8px !important;
            background-color: #ffffff !important;
            background: #ffffff !important;
            color: #000000 !important;
            font-weight: 600 !important;
            min-height: 50px !important;
        }
        
        /* Number Input Buttons - Remove black backgrounds */
        .stNumberInput > div > div > div > button,
        .step-up,
        .step-down,
        button[title="Decrement"],
        button[title="Increment"] {
            background-color: #f5f5f5 !important;
            background: #f5f5f5 !important;
            color: #000080 !important;
            border: 2px solid #000080 !important;
        }
        
        .stNumberInput > div > div > div > button:hover {
            background-color: #ffffff !important;
            background: #ffffff !important;
            color: #8b0000 !important;
            border-color: #8b0000 !important;
        }
        
        .stTextInput > div > div > input:focus,
        .stNumberInput > div > div > input:focus {
            border-color: var(--text-darkred) !important;
            outline: 3px solid rgba(139, 0, 0, 0.2) !important;
            outline-offset: 2px !important;
        }
        
        /* File Uploader - More Prominent */
        .stFileUploader {
            border: 3px dashed var(--text-navy) !important;
            border-radius: 12px !important;
            padding: 30px !important;
            background-color: var(--bg-lighter) !important;
        }
        
        .stFileUploader > div {
            min-height: 120px !important;
        }
        
        .stFileUploader label {
            font-size: 1.3rem !important;
            font-weight: 700 !important;
            color: var(--text-navy) !important;
        }
        
        /* Sliders */
        .stSlider label {
            font-size: 1.2rem !important;
            font-weight: 700 !important;
            color: var(--text-navy) !important;
            margin-bottom: 10px !important;
        }
        
        /* Slider track */
        .stSlider > div > div > div > div {
            background-color: var(--text-navy) !important;
            height: 8px !important;
        }
        
        /* Slider thumb - make it a triangle */
        .stSlider > div > div > div > div > div {
            width: 0 !important;
            height: 0 !important;
            background-color: transparent !important;
            border-left: 12px solid transparent !important;
            border-right: 12px solid transparent !important;
            border-bottom: 20px solid var(--text-navy) !important;
            border-top: none !important;
            margin-top: -10px !important;
        }
        
        /* Slider value display - make it more visible */
        .stSlider > div > div > div:last-child {
            margin-top: 5px !important;
        }
        
        .stSlider [data-testid="stTickBarMin"],
        .stSlider [data-testid="stTickBarMax"],
        .stSlider [data-testid="stThumbValue"] {
            font-size: 1.3rem !important;
            font-weight: 800 !important;
            color: var(--text-navy) !important;
            background-color: transparent !important;
        }
        
        /* Metric Cards */
        .metric-card {
            background: var(--bg-white) !important;
            border: 3px solid var(--text-navy) !important;
            border-radius: 12px !important;
            padding: 30px !important;
            box-shadow: 0 4px 8px var(--shadow) !important;
            margin-bottom: 20px !important;
        }
        
        .metric-value {
            font-size: 3rem !important;
            font-weight: 900 !important;
            color: var(--text-navy) !important;
            margin-bottom: 10px !important;
        }
        
        .metric-label {
            font-size: 1.3rem !important;
            font-weight: 700 !important;
            color: var(--text-black) !important;
            text-transform: uppercase !important;
        }
        
        /* Info/Alert Boxes */
        .stAlert {
            border: 3px solid var(--primary-dark) !important;
            border-radius: 8px !important;
            padding: 20px !important;
            font-size: 1.2rem !important;
            font-weight: 600 !important;
            background-color: white !important;
            color: var(--text-black) !important;
        }
        
        /* Sidebar */
        section[data-testid="stSidebar"] {
            background-color: var(--bg-lighter) !important;
            border-right: 3px solid var(--text-navy) !important;
        }
        
        section[data-testid="stSidebar"] * {
            font-size: 1.15rem !important;
            font-weight: 600 !important;
            color: var(--text-black) !important;
        }
        
        /* CRITICAL: Additional dropdown fixes for ALL selectbox elements */
        div[data-baseweb="select"] > div,
        div[role="combobox"],
        div[data-baseweb="popover"],
        .st-emotion-cache-10trblm {
            background-color: #ffffff !important;
            color: #000000 !important;
        }
        
        /* Fix dropdown menu background and text */
        [data-baseweb="menu"],
        [data-baseweb="list"],
        div[role="listbox"] {
            background-color: #ffffff !important;
            border: 2px solid #000080 !important;
        }
        
        /* Each dropdown option */
        [data-baseweb="menu"] li,
        [role="option"],
        div[role="option"] {
            color: #000000 !important;
            background-color: #ffffff !important;
            padding: 12px !important;
            font-size: 1.2rem !important;
            font-weight: 600 !important;
            border-bottom: 1px solid #e0e0e0 !important;
        }
        
        /* Hover state for dropdown options */
        [data-baseweb="menu"] li:hover,
        [role="option"]:hover {
            background-color: #e6f2ff !important;
            color: #000080 !important;
            font-weight: 700 !important;
        }
        
        /* Selected dropdown option */
        [aria-selected="true"],
        [data-highlighted="true"] {
            background-color: #d4e5ff !important;
            color: #000080 !important;
            font-weight: 800 !important;
        }
        
        /* Tabs */
        .stTabs [data-baseweb="tab-list"] {
            background-color: var(--bg-light) !important;
            border: 2px solid var(--text-navy) !important;
            border-radius: 8px !important;
            padding: 4px !important;
        }
        
        .stTabs [data-baseweb="tab"] {
            font-size: 1.2rem !important;
            font-weight: 700 !important;
            color: var(--text-navy) !important;
            padding: 12px 24px !important;
        }
        
        .stTabs [aria-selected="true"] {
            background-color: var(--bg-white) !important;
            color: var(--text-darkred) !important;
            border: 2px solid var(--text-darkred) !important;
            border-radius: 6px !important;
        }
        
        /* Expander */
        .streamlit-expanderHeader {
            font-size: 1.3rem !important;
            font-weight: 700 !important;
            color: var(--text-navy) !important;
            background-color: var(--bg-light) !important;
            border: 2px solid var(--text-navy) !important;
            border-radius: 8px !important;
            padding: 16px !important;
        }
        
        .streamlit-expanderHeader:hover {
            background-color: var(--bg-white) !important;
            color: var(--text-darkred) !important;
        }
        
        /* Data Tables - MUCH LARGER text for accessibility - NO BLACK */
        .stDataFrame {
            border: 3px solid #000080 !important;
            border-radius: 8px !important;
            background-color: #ffffff !important;
            background: #ffffff !important;
        }
        
        .stDataFrame th {
            background-color: #f5f5f5 !important;
            background: #f5f5f5 !important;
            color: #000080 !important;
            font-weight: 900 !important;
            font-size: 1.8rem !important;
            padding: 20px !important;
            border-bottom: 3px solid #000080 !important;
            text-transform: uppercase !important;
            letter-spacing: 0.5px !important;
        }
        
        .stDataFrame td {
            font-size: 1.7rem !important;
            font-weight: 700 !important;
            padding: 18px !important;
            color: #000000 !important;
            background-color: #ffffff !important;
            background: #ffffff !important;
            line-height: 1.8 !important;
        }
        
        /* Specific styling for dataframe cells */
        .stDataFrame tbody tr:hover {
            background-color: var(--bg-lighter) !important;
        }
        
        /* Force ALL dataframe text to be larger and NEVER white on black */
        [data-testid="stDataFrame"] *,
        [data-testid="stDataFrameResizable"] *,
        .dataframe * {
            font-size: 1.7rem !important;
            font-weight: 700 !important;
            color: #000000 !important;
            background-color: transparent !important;
        }
        
        [data-testid="stDataFrame"] th,
        [data-testid="stDataFrameResizable"] th,
        .dataframe th {
            font-size: 1.8rem !important;
            font-weight: 900 !important;
            color: #000080 !important;
            background-color: #f5f5f5 !important;
            background: #f5f5f5 !important;
        }
        
        [data-testid="stDataFrame"] td,
        [data-testid="stDataFrameResizable"] td,
        .dataframe td {
            color: #000000 !important;
            background-color: #ffffff !important;
            background: #ffffff !important;
        }
        
        /* Override Streamlit's default dataframe styles */
        div[data-testid="stDataFrame"] div[data-testid="stDataFrameContent"] table {
            font-size: 1.7rem !important;
        }
        
        div[data-testid="stDataFrame"] div[data-testid="stDataFrameContent"] th {
            font-size: 1.8rem !important;
            padding: 20px !important;
        }
        
        div[data-testid="stDataFrame"] div[data-testid="stDataFrameContent"] td {
            font-size: 1.7rem !important;
            padding: 18px !important;
        }
        
        /* Focus Indicators for All Interactive Elements */
        *:focus {
            outline: 4px solid #ffcc00 !important;
            outline-offset: 2px !important;
        }
        
        /* Remove Streamlit Branding for Cleaner Look */
        .css-1y4p8pa {
            display: none !important;
        }
        
        /* Make Links More Visible */
        a {
            color: var(--secondary) !important;
            font-weight: 700 !important;
            text-decoration: underline !important;
        }
        
        a:hover {
            color: var(--warning) !important;
        }
        
        /* Ensure Plotly Charts Have White Backgrounds and Good Contrast */
        .js-plotly-plot .plotly {
            font-weight: 600 !important;
            background-color: #ffffff !important;
        }
        
        /* Force Plotly charts to have white backgrounds */
        .js-plotly-plot,
        .plotly,
        .plot-container,
        .svg-container,
        .main-svg,
        .bg {
            background-color: #ffffff !important;
            background: #ffffff !important;
        }
        
        /* Plotly specific overrides */
        .plotly .bg {
            fill: #ffffff !important;
        }
        
        .plotly-graph-div {
            background-color: #ffffff !important;
            background: #ffffff !important;
        }
        
        /* Chart containers should be white */
        .chart-container {
            background-color: #ffffff !important;
            background: #ffffff !important;
            border: 2px solid #000080 !important;
        }
        
        /* Streamlit native charts - force light theme */
        canvas {
            background-color: #ffffff !important;
        }
        
        .stPlotlyChart,
        [data-testid="stVegaLiteChart"] {
            background-color: #ffffff !important;
        }
        
        /* Vega-Lite charts (used by st.line_chart, st.area_chart, st.bar_chart) */
        .vega-embed {
            background-color: #ffffff !important;
        }
        
        .vega-embed .marks {
            fill: #000080 !important;
            stroke: #000080 !important;
        }
        
        .vega-embed .mark-line {
            stroke: #000080 !important;
            stroke-width: 3 !important;
        }
        
        .vega-embed .mark-area {
            fill: #000080 !important;
            fill-opacity: 0.3 !important;
        }
        
        .vega-embed .mark-rect {
            fill: #000080 !important;
        }
        
        .vega-embed .mark-text {
            fill: #000000 !important;
            font-weight: bold !important;
        }
        
        /* Override Vega axis and grid */
        .vega-embed .domain {
            stroke: #000000 !important;
            stroke-width: 2 !important;
        }
        
        .vega-embed .tick line {
            stroke: #333333 !important;
        }
        
        .vega-embed .tick text {
            fill: #000000 !important;
            font-size: 12px !important;
            font-weight: 600 !important;
        }
        
        .vega-embed .grid line {
            stroke: #cccccc !important;
            stroke-dasharray: 2,2 !important;
        }
        
        .vega-embed .background {
            fill: #ffffff !important;
        }
        
        /* Force chart container backgrounds */
        div:has(> canvas),
        div:has(> .vega-embed) {
            background-color: #ffffff !important;
        }
        
        /* Custom Classes for Special Elements */
        .high-priority {
            border: 4px solid var(--danger) !important;
            background-color: #fff5f5 !important;
        }
        
        /* Performance Metrics Tables - EXTRA LARGE Text */
        .performance-metrics table,
        div[data-testid="stTable"] table {
            font-size: 1.8rem !important;
        }
        
        .performance-metrics th,
        div[data-testid="stTable"] th {
            font-size: 2rem !important;
            font-weight: 900 !important;
            padding: 22px !important;
        }
        
        .performance-metrics td,
        div[data-testid="stTable"] td {
            font-size: 1.8rem !important;
            font-weight: 700 !important;
            padding: 20px !important;
        }
        
        /* AGGRESSIVE OVERRIDE for all table elements - NO BLACK BACKGROUNDS */
        table {
            font-size: 1.7rem !important;
            background-color: #ffffff !important;
            background: #ffffff !important;
        }
        
        th {
            font-size: 1.8rem !important;
            font-weight: 900 !important;
            color: #000080 !important;
            background-color: #f5f5f5 !important;
            background: #f5f5f5 !important;
            padding: 20px !important;
        }
        
        td {
            font-size: 1.7rem !important;
            font-weight: 700 !important;
            color: #000000 !important;
            background-color: #ffffff !important;
            background: #ffffff !important;
            padding: 18px !important;
        }
        
        /* Override any dark table styles */
        table[class*="dark"],
        table[style*="background-color: black"],
        table[style*="background: black"],
        table[style*="background-color: #000"],
        table[style*="background: #000"] {
            background-color: #ffffff !important;
            background: #ffffff !important;
        }
        
        th[style*="color: white"],
        th[style*="color: #fff"],
        td[style*="color: white"],
        td[style*="color: #fff"] {
            color: #000000 !important;
        }
        
        /* Target Streamlit's generated table classes */
        .css-1v0mbdj, .css-115wg9t {
            font-size: 1.7rem !important;
            background-color: #ffffff !important;
            color: #000000 !important;
        }
        
        /* Make sure table content is never small or white on black */
        tbody *, thead *, tfoot * {
            font-size: inherit !important;
            font-weight: 700 !important;
            color: #000000 !important;
            background-color: transparent !important;
        }
        
        /* Force table rows to have white background */
        tr {
            background-color: #ffffff !important;
            background: #ffffff !important;
        }
        
        tr:nth-child(even) {
            background-color: #fafafa !important;
            background: #fafafa !important;
        }
        
        tr:hover {
            background-color: #f0f0f0 !important;
            background: #f0f0f0 !important;
        }
        
        .visn21-highlight {
            background: var(--bg-light) !important;
            color: var(--text-navy) !important;
            padding: 25px !important;
            border-radius: 12px !important;
            border: 4px solid var(--text-darkred) !important;
            box-shadow: 0 6px 12px var(--shadow) !important;
            text-align: center !important;
        }
        
        .visn21-highlight h3 {
            color: var(--text-darkred) !important;
            font-size: 1.8rem !important;
            font-weight: 900 !important;
            margin-bottom: 15px !important;
        }
        
        .visn21-highlight p {
            color: var(--text-black) !important;
            font-size: 1.3rem !important;
            font-weight: 600 !important;
        }
        
        /* AGGRESSIVE OVERRIDES - Remove ALL black backgrounds */
        button {
            background-color: var(--bg-light) !important;
            background-image: none !important;
            color: var(--text-navy) !important;
        }
        
        /* Target all button elements regardless of nesting */
        [role="button"],
        [type="button"],
        button,
        .stButton > button,
        .stDownloadButton > button,
        div[data-testid*="column"] button,
        div.row-widget button,
        div.block-container button {
            background: var(--bg-light) !important;
            background-color: var(--bg-light) !important;
            background-image: none !important;
            color: var(--text-navy) !important;
            border: 3px solid var(--text-navy) !important;
        }
        
        /* Remove any gradient backgrounds */
        button[kind="primary"],
        button[kind="secondary"],
        .stButton > button[kind="primary"],
        .stButton > button[kind="secondary"] {
            background: var(--bg-light) !important;
            background-image: none !important;
            background-color: var(--bg-light) !important;
        }
        
        /* Ensure download buttons also follow the scheme */
        .stDownloadButton > button {
            background-color: var(--bg-white) !important;
            color: var(--text-navy) !important;
            border: 3px solid var(--text-navy) !important;
        }
        
        .stDownloadButton > button:hover {
            background-color: var(--bg-light) !important;
            color: var(--text-darkred) !important;
            border-color: var(--text-darkred) !important;
        }
        
        /* Remove black from any metric elements */
        [data-testid="metric-container"] {
            background-color: var(--bg-white) !important;
        }
        
        /* Ensure all text in buttons is visible */
        button * {
            color: inherit !important;
        }
        
        /* Radio buttons and checkboxes */
        .stRadio > div,
        .stCheckbox > div {
            color: var(--text-navy) !important;
        }
        
        /* Remove any remaining dark backgrounds */
        div[class*="css-"] {
            background-color: transparent !important;
        }
        
        /* Fix Streamlit Deploy button visibility */
        [data-testid="stToolbar"],
        [data-testid="stToolbarActions"],
        .stDeployButton,
        [title*="Deploy"],
        button[title*="Deploy"] {
            background-color: var(--bg-white) !important;
        }
        
        /* Deploy button menu items */
        [data-testid="stToolbarActionButton"],
        [data-testid="stPopover"],
        div[data-baseweb="popover"],
        div[role="tooltip"] {
            background-color: #ffffff !important;
            color: #000000 !important;
            border: 2px solid #000080 !important;
        }
        
        /* Deploy menu text */
        [data-testid="stPopover"] *,
        div[data-baseweb="popover"] *,
        div[role="tooltip"] * {
            color: #000000 !important;
            background-color: transparent !important;
            font-weight: 600 !important;
        }
        
        /* Force all input containers to have white backgrounds */
        .stNumberInput,
        .stTextInput,
        div[data-baseweb="input"],
        div[data-testid*="stNumberInput"],
        div[data-testid*="stTextInput"] {
            background-color: transparent !important;
        }
        
        /* Ensure ALL number inputs have white backgrounds */
        .stNumberInput * {
            background-color: transparent !important;
        }
        
        .stNumberInput input {
            background-color: #ffffff !important;
            background: #ffffff !important;
        }
        
        /* Override any inline styles on inputs */
        input[style*="background"] {
            background-color: #ffffff !important;
            background: #ffffff !important;
        }
        
        /* But keep white/light backgrounds where needed */
        .stApp,
        .main,
        .block-container,
        .element-container,
        .row-widget,
        .css-1d391kg,
        [data-testid="stAppViewContainer"],
        [data-testid="stHeader"],
        [data-testid="stToolbar"],
        [data-testid="stDecoration"],
        [data-testid="stStatusWidget"],
        [data-testid="block-container"] {
            background-color: var(--bg-white) !important;
        }
        
        section[data-testid="stSidebar"] {
            background-color: var(--bg-lighter) !important;
        }
        
        /* Ensure all markdown containers have white backgrounds */
        [data-testid="stMarkdownContainer"] {
            background-color: transparent !important;
        }
        
        /* Fix any sections that might have dark backgrounds */
        .stPlotlyChart,
        [data-testid="stPlotlyChart"],
        [data-testid="stDataFrame"],
        [data-testid="stTable"] {
            background-color: #ffffff !important;
            background: #ffffff !important;
        }
        
        /* Remove any dark overlays or backgrounds from chart areas */
        div:has(> .js-plotly-plot),
        div:has(> [data-testid="stPlotlyChart"]) {
            background-color: #ffffff !important;
            background: #ffffff !important;
        }
    </style>
    """, unsafe_allow_html=True)