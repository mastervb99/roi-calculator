"""
Enhanced PraediAlert ROI Calculator with Real-World Study Data
Based on 8 VA facility implementation (Dec 2020 - Aug 2024)
All dollar amounts rounded to nearest dollar (no decimals)
"""

import pandas as pd
import numpy as np
import streamlit as st
from datetime import datetime, timedelta
from pathlib import Path
import sys
sys.path.append(str(Path(__file__).parent.parent))

from config.defaults import PRAEDIALERT_DEFAULTS, FINANCIAL_DEFAULTS, PRAEDIALERT_BUDGET
from config.study_data import (
    STUDY_RESULTS_18_MONTHS, 
    ANNUAL_FINANCIAL_PER_FACILITY,
    KEY_METRICS,
    calculate_annual_savings,
    calculate_five_year_projection,
    TARGET_HOSPITALS
)
from ui.data_viewer import show_data_viewer

class PraediAlertCalculatorEnhanced:
    def __init__(self, organization_type):
        self.organization_type = organization_type
        self.defaults = PRAEDIALERT_DEFAULTS.get(organization_type, PRAEDIALERT_DEFAULTS['medium_hospital'])
        self.financial = self._get_financial_defaults()
        self.data = self._load_data()
        
    def _get_financial_defaults(self):
        """Get financial defaults based on organization type"""
        size_map = {
            'small_hospital': 'small',
            'medium_hospital': 'medium', 
            'large_hospital': 'large',
            'visn21': 'visn21'
        }
        size = size_map.get(self.organization_type, 'medium')
        
        # Use study-based costs with no decimals
        if self.organization_type in TARGET_HOSPITALS:
            hospital_data = TARGET_HOSPITALS[self.organization_type]
            size = hospital_data['size']
            
        return {
            'implementation': int(FINANCIAL_DEFAULTS['implementation_cost'][size]),
            'maintenance': int(FINANCIAL_DEFAULTS['annual_maintenance'][size]),
            'training': int(FINANCIAL_DEFAULTS['staff_training'][size])
        }
    
    def _load_data(self):
        """Load VISN21 data if available"""
        data = {}
        data_path = Path(__file__).parent.parent / 'data'
        
        if self.organization_type == 'visn21':
            try:
                data['bed_days'] = pd.read_csv(data_path / 'visn21_patient_bed_days.csv')
                data['hai_rates'] = pd.read_csv(data_path / 'visn21_hai_rates.csv')
                data['antibiotic_dot'] = pd.read_csv(data_path / 'visn21_antibiotic_dot.csv')
            except:
                st.info("Using study-based parameters for calculations.")
        
        return data
    
    def format_currency(self, value):
        """Format currency with no decimals"""
        return f"${int(round(value)):,}"
    
    def format_number(self, value):
        """Format number with no decimals"""
        return f"{int(round(value)):,}"
    
    def calculate_roi(self):
        """Calculate ROI for all PraediAlert modules using real-world data"""
        st.markdown("## 🏥 PraediAlert ROI Analysis")
        st.markdown("*Based on proven results from 8 VA facility implementation (43.6% HAI reduction)*")
        
        # Create tabs
        tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs([
            "📊 Executive Summary",
            "🦠 IPC Surveillance", 
            "💊 Antimicrobial Stewardship",
            "📋 Regulatory Reporting",
            "📈 5-Year Projection",
            "📊 Source Data"
        ])
        
        # Calculate using real-world data
        ipc_roi = self.calculate_ipc_surveillance_enhanced()
        antimicrobial_roi = self.calculate_antimicrobial_stewardship_enhanced()
        regulatory_roi = self.calculate_regulatory_reporting_enhanced()
        
        # Total calculations (no decimals)
        total_savings = int(
            ipc_roi['total_savings'] +
            antimicrobial_roi['total_savings'] +
            regulatory_roi['total_savings']
        )
        
        total_investment = int(
            self.financial['implementation'] +
            self.financial['maintenance'] +
            self.financial['training']
        )
        
        roi_percentage = int((total_savings - total_investment) / total_investment * 100) if total_investment > 0 else 0
        payback_months = int((total_investment / (total_savings / 12))) if total_savings > 0 else 999
        
        # 5-year projection
        five_year = calculate_five_year_projection(total_savings, total_investment, self.financial['maintenance'])
        
        with tab1:
            self._show_executive_summary_enhanced(
                total_savings, total_investment, roi_percentage, payback_months,
                ipc_roi, antimicrobial_roi, regulatory_roi, five_year
            )
        
        with tab2:
            self._show_ipc_details_enhanced(ipc_roi)
        
        with tab3:
            self._show_antimicrobial_details_enhanced(antimicrobial_roi)
        
        with tab4:
            self._show_regulatory_details_enhanced(regulatory_roi)
            
        with tab5:
            self._show_five_year_projection(five_year, total_savings, total_investment)
            
        with tab6:
            show_data_viewer('praedialert', self.organization_type)
        
        # Return ROI results dictionary for dashboard
        return {
            'total_savings': total_savings,
            'total_investment': total_investment,
            'roi_percentage': roi_percentage,
            'payback_months': payback_months,
            'ipc': ipc_roi,  # Changed from ipc_roi to match dashboard
            'antimicrobial': antimicrobial_roi,  # Changed from antimicrobial_roi
            'regulatory': regulatory_roi,  # Changed from regulatory_roi
            'five_year_projection': five_year,
            'hais_prevented': ipc_roi['hais_prevented'],
            'lives_saved': ipc_roi['lives_saved'],
            'days_saved': ipc_roi['days_saved']
        }
    
    def calculate_ipc_surveillance_enhanced(self):
        """Calculate IPC ROI using real-world study data"""
        params = self.defaults['ipc_surveillance']
        
        st.sidebar.markdown("### 🦠 IPC Surveillance Parameters")
        st.sidebar.markdown("*Using 43.6% reduction from study*")
        
        # Get parameters
        patient_days = st.sidebar.number_input(
            "Annual Patient Days",
            min_value=10000,
            max_value=200000,
            value=int(params['annual_patient_days']),
            step=5000
        )
        
        # Use study-based HAI reduction rate (43.6%)
        hai_reduction = 43.6  # Fixed from study
        st.sidebar.info(f"HAI Reduction: {hai_reduction}% (proven in 8-facility study)")
        
        # Calculate using study data
        baseline_hai_rate = params['hai_incidence_rate'] / 100
        baseline_hais = int((patient_days / 1000) * baseline_hai_rate * 10)  # HAIs per 1000 patient days
        hais_prevented = int(baseline_hais * (hai_reduction / 100))
        
        # Financial calculations (no decimals)
        direct_savings = hais_prevented * KEY_METRICS['cost_per_hai']
        
        # Additional savings
        los_days_saved = hais_prevented * KEY_METRICS['average_los_extension']
        los_savings = los_days_saved * KEY_METRICS['cost_per_hospital_day']
        
        # Mortality impact
        lives_saved = int(hais_prevented * KEY_METRICS['mortality_rate'])
        mortality_value = lives_saved * KEY_METRICS['life_value']
        
        # Outbreak prevention (probabilistic)
        outbreak_probability = 0.25  # From study: 2 outbreaks in 8 facilities
        outbreak_savings = int(outbreak_probability * KEY_METRICS['outbreak_cost'])
        
        total_savings = direct_savings + los_savings + mortality_value + outbreak_savings
        
        return {
            'patient_days': patient_days,
            'baseline_hais': baseline_hais,
            'hais_prevented': hais_prevented,
            'reduction_percentage': hai_reduction,
            'direct_savings': direct_savings,
            'los_savings': los_savings,
            'mortality_value': mortality_value,
            'outbreak_savings': outbreak_savings,
            'total_savings': total_savings,
            'lives_saved': lives_saved,
            'days_saved': los_days_saved
        }
    
    def calculate_antimicrobial_stewardship_enhanced(self):
        """Calculate Antimicrobial Stewardship ROI with no decimals"""
        params = self.defaults['antimicrobial_stewardship']
        
        st.sidebar.markdown("### 💊 Antimicrobial Parameters")
        
        annual_dot = st.sidebar.number_input(
            "Annual DOT (Days of Therapy)",
            min_value=10000,
            max_value=100000,
            value=int(params['annual_dot']),
            step=5000
        )
        
        cost_per_dot = st.sidebar.number_input(
            "Cost per DOT ($)",
            min_value=50,
            max_value=200,
            value=int(params['cost_per_dot']),
            step=10
        )
        
        dot_reduction = st.sidebar.slider(
            "DOT Reduction Target (%)",
            min_value=10,
            max_value=40,
            value=int(params['dot_reduction_target']),
            step=5
        )
        
        # Calculations (no decimals)
        current_antibiotic_cost = annual_dot * cost_per_dot
        dot_reduced = int(annual_dot * (dot_reduction / 100))
        dot_savings = dot_reduced * cost_per_dot
        
        # Additional savings
        optimization_savings = int(current_antibiotic_cost * 0.25)  # 25% cost optimization
        
        # C. diff reduction
        cdiff_cases_prevented = int((annual_dot / 10000) * (dot_reduction / 100) * 15)
        cdiff_savings = cdiff_cases_prevented * 15000
        
        total_savings = dot_savings + optimization_savings + cdiff_savings
        
        return {
            'annual_dot': annual_dot,
            'current_cost': current_antibiotic_cost,
            'dot_reduced': dot_reduced,
            'dot_reduction_percentage': dot_reduction,
            'dot_savings': dot_savings,
            'optimization_savings': optimization_savings,
            'cdiff_cases_prevented': cdiff_cases_prevented,
            'cdiff_savings': cdiff_savings,
            'total_savings': total_savings
        }
    
    def calculate_regulatory_reporting_enhanced(self):
        """Calculate Regulatory Reporting ROI with no decimals"""
        params = self.defaults['regulatory_reporting']
        
        st.sidebar.markdown("### 📋 Regulatory Parameters")
        
        reports_per_year = st.sidebar.number_input(
            "Reports per Year",
            min_value=50,
            max_value=200,
            value=int(params['reports_per_year']),
            step=10
        )
        
        hours_per_report = st.sidebar.number_input(
            "Hours per Report",
            min_value=1,
            max_value=8,
            value=int(params['hours_per_report']),
            step=1
        )
        
        hourly_cost = st.sidebar.number_input(
            "Hourly Labor Cost ($)",
            min_value=30,
            max_value=100,
            value=int(params['hourly_labor_cost']),
            step=5
        )
        
        automation_efficiency = st.sidebar.slider(
            "Automation Efficiency (%)",
            min_value=50,
            max_value=90,
            value=int(params['automation_efficiency']),
            step=5
        )
        
        # Calculations (no decimals)
        total_hours_manual = reports_per_year * hours_per_report
        hours_saved = int(total_hours_manual * (automation_efficiency / 100))
        labor_savings = hours_saved * hourly_cost
        
        # Additional benefits
        accuracy_improvement_value = reports_per_year * 50
        compliance_risk_reduction = reports_per_year * 100
        
        total_savings = labor_savings + accuracy_improvement_value + compliance_risk_reduction
        
        return {
            'reports_per_year': reports_per_year,
            'hours_per_report': hours_per_report,
            'total_hours_manual': total_hours_manual,
            'hours_saved': hours_saved,
            'hourly_cost': hourly_cost,
            'labor_savings': labor_savings,
            'accuracy_value': accuracy_improvement_value,
            'compliance_value': compliance_risk_reduction,
            'total_savings': total_savings,
            'automation_efficiency': automation_efficiency
        }
    
    def _show_executive_summary_enhanced(self, total_savings, total_investment, roi_percentage, 
                                        payback_months, ipc_roi, antimicrobial_roi, regulatory_roi, five_year):
        """Show executive summary with real-world data context"""
        st.markdown("### 📊 Executive Summary")
        st.markdown("*Based on proven 43.6% HAI reduction from 8 VA facilities*")
        
        # Key metrics in columns
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric(
                "Total Annual Savings",
                self.format_currency(total_savings),
                f"Year 1 Net: {self.format_currency(total_savings - total_investment)}"
            )
        
        with col2:
            st.metric(
                "Total Investment",
                self.format_currency(total_investment),
                f"Payback: {payback_months} months"
            )
        
        with col3:
            st.metric(
                "First Year ROI",
                f"{roi_percentage}%",
                f"5-Year: {five_year[-1]['cumulative_roi']}%"
            )
        
        with col4:
            total_hais = ipc_roi['hais_prevented']
            st.metric(
                "HAIs Prevented",
                self.format_number(total_hais),
                f"{ipc_roi['lives_saved']} lives saved"
            )
        
        # Module breakdown
        st.markdown("### Module Contribution")
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.markdown("#### 🦠 IPC Surveillance")
            st.markdown(f"**Savings:** {self.format_currency(ipc_roi['total_savings'])}")
            st.markdown(f"**HAIs Prevented:** {self.format_number(ipc_roi['hais_prevented'])}")
            st.markdown(f"**Lives Saved:** {self.format_number(ipc_roi['lives_saved'])}")
        
        with col2:
            st.markdown("#### 💊 Antimicrobial")
            st.markdown(f"**Savings:** {self.format_currency(antimicrobial_roi['total_savings'])}")
            st.markdown(f"**DOT Reduced:** {self.format_number(antimicrobial_roi['dot_reduced'])}")
            st.markdown(f"**C.diff Prevented:** {self.format_number(antimicrobial_roi['cdiff_cases_prevented'])}")
        
        with col3:
            st.markdown("#### 📋 Regulatory")
            st.markdown(f"**Savings:** {self.format_currency(regulatory_roi['total_savings'])}")
            st.markdown(f"**Hours Saved:** {self.format_number(regulatory_roi['hours_saved'])}")
            st.markdown(f"**Reports:** {self.format_number(regulatory_roi['reports_per_year'])}")
        
        # Study context
        st.info("""
        **Proven Results:** This analysis uses real-world effectiveness data from 8 VA Medical Centers 
        (Dec 2020 - Aug 2024) showing 43.6% HAI reduction, 18.1% better than control facilities.
        """)
    
    def _show_ipc_details_enhanced(self, roi):
        """Show IPC details with study context"""
        st.markdown("### 🦠 IPC Surveillance Details")
        st.markdown("*Using proven 43.6% reduction rate from 8-facility study*")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("#### Infection Prevention")
            st.markdown(f"- **Baseline HAIs:** {self.format_number(roi['baseline_hais'])}")
            st.markdown(f"- **HAIs Prevented:** {self.format_number(roi['hais_prevented'])}")
            st.markdown(f"- **Reduction Rate:** {roi['reduction_percentage']}%")
            st.markdown(f"- **Lives Saved:** {self.format_number(roi['lives_saved'])}")
            st.markdown(f"- **Hospital Days Saved:** {self.format_number(roi['days_saved'])}")
        
        with col2:
            st.markdown("#### Financial Impact")
            st.markdown(f"- **Direct HAI Savings:** {self.format_currency(roi['direct_savings'])}")
            st.markdown(f"- **LOS Reduction Savings:** {self.format_currency(roi['los_savings'])}")
            st.markdown(f"- **Mortality Prevention Value:** {self.format_currency(roi['mortality_value'])}")
            st.markdown(f"- **Outbreak Prevention:** {self.format_currency(roi['outbreak_savings'])}")
            st.markdown(f"- **Total Savings:** {self.format_currency(roi['total_savings'])}")
        
        # Context from study
        st.success("""
        **Study Validation:** These projections are based on actual results where facilities like 
        Palo Alto (18.9% reduction), Dallas (63.5% reduction), and West Palm Beach (65.1% reduction) 
        demonstrated the range of achievable outcomes.
        """)
    
    def _show_antimicrobial_details_enhanced(self, roi):
        """Show antimicrobial details"""
        st.markdown("### 💊 Antimicrobial Stewardship Details")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("#### Usage Reduction")
            st.markdown(f"- **Current Annual DOT:** {self.format_number(roi['annual_dot'])}")
            st.markdown(f"- **DOT Reduced:** {self.format_number(roi['dot_reduced'])}")
            st.markdown(f"- **Reduction Rate:** {roi['dot_reduction_percentage']}%")
            st.markdown(f"- **C.diff Cases Prevented:** {self.format_number(roi['cdiff_cases_prevented'])}")
        
        with col2:
            st.markdown("#### Cost Savings")
            st.markdown(f"- **Current Antibiotic Cost:** {self.format_currency(roi['current_cost'])}")
            st.markdown(f"- **DOT Savings:** {self.format_currency(roi['dot_savings'])}")
            st.markdown(f"- **Optimization Savings:** {self.format_currency(roi['optimization_savings'])}")
            st.markdown(f"- **C.diff Prevention:** {self.format_currency(roi['cdiff_savings'])}")
            st.markdown(f"- **Total Savings:** {self.format_currency(roi['total_savings'])}")
    
    def _show_regulatory_details_enhanced(self, roi):
        """Show regulatory details"""
        st.markdown("### 📋 Regulatory Reporting Details")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("#### Efficiency Gains")
            st.markdown(f"- **Reports per Year:** {self.format_number(roi['reports_per_year'])}")
            st.markdown(f"- **Manual Hours Required:** {self.format_number(roi['total_hours_manual'])}")
            st.markdown(f"- **Hours Saved:** {self.format_number(roi['hours_saved'])}")
            st.markdown(f"- **Automation Rate:** {roi['automation_efficiency']}%")
        
        with col2:
            st.markdown("#### Value Creation")
            st.markdown(f"- **Labor Cost Savings:** {self.format_currency(roi['labor_savings'])}")
            st.markdown(f"- **Accuracy Improvement:** {self.format_currency(roi['accuracy_value'])}")
            st.markdown(f"- **Compliance Risk Reduction:** {self.format_currency(roi['compliance_value'])}")
            st.markdown(f"- **Total Value:** {self.format_currency(roi['total_savings'])}")
    
    def _show_five_year_projection(self, projections, annual_savings, initial_investment):
        """Show 5-year financial projection"""
        st.markdown("### 📈 Five-Year Financial Projection")
        
        # Create DataFrame for display
        df = pd.DataFrame(projections)
        
        # Format for display
        display_df = df.copy()
        currency_cols = ['cost', 'savings', 'net_benefit', 'cumulative_cost', 'cumulative_savings', 'cumulative_net']
        for col in currency_cols:
            display_df[col] = display_df[col].apply(lambda x: self.format_currency(x))
        
        display_df['roi_percent'] = display_df['roi_percent'].apply(lambda x: f"{x}%")
        display_df['cumulative_roi'] = display_df['cumulative_roi'].apply(lambda x: f"{x}%")
        
        # Rename columns for display
        display_df.columns = [
            'Year', 'Annual Cost', 'Annual Savings', 'Net Benefit', 'ROI %',
            'Total Cost', 'Total Savings', 'Total Net', 'Cumulative ROI %'
        ]
        
        st.dataframe(display_df, use_container_width=True, hide_index=True)
        
        # Summary metrics
        col1, col2, col3 = st.columns(3)
        
        with col1:
            total_5yr_savings = df['savings'].sum()
            st.metric(
                "5-Year Total Savings",
                self.format_currency(total_5yr_savings)
            )
        
        with col2:
            total_5yr_cost = df['cost'].sum()
            st.metric(
                "5-Year Total Cost",
                self.format_currency(total_5yr_cost)
            )
        
        with col3:
            net_5yr = total_5yr_savings - total_5yr_cost
            st.metric(
                "5-Year Net Benefit",
                self.format_currency(net_5yr)
            )
        
        st.success(f"""
        **5-Year Summary:** With proven effectiveness from the 8-facility study, this implementation 
        is projected to save {self.format_currency(net_5yr)} over 5 years with a {df.iloc[-1]['cumulative_roi']}% ROI.
        """)