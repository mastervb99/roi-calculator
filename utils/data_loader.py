"""
Data loader for ROI Calculator
Handles CSV import and VISN21 sample data
"""

import pandas as pd
import streamlit as st
from pathlib import Path
import json

class DataLoader:
    def __init__(self):
        self.data_path = Path(__file__).parent.parent / 'data'
        self.loaded_data = {}
    
    def load_custom_data(self, uploaded_file):
        """Load custom data from uploaded file"""
        try:
            if uploaded_file.name.endswith('.csv'):
                df = pd.read_csv(uploaded_file)
            elif uploaded_file.name.endswith('.xlsx'):
                df = pd.read_excel(uploaded_file)
            else:
                st.error("Unsupported file format. Please upload CSV or XLSX file.")
                return False
            
            # Store the data
            self.loaded_data['custom'] = df
            
            # Try to detect data type
            columns = df.columns.tolist()
            
            if 'hai_type' in columns or 'infection_rate' in columns:
                self.loaded_data['type'] = 'hai_rates'
                st.info("Detected HAI rates data")
            elif 'dot_per_1000_days' in columns or 'antibiotic' in columns:
                self.loaded_data['type'] = 'antibiotic_dot'
                st.info("Detected antibiotic DOT data")
            elif 'bed_days' in columns or 'patient_days' in columns:
                self.loaded_data['type'] = 'patient_days'
                st.info("Detected patient bed days data")
            elif 'test_volume' in columns or 'sample_id' in columns:
                self.loaded_data['type'] = 'genetic_tests'
                st.info("Detected genetic testing data")
            else:
                self.loaded_data['type'] = 'generic'
                st.info("Loaded generic data file")
            
            # Display preview
            st.markdown("### Data Preview")
            st.dataframe(df.head(), use_container_width=True)
            
            # Display summary statistics
            st.markdown("### Summary Statistics")
            col1, col2, col3 = st.columns(3)
            
            with col1:
                st.metric("Rows", len(df))
            with col2:
                st.metric("Columns", len(df.columns))
            with col3:
                st.metric("Data Type", self.loaded_data['type'].replace('_', ' ').title())
            
            return True
            
        except Exception as e:
            st.error(f"Error loading file: {str(e)}")
            return False
    
    def load_visn21_sample_data(self):
        """Load VISN21 sample data files"""
        try:
            # Load all VISN21 data files
            files_loaded = []
            
            # Patient bed days
            bed_days_file = self.data_path / 'visn21_patient_bed_days.csv'
            if bed_days_file.exists():
                self.loaded_data['bed_days'] = pd.read_csv(bed_days_file)
                files_loaded.append("Patient Bed Days")
            
            # HAI rates
            hai_file = self.data_path / 'visn21_hai_rates.csv'
            if hai_file.exists():
                self.loaded_data['hai_rates'] = pd.read_csv(hai_file)
                files_loaded.append("HAI Rates")
            
            # Antibiotic DOT
            dot_file = self.data_path / 'visn21_antibiotic_dot.csv'
            if dot_file.exists():
                self.loaded_data['antibiotic_dot'] = pd.read_csv(dot_file)
                files_loaded.append("Antibiotic DOT")
            
            if files_loaded:
                st.success(f"✅ Loaded VISN21 data: {', '.join(files_loaded)}")
                
                # Display summary
                with st.expander("📊 VISN21 Data Summary", expanded=True):
                    if 'bed_days' in self.loaded_data:
                        st.markdown("**Facilities Included:**")
                        facilities = self.loaded_data['bed_days']['facility'].tolist()
                        st.write(", ".join(facilities))
                    
                    if 'hai_rates' in self.loaded_data:
                        st.markdown("**HAI Types Tracked:**")
                        hai_types = self.loaded_data['hai_rates']['hai_type'].unique().tolist()
                        st.write(", ".join(hai_types))
                    
                    if 'antibiotic_dot' in self.loaded_data:
                        st.markdown("**Antibiotic DOT Data:**")
                        facilities = self.loaded_data['antibiotic_dot']['facility'].unique().tolist()
                        st.write(f"Data for {len(facilities)} facilities across 4 quarters")
                
                return True
            else:
                st.warning("No VISN21 sample data files found")
                return False
                
        except Exception as e:
            st.error(f"Error loading VISN21 data: {str(e)}")
            return False
    
    def get_loaded_data(self):
        """Return loaded data"""
        return self.loaded_data
    
    def export_template(self, template_type):
        """Export a template CSV for data import"""
        templates = {
            'hai_rates': pd.DataFrame({
                'facility': ['Hospital A', 'Hospital B'],
                'hai_type': ['CLABSI', 'CLABSI'],
                'rolling_12_months_rate': [0.5, 0.8],
                'unit_of_measure': ['per 1000 central line days', 'per 1000 central line days']
            }),
            'antibiotic_dot': pd.DataFrame({
                'facility': ['Hospital A', 'Hospital B'],
                'quarter': ['Q1', 'Q1'],
                'year': [2024, 2024],
                'dot_per_1000_days': [350.5, 425.3]
            }),
            'patient_days': pd.DataFrame({
                'facility': ['Hospital A', 'Hospital B'],
                'bed_days_annual': [50000, 75000]
            }),
            'genetic_tests': pd.DataFrame({
                'test_type': ['PGx', 'TSO500', 'BIAS2015'],
                'annual_volume': [1000, 200, 500],
                'in_house_cost': [200, 1500, 1000],
                'outsource_cost': [350, 1800, 1200]
            })
        }
        
        if template_type in templates:
            return templates[template_type]
        else:
            return None
    
    def validate_data(self, df, expected_columns):
        """Validate uploaded data has required columns"""
        missing_columns = []
        for col in expected_columns:
            if col not in df.columns:
                missing_columns.append(col)
        
        if missing_columns:
            st.warning(f"Missing expected columns: {', '.join(missing_columns)}")
            return False
        return True
    
    def merge_facility_data(self, facility_dfs):
        """Merge data from multiple facilities"""
        merged_data = {}
        
        for facility, df in facility_dfs.items():
            # Process each facility's data
            if 'hai_rates' in df:
                if 'hai_rates' not in merged_data:
                    merged_data['hai_rates'] = []
                df['hai_rates']['facility'] = facility
                merged_data['hai_rates'].append(df['hai_rates'])
            
            if 'antibiotic_dot' in df:
                if 'antibiotic_dot' not in merged_data:
                    merged_data['antibiotic_dot'] = []
                df['antibiotic_dot']['facility'] = facility
                merged_data['antibiotic_dot'].append(df['antibiotic_dot'])
        
        # Concatenate all facility data
        for key in merged_data:
            merged_data[key] = pd.concat(merged_data[key], ignore_index=True)
        
        return merged_data