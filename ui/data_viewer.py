"""
Data Viewer for ROI Calculator
Displays loaded CSV data in accessible format
"""

import streamlit as st
import pandas as pd
from pathlib import Path

def show_data_viewer(product_type, organization_type):
    """Display loaded data in accessible tables"""
    
    st.markdown("""
    <div class="section-header">
        📊 Source Data Viewer
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("""
    <p style="font-size: 1.3rem; font-weight: 600; color: #000080; margin-bottom: 20px;">
        View the actual data being used in ROI calculations. This helps you understand the baseline metrics and make informed adjustments.
    </p>
    """, unsafe_allow_html=True)
    
    # Check if VISN21 data is loaded
    if organization_type == 'visn21':
        show_visn21_data()
    else:
        st.info("📌 No external data loaded. Using default parameters for calculations.")
        show_default_parameters(product_type, organization_type)

def show_visn21_data():
    """Display VISN21 data files in formatted tables"""
    
    data_path = Path(__file__).parent.parent / 'data'
    
    # Create tabs for different data files
    tab1, tab2, tab3 = st.tabs([
        "🏥 Facility Bed Days",
        "🦠 HAI Rates", 
        "💊 Antibiotic DOT"
    ])
    
    with tab1:
        show_bed_days_data(data_path)
    
    with tab2:
        show_hai_rates_data(data_path)
    
    with tab3:
        show_antibiotic_dot_data(data_path)

def show_bed_days_data(data_path):
    """Display patient bed days data"""
    
    st.markdown("### 🏥 Patient Bed Days by Facility")
    st.markdown("""
    <p style="font-size: 1.2rem; font-weight: 600; color: #333; margin-bottom: 15px;">
        Annual patient bed days for each VISN21 facility. This data is used to calculate HAI rates and potential savings.
    </p>
    """, unsafe_allow_html=True)
    
    try:
        df = pd.read_csv(data_path / 'visn21_patient_bed_days.csv')
        
        # Format the numbers and rename columns to title case
        df['bed_days_annual'] = df['bed_days_annual'].apply(lambda x: f"{x:,}")
        df = df.rename(columns={
            'facility': 'Facility',
            'facility_code': 'Facility Code', 
            'bed_days_annual': 'Annual Bed Days'
        })
        
        # Create HTML table with accessibility styling
        html_table = df.to_html(index=False, escape=False)
        html_table = html_table.replace('<table', '<table style="background-color: white !important; width: 100%; border-collapse: collapse;"')
        html_table = html_table.replace('<th', '<th style="background-color: #f5f5f5 !important; color: #000080 !important; padding: 20px !important; font-size: 1.8rem !important; font-weight: 900 !important; border: 2px solid #000080 !important; text-align: left;"')
        html_table = html_table.replace('<td', '<td style="background-color: white !important; color: black !important; padding: 18px !important; font-size: 1.7rem !important; font-weight: 700 !important; border: 1px solid #ddd !important;"')
        
        st.markdown(html_table, unsafe_allow_html=True)
        
        # Summary metrics
        st.markdown("### 📈 Summary Statistics")
        col1, col2, col3 = st.columns(3)
        
        # Reload for calculations
        df_calc = pd.read_csv(data_path / 'visn21_patient_bed_days.csv')
        
        with col1:
            total_beds = df_calc['bed_days_annual'].sum()
            st.markdown(f"""
            <div class="metric-card">
                <div class="metric-value">{total_beds:,}</div>
                <div class="metric-label">Total Annual Bed Days</div>
            </div>
            """, unsafe_allow_html=True)
        
        with col2:
            avg_beds = df_calc[df_calc['facility'] != 'VISN 21']['bed_days_annual'].mean()
            st.markdown(f"""
            <div class="metric-card">
                <div class="metric-value">{avg_beds:,.0f}</div>
                <div class="metric-label">Average per Facility</div>
            </div>
            """, unsafe_allow_html=True)
        
        with col3:
            num_facilities = len(df_calc[df_calc['facility'] != 'VISN 21'])
            st.markdown(f"""
            <div class="metric-card">
                <div class="metric-value">{num_facilities}</div>
                <div class="metric-label">Number of Facilities</div>
            </div>
            """, unsafe_allow_html=True)
            
    except FileNotFoundError:
        st.warning("Patient bed days data file not found")
    except Exception as e:
        st.error(f"Error loading bed days data: {str(e)}")

def show_hai_rates_data(data_path):
    """Display HAI rates data"""
    
    st.markdown("### 🦠 Healthcare-Associated Infection (HAI) Rates")
    st.markdown("""
    <p style="font-size: 1.2rem; font-weight: 600; color: #333; margin-bottom: 15px;">
        Rolling 12-month HAI rates by type and facility. These baseline rates determine potential infection prevention savings.
    </p>
    """, unsafe_allow_html=True)
    
    try:
        df = pd.read_csv(data_path / 'visn21_hai_rates.csv')
        
        # Group by HAI type for better visualization
        hai_types = df['hai_type'].unique()
        
        for hai_type in hai_types:
            st.markdown(f"#### {hai_type} Rates")
            
            hai_df = df[df['hai_type'] == hai_type][['facility', 'rolling_12_months_rate', 'unit_of_measure']].copy()
            hai_df['rolling_12_months_rate'] = hai_df['rolling_12_months_rate'].apply(lambda x: f"{x:.2f}")
            
            # Rename columns to title case
            hai_df = hai_df.rename(columns={
                'facility': 'Facility',
                'rolling_12_months_rate': 'Rolling 12 Months Rate',
                'unit_of_measure': 'Unit of Measure'
            })
            
            # Create HTML table
            html_table = hai_df.to_html(index=False, escape=False)
            html_table = html_table.replace('<table', '<table style="background-color: white !important; width: 100%; border-collapse: collapse; margin-bottom: 30px;"')
            html_table = html_table.replace('<th', '<th style="background-color: #f5f5f5 !important; color: #000080 !important; padding: 20px !important; font-size: 1.8rem !important; font-weight: 900 !important; border: 2px solid #000080 !important; text-align: left;"')
            html_table = html_table.replace('<td', '<td style="background-color: white !important; color: black !important; padding: 18px !important; font-size: 1.7rem !important; font-weight: 700 !important; border: 1px solid #ddd !important;"')
            
            st.markdown(html_table, unsafe_allow_html=True)
        
        # Summary by HAI type
        st.markdown("### 📊 HAI Type Summary")
        summary_data = []
        
        for hai_type in hai_types:
            hai_data = df[df['hai_type'] == hai_type]
            # Exclude VISN21 aggregate from average calculation
            facility_data = hai_data[hai_data['facility'] != 'VISN21']
            
            summary_data.append({
                'HAI Type': hai_type,
                'Average Rate': f"{facility_data['rolling_12_months_rate'].mean():.2f}",
                'Max Rate': f"{facility_data['rolling_12_months_rate'].max():.2f}",
                'Min Rate': f"{facility_data['rolling_12_months_rate'].min():.2f}",
                'Facilities with >0': f"{(facility_data['rolling_12_months_rate'] > 0).sum()}"
            })
        
        summary_df = pd.DataFrame(summary_data)
        
        # Create HTML table
        html_table = summary_df.to_html(index=False, escape=False)
        html_table = html_table.replace('<table', '<table style="background-color: white !important; width: 100%; border-collapse: collapse;"')
        html_table = html_table.replace('<th', '<th style="background-color: #f5f5f5 !important; color: #000080 !important; padding: 20px !important; font-size: 1.8rem !important; font-weight: 900 !important; border: 2px solid #000080 !important; text-align: left;"')
        html_table = html_table.replace('<td', '<td style="background-color: white !important; color: black !important; padding: 18px !important; font-size: 1.7rem !important; font-weight: 700 !important; border: 1px solid #ddd !important;"')
        
        st.markdown(html_table, unsafe_allow_html=True)
        
    except FileNotFoundError:
        st.warning("HAI rates data file not found")
    except Exception as e:
        st.error(f"Error loading HAI rates data: {str(e)}")

def show_antibiotic_dot_data(data_path):
    """Display antibiotic DOT data"""
    
    st.markdown("### 💊 Antibiotic Days of Therapy (DOT)")
    st.markdown("""
    <p style="font-size: 1.2rem; font-weight: 600; color: #333; margin-bottom: 15px;">
        Quarterly antibiotic usage rates per 1000 patient days. This data drives antimicrobial stewardship savings calculations.
    </p>
    """, unsafe_allow_html=True)
    
    try:
        df = pd.read_csv(data_path / 'visn21_antibiotic_dot.csv')
        
        # Create quarterly trend view
        quarters = df.groupby(['quarter', 'year']).agg({
            'dot_per_1000_days': ['mean', 'min', 'max']
        }).round(2)
        
        # Facility-specific view
        st.markdown("#### Facility DOT by Quarter")
        
        for facility in df['facility'].unique():
            facility_df = df[df['facility'] == facility][['quarter', 'year', 'dot_per_1000_days']].copy()
            facility_df['Quarter'] = facility_df['quarter'] + ' ' + facility_df['year'].astype(str)
            facility_df['DOT per 1000 Days'] = facility_df['dot_per_1000_days'].apply(lambda x: f"{x:.2f}")
            facility_df = facility_df[['Quarter', 'DOT per 1000 Days']]
            
            st.markdown(f"**{facility}**")
            
            # Create HTML table
            html_table = facility_df.to_html(index=False, escape=False)
            html_table = html_table.replace('<table', '<table style="background-color: white !important; width: 60%; border-collapse: collapse; margin-bottom: 20px;"')
            html_table = html_table.replace('<th', '<th style="background-color: #f5f5f5 !important; color: #000080 !important; padding: 15px !important; font-size: 1.6rem !important; font-weight: 900 !important; border: 2px solid #000080 !important; text-align: left;"')
            html_table = html_table.replace('<td', '<td style="background-color: white !important; color: black !important; padding: 12px !important; font-size: 1.5rem !important; font-weight: 700 !important; border: 1px solid #ddd !important;"')
            
            st.markdown(html_table, unsafe_allow_html=True)
        
        # Overall summary
        st.markdown("### 📈 DOT Summary Statistics")
        
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            overall_avg = df['dot_per_1000_days'].mean()
            st.markdown(f"""
            <div class="metric-card">
                <div class="metric-value">{overall_avg:.1f}</div>
                <div class="metric-label">Average DOT/1000 Days</div>
            </div>
            """, unsafe_allow_html=True)
        
        with col2:
            highest_facility = df.groupby('facility')['dot_per_1000_days'].mean().idxmax()
            highest_value = df.groupby('facility')['dot_per_1000_days'].mean().max()
            st.markdown(f"""
            <div class="metric-card">
                <div class="metric-value">{highest_value:.1f}</div>
                <div class="metric-label">Highest Avg ({highest_facility})</div>
            </div>
            """, unsafe_allow_html=True)
        
        with col3:
            lowest_facility = df.groupby('facility')['dot_per_1000_days'].mean().idxmin()
            lowest_value = df.groupby('facility')['dot_per_1000_days'].mean().min()
            st.markdown(f"""
            <div class="metric-card">
                <div class="metric-value">{lowest_value:.1f}</div>
                <div class="metric-label">Lowest Avg ({lowest_facility})</div>
            </div>
            """, unsafe_allow_html=True)
        
        with col4:
            variation = (df['dot_per_1000_days'].std() / df['dot_per_1000_days'].mean()) * 100
            st.markdown(f"""
            <div class="metric-card">
                <div class="metric-value">{variation:.1f}%</div>
                <div class="metric-label">Coefficient of Variation</div>
            </div>
            """, unsafe_allow_html=True)
        
    except FileNotFoundError:
        st.warning("Antibiotic DOT data file not found")
    except Exception as e:
        st.error(f"Error loading antibiotic DOT data: {str(e)}")

def show_default_parameters(product_type, organization_type):
    """Show default parameters being used when no CSV data is loaded"""
    
    st.markdown("### 📋 Default Parameters in Use")
    st.markdown("""
    <p style="font-size: 1.2rem; font-weight: 600; color: #333; margin-bottom: 15px;">
        These are the default values being used for your calculations. You can adjust them using the sidebar controls.
    </p>
    """, unsafe_allow_html=True)
    
    from config.defaults import PRAEDIGENE_DEFAULTS, PRAEDIALERT_DEFAULTS
    
    if product_type == 'praedigene':
        defaults = PRAEDIGENE_DEFAULTS.get(organization_type, PRAEDIGENE_DEFAULTS['medium_hospital'])
        
        # Show PGx defaults
        st.markdown("#### 💊 PGx Pipeline Defaults")
        pgx_data = [
            ['Annual Volume', f"{defaults['pgx']['annual_volume']:,}"],
            ['ADR Cost', f"${defaults['pgx']['adr_cost']:,}"],
            ['Patient Impact', f"{defaults['pgx']['patient_impact']}%"],
            ['Readmission Rate', f"{defaults['pgx']['readmission_rate']}%"]
        ]
        show_parameter_table(pgx_data)
        
        # Show TSO500 defaults
        st.markdown("#### 🧫 TSO500 Pipeline Defaults")
        tso500_data = [
            ['Annual Volume', f"{defaults['tso500']['annual_volume']:,}"],
            ['Treatment Cost', f"${defaults['tso500']['treatment_cost']:,}"],
            ['Treatment Success', f"{defaults['tso500']['treatment_success']}%"],
            ['FTE Daily Cost', f"${defaults['tso500']['fte_daily_cost']:,}"]
        ]
        show_parameter_table(tso500_data)
        
    else:  # praedialert
        defaults = PRAEDIALERT_DEFAULTS.get(organization_type, PRAEDIALERT_DEFAULTS['medium_hospital'])
        
        # Show IPC defaults
        st.markdown("#### 🦠 IPC Surveillance Defaults")
        ipc_data = [
            ['Annual Patient Days', f"{defaults['ipc_surveillance']['annual_patient_days']:,}"],
            ['HAI Incidence Rate', f"{defaults['ipc_surveillance']['hai_incidence_rate']}%"],
            ['Cost per HAI', f"${defaults['ipc_surveillance']['cost_per_hai']:,}"],
            ['Reduction Target', f"{defaults['ipc_surveillance']['reduction_target']}%"]
        ]
        show_parameter_table(ipc_data)
        
        # Show Antimicrobial defaults
        st.markdown("#### 💊 Antimicrobial Stewardship Defaults")
        anti_data = [
            ['Annual DOT', f"{defaults['antimicrobial_stewardship']['annual_dot']:,}"],
            ['Cost per DOT', f"${defaults['antimicrobial_stewardship']['cost_per_dot']:,}"],
            ['DOT Reduction Target', f"{defaults['antimicrobial_stewardship']['dot_reduction_target']}%"],
            ['Antibiotic Cost Reduction', f"{defaults['antimicrobial_stewardship']['antibiotic_cost_reduction']}%"]
        ]
        show_parameter_table(anti_data)

def show_parameter_table(data):
    """Display a parameter table with consistent formatting"""
    
    df = pd.DataFrame(data, columns=['Parameter', 'Value'])
    
    html_table = df.to_html(index=False, escape=False)
    html_table = html_table.replace('<table', '<table style="background-color: white !important; width: 60%; border-collapse: collapse; margin-bottom: 30px;"')
    html_table = html_table.replace('<th', '<th style="background-color: #f5f5f5 !important; color: #000080 !important; padding: 15px !important; font-size: 1.6rem !important; font-weight: 900 !important; border: 2px solid #000080 !important; text-align: left;"')
    html_table = html_table.replace('<td', '<td style="background-color: white !important; color: black !important; padding: 12px !important; font-size: 1.5rem !important; font-weight: 700 !important; border: 1px solid #ddd !important;"')
    
    st.markdown(html_table, unsafe_allow_html=True)