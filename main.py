"""
Bitscopic ROI Calculator
Unified interface for PraediGene and PraediAlert ROI calculations
Version 1.1 - Improved responsive design
"""

import streamlit as st
import pandas as pd
import numpy as np
from pathlib import Path
import sys
from datetime import datetime

# Add project directories to path
sys.path.append(str(Path(__file__).parent))

from config.defaults import BITSCOPIC_COLORS, PRAEDIGENE_DEFAULTS, PRAEDIALERT_DEFAULTS, FINANCIAL_DEFAULTS
from ui.styles import load_css
from ui.enhanced_accessibility_styles import load_enhanced_css
from ui.dashboard import show_dashboard
from calculators.praedigene_calculator import PraediGeneCalculator
from calculators.praedialert_calculator import PraediAlertCalculator
from calculators.praedialert_calculator_enhanced import PraediAlertCalculatorEnhanced
from utils.data_loader import DataLoader
from utils.export_handler import ExportHandler
from utils.export_handler_enhanced import EnhancedExportHandler

# Page configuration with light theme
st.set_page_config(
    page_title="Bitscopic ROI Calculator",
    page_icon="💰",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Force light theme for native charts
st.markdown("""
<style>
    /* Override Streamlit's native chart dark theme */
    [data-testid="stVegaLiteChart"] {
        background-color: white !important;
    }
    
    /* Force Vega-Lite to use light theme */
    .vega-embed {
        background-color: white !important;
    }
    
    .vega-embed .vega-themes-light {
        background-color: white !important;
    }
</style>
""", unsafe_allow_html=True)

def initialize_session_state():
    """Initialize session state variables"""
    if 'product_selection' not in st.session_state:
        st.session_state.product_selection = None
    if 'organization_type' not in st.session_state:
        st.session_state.organization_type = None
    if 'custom_data_loaded' not in st.session_state:
        st.session_state.custom_data_loaded = False
    if 'roi_results' not in st.session_state:
        st.session_state.roi_results = None
    if 'view_mode' not in st.session_state:
        st.session_state.view_mode = 'executive'

def show_product_selection():
    """Display product selection interface"""
    st.markdown("""
    <div class="welcome-header">
        <h1 style="color: #000080; font-size: 3.5em; margin-bottom: 20px; font-weight: 900;">
            Bitscopic ROI Calculator
        </h1>
        <p style="color: #8b0000; font-size: 1.8em; margin-bottom: 30px; font-weight: 700;">
            Select Your Product Platform
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        if st.button(
            "🧬 **PraediGene**\n\n"
            "Genetic testing and precision medicine ROI\n\n"
            "• PGx (Pharmacogenomics)\n"
            "• TSO500 (Tumor Sequencing)\n"
            "• BIAS2015 (Bioinformatics)\n"
            "• Cytogenetics",
            key="praedigene_btn",
            use_container_width=True,
            help="Calculate ROI for genetic testing pipelines"
        ):
            st.session_state.product_selection = 'praedigene'
            st.rerun()
    
    with col2:
        if st.button(
            "🏥 **PraediAlert**\n\n"
            "Clinical surveillance and infection control ROI\n\n"
            "• IPC Surveillance\n"
            "• Antimicrobial Stewardship\n"
            "• Regulatory Reporting\n"
            "• HAI Reduction",
            key="praedialert_btn",
            use_container_width=True,
            help="Calculate ROI for clinical surveillance modules"
        ):
            st.session_state.product_selection = 'praedialert'
            st.rerun()
    
    # Information cards with better contrast
    st.markdown("---")
    st.markdown("### 📊 Key Features")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("""
        <div style="background: white; border: 3px solid #000080; border-radius: 8px; padding: 25px; min-height: 250px;">
            <h4 style="color: #000080; margin-bottom: 20px; font-size: 1.4em;">📥 Data Import</h4>
            <ul style="color: #000; font-size: 1.15em; font-weight: 500; line-height: 2.0; margin: 0; padding-left: 20px;">
                <li style="margin-bottom: 10px;">CSV file upload</li>
                <li style="margin-bottom: 10px;">VISN21 templates</li>
                <li style="margin-bottom: 10px;">Custom parameters</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div style="background: white; border: 3px solid #006400; border-radius: 8px; padding: 25px; min-height: 250px;">
            <h4 style="color: #006400; margin-bottom: 20px; font-size: 1.4em;">📈 Analysis</h4>
            <ul style="color: #000; font-size: 1.15em; font-weight: 500; line-height: 2.0; margin: 0; padding-left: 20px;">
                <li style="margin-bottom: 10px;">Monthly trends</li>
                <li style="margin-bottom: 10px;">Annual projections</li>
                <li style="margin-bottom: 10px;">Sensitivity analysis</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown("""
        <div style="background: white; border: 3px solid #8b0000; border-radius: 8px; padding: 25px; min-height: 250px;">
            <h4 style="color: #8b0000; margin-bottom: 20px; font-size: 1.4em;">📤 Export Options</h4>
            <ul style="color: #000; font-size: 1.15em; font-weight: 500; line-height: 2.0; margin: 0; padding-left: 20px;">
                <li style="margin-bottom: 10px;">Executive reports</li>
                <li style="margin-bottom: 10px;">Detailed analytics</li>
                <li style="margin-bottom: 10px;">Excel workbooks</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)

def show_organization_setup():
    """Display organization setup interface"""
    st.markdown("### 🏢 Organization Setup")
    
    # Prominent VISN21 data loading option
    st.markdown("---")
    col1, col2, col3 = st.columns([1, 2, 1])
    
    with col2:
        st.markdown("""
        <div class="visn21-highlight">
            <h3>📊 Quick Start with VISN21 Data</h3>
            <p>Load pre-configured VA hospital network data including 6 facilities, HAI rates, and antibiotic usage metrics</p>
        </div>
        """, unsafe_allow_html=True)
        
        if st.button("🚀 **LOAD VISN21 SAMPLE DATA**", 
                     use_container_width=True,
                     help="Click to instantly load VISN21 data with all metrics"):
            st.session_state.organization_type = 'visn21'
            data_loader = DataLoader()
            if data_loader.load_visn21_sample_data():
                st.session_state.custom_data_loaded = True
                st.success("✅ VISN21 sample data loaded successfully!")
                st.rerun()
    
    st.markdown("---")
    
    # Regular organization selection
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.markdown("#### Or Select Organization Type")
        org_type = st.selectbox(
            "Choose your organization",
            ["VISN21", "Small Hospital", "Medium Hospital", "Large Hospital", "Custom"],
            index=0,  # VISN21 is now default (index 0)
            help="Choose your organization type for default parameters"
        )
        
        if org_type:
            # Handle VISN21 specially to preserve case
            if org_type == "VISN21":
                st.session_state.organization_type = 'visn21'
            else:
                st.session_state.organization_type = org_type.lower().replace(" ", "_")
    
    with col2:
        st.markdown("#### Upload Custom Data")
        uploaded_file = st.file_uploader(
            "Upload CSV/Excel file",
            type=['csv', 'xlsx'],
            help="Upload facility-specific data"
        )
        
        if uploaded_file:
            data_loader = DataLoader()
            if data_loader.load_custom_data(uploaded_file):
                st.session_state.custom_data_loaded = True
                st.success("✅ Custom data loaded successfully!")

def main():
    """Main application function"""
    # Load Enhanced Accessibility CSS
    load_enhanced_css()
    
    # Initialize session state
    initialize_session_state()
    
    # Sidebar navigation
    with st.sidebar:
        st.markdown("## 🧭 Navigation")
        
        if st.session_state.product_selection:
            st.markdown(f"**Product:** {st.session_state.product_selection.upper()}")
            
            if st.button("🔄 Change Product"):
                st.session_state.product_selection = None
                st.session_state.roi_results = None
                st.rerun()
        
        if st.session_state.organization_type:
            # Display organization type properly - handle VISN21 specially
            org_display = 'VISN21' if st.session_state.organization_type == 'visn21' else st.session_state.organization_type.replace('_', ' ').title()
            st.markdown(f"**Organization:** {org_display}")
        
        st.markdown("---")
        
        # View mode selection
        if st.session_state.product_selection and st.session_state.organization_type:
            st.markdown("### 👁️ View Mode")
            
            # Get current index based on session state
            view_options = ["Executive Summary", "Detailed Analysis", "Comparison View"]
            current_index = 0
            if 'view_mode' in st.session_state:
                mode_map = {
                    'executive_summary': 0,
                    'detailed_analysis': 1,
                    'comparison_view': 2
                }
                current_index = mode_map.get(st.session_state.view_mode, 0)
            
            view_mode = st.radio(
                "Select Dashboard",
                view_options,
                index=current_index,
                key="view_mode_radio"
            )
            
            # Update session state if changed
            new_mode = view_mode.lower().replace(" ", "_")
            if st.session_state.view_mode != new_mode:
                st.session_state.view_mode = new_mode
                st.rerun()
            
            # Export options
            st.markdown("---")
            st.markdown("### 📤 Export")
            
            # Use enhanced export handler for comprehensive reports
            export_handler = EnhancedExportHandler()
            
            # Initialize report generation state
            if 'report_generated' not in st.session_state:
                st.session_state.report_generated = False
            if 'report_data' not in st.session_state:
                st.session_state.report_data = None
            
            # Single button that generates and immediately shows download
            # Check if we have the necessary selections to calculate ROI
            if st.session_state.product_selection and st.session_state.organization_type:
                # Generate report on button click
                report_button = st.button("📄 Generate & Download Report", type="primary", key="gen_report_btn")
                
                if report_button:
                    with st.spinner("Generating comprehensive report with 8-facility study data..."):
                        try:
                            # Ensure ROI results exist (they should have been calculated by now)
                            if not hasattr(st.session_state, 'roi_results') or st.session_state.roi_results is None:
                                # Force calculation if needed
                                if st.session_state.product_selection == 'praedigene':
                                    calculator = PraediGeneCalculator(st.session_state.organization_type)
                                    st.session_state.roi_results = calculator.calculate_roi()
                                else:
                                    calculator = PraediAlertCalculatorEnhanced(st.session_state.organization_type)
                                    st.session_state.roi_results = calculator.calculate_roi()
                            
                            report = export_handler.generate_comprehensive_report(
                                st.session_state.roi_results,
                                st.session_state.product_selection,
                                st.session_state.organization_type
                            )
                            st.session_state.report_data = report
                            st.session_state.report_generated = True
                        except Exception as e:
                            st.error(f"Error generating report: {str(e)}")
                
                # Show download button immediately after generation (simplified)
                if st.session_state.report_generated and st.session_state.report_data:
                    file_name = f"PraediAlert_ROI_Report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf"
                    
                    # Simple download button without extra messages
                    st.download_button(
                        label="📥 Download PDF Report",
                        data=st.session_state.report_data,
                        file_name=file_name,
                        mime="application/pdf",
                        key=f"download_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
                    )
                    
                    # Reset after showing button
                    st.session_state.report_generated = False
            else:
                st.warning("Please calculate ROI first before generating report.")
            
            if st.button("📊 Export to Excel"):
                if st.session_state.roi_results:
                    excel = export_handler.export_to_excel(
                        st.session_state.roi_results,
                        st.session_state.product_selection
                    )
                    st.download_button(
                        "⬇️ Download Excel",
                        excel,
                        "roi_analysis.xlsx",
                        "application/vnd.ms-excel"
                    )
    
    # Main content area
    if not st.session_state.product_selection:
        show_product_selection()
    elif not st.session_state.organization_type:
        show_organization_setup()
    else:
        # Calculate ROI based on product selection
        if st.session_state.product_selection == 'praedigene':
            calculator = PraediGeneCalculator(st.session_state.organization_type)
            st.session_state.roi_results = calculator.calculate_roi()
        else:
            # Use enhanced calculator with real-world study data
            calculator = PraediAlertCalculatorEnhanced(st.session_state.organization_type)
            st.session_state.roi_results = calculator.calculate_roi()
        
        # Show dashboard
        show_dashboard(
            st.session_state.roi_results,
            st.session_state.product_selection,
            st.session_state.view_mode
        )

if __name__ == "__main__":
    main()