"""
PraediAlert ROI Calculator
Handles IPC Surveillance, Antimicrobial Stewardship, and Regulatory Reporting
"""

import pandas as pd
import numpy as np
import streamlit as st
from datetime import datetime, timedelta
from config.defaults import PRAEDIALERT_DEFAULTS, FINANCIAL_DEFAULTS, PRAEDIALERT_BUDGET
from pathlib import Path
import sys
sys.path.append(str(Path(__file__).parent.parent))
from ui.data_viewer import show_data_viewer

class PraediAlertCalculator:
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
        return {
            'implementation': FINANCIAL_DEFAULTS['implementation_cost'][size],
            'maintenance': FINANCIAL_DEFAULTS['annual_maintenance'][size],
            'training': FINANCIAL_DEFAULTS['staff_training'][size]
        }
    
    def _load_data(self):
        """Load VISN21 data if available"""
        data = {}
        data_path = Path(__file__).parent.parent / 'data'
        
        # Try to load VISN21 specific data
        if self.organization_type == 'visn21':
            try:
                data['bed_days'] = pd.read_csv(data_path / 'visn21_patient_bed_days.csv')
                data['hai_rates'] = pd.read_csv(data_path / 'visn21_hai_rates.csv')
                data['antibiotic_dot'] = pd.read_csv(data_path / 'visn21_antibiotic_dot.csv')
            except:
                st.info("Using default VISN21 parameters. Upload custom data for more accurate calculations.")
        
        return data
    
    def calculate_roi(self):
        """Calculate ROI for all PraediAlert modules"""
        st.markdown("## 🏥 PraediAlert ROI Analysis")
        
        # Create tabs for different modules
        tab1, tab2, tab3, tab4, tab5 = st.tabs([
            "📊 Executive Summary",
            "🦠 IPC Surveillance",
            "💊 Antimicrobial Stewardship",
            "📋 Regulatory Reporting",
            "📊 Source Data"
        ])
        
        # Calculate individual modules
        ipc_roi = self.calculate_ipc_surveillance()
        antimicrobial_roi = self.calculate_antimicrobial_stewardship()
        regulatory_roi = self.calculate_regulatory_reporting()
        
        # Combine results
        total_savings = (
            ipc_roi['total_savings'] +
            antimicrobial_roi['total_savings'] +
            regulatory_roi['total_savings']
        )
        
        total_investment = (
            self.financial['implementation'] +
            self.financial['maintenance'] +
            self.financial['training']
        )
        
        roi_percentage = ((total_savings - total_investment) / total_investment * 100) if total_investment > 0 else 0
        payback_months = (total_investment / (total_savings / 12)) if total_savings > 0 else 999
        
        with tab1:
            self._show_executive_summary(
                total_savings, total_investment, roi_percentage, payback_months,
                ipc_roi, antimicrobial_roi, regulatory_roi
            )
        
        with tab2:
            self._show_ipc_details(ipc_roi)
        
        with tab3:
            self._show_antimicrobial_details(antimicrobial_roi)
        
        with tab4:
            self._show_regulatory_details(regulatory_roi)
        
        with tab5:
            show_data_viewer('praedialert', self.organization_type)
        
        return {
            'total_savings': total_savings,
            'total_investment': total_investment,
            'roi_percentage': roi_percentage,
            'payback_months': payback_months,
            'ipc': ipc_roi,
            'antimicrobial': antimicrobial_roi,
            'regulatory': regulatory_roi
        }
    
    def calculate_ipc_surveillance(self):
        """Calculate ROI for IPC Surveillance module"""
        params = self.defaults['ipc_surveillance']
        
        # Get actual data if VISN21
        if self.organization_type == 'visn21' and 'hai_rates' in self.data:
            hai_data = self.data['hai_rates']
            bed_days_data = self.data['bed_days']
            
            # Calculate weighted average HAI rate
            avg_hai_rate = hai_data[hai_data['hai_type'] == 'CDI']['rolling_12_months_rate'].mean()
            annual_patient_days = bed_days_data['bed_days_annual'].sum()
        else:
            avg_hai_rate = params['hai_incidence_rate']
            annual_patient_days = params['annual_patient_days']
        
        # Parameters with sliders
        st.sidebar.markdown("### 🦠 IPC Surveillance Parameters")
        
        cost_per_hai = st.sidebar.number_input(
            "Cost per HAI ($)",
            min_value=10000,
            max_value=50000,
            value=params['cost_per_hai'],
            step=1000,
            help="Average cost of treating a healthcare-associated infection"
        )
        
        reduction_target = st.sidebar.slider(
            "HAI Reduction Target (%)",
            min_value=10.0,
            max_value=50.0,
            value=params['reduction_target'],
            step=5.0,
            help="Expected reduction in HAI rates with PraediAlert"
        )
        
        # Calculations
        current_hais = (avg_hai_rate / 100) * (annual_patient_days / 365)
        hais_prevented = current_hais * (reduction_target / 100)
        savings_from_prevention = hais_prevented * cost_per_hai
        
        # Additional savings from early detection
        early_detection_rate = 0.4  # 40% detected earlier
        early_detection_savings = current_hais * early_detection_rate * (cost_per_hai * 0.3)
        
        total_savings = savings_from_prevention + early_detection_savings
        
        return {
            'annual_patient_days': annual_patient_days,
            'current_hai_rate': avg_hai_rate,
            'current_hais': current_hais,
            'hais_prevented': hais_prevented,
            'reduction_percentage': reduction_target,
            'cost_per_hai': cost_per_hai,
            'prevention_savings': savings_from_prevention,
            'early_detection_savings': early_detection_savings,
            'total_savings': total_savings
        }
    
    def calculate_antimicrobial_stewardship(self):
        """Calculate ROI for Antimicrobial Stewardship module"""
        params = self.defaults['antimicrobial_stewardship']
        
        # Get actual data if VISN21
        if self.organization_type == 'visn21' and 'antibiotic_dot' in self.data:
            dot_data = self.data['antibiotic_dot']
            annual_dot = dot_data['dot_per_1000_days'].mean() * 144.517  # VISN21 total bed days in thousands
        else:
            annual_dot = params['annual_dot']
        
        # Parameters with sliders
        st.sidebar.markdown("### 💊 Antimicrobial Parameters")
        
        cost_per_dot = st.sidebar.number_input(
            "Cost per DOT ($)",
            min_value=50,
            max_value=200,
            value=params['cost_per_dot'],
            step=10,
            help="Average cost per day of therapy"
        )
        
        dot_reduction = st.sidebar.slider(
            "DOT Reduction Target (%)",
            min_value=10.0,
            max_value=40.0,
            value=params['dot_reduction_target'],
            step=5.0,
            help="Expected reduction in days of therapy"
        )
        
        cost_reduction = st.sidebar.slider(
            "Antibiotic Cost Reduction (%)",
            min_value=15.0,
            max_value=40.0,
            value=params['antibiotic_cost_reduction'],
            step=5.0,
            help="Expected reduction in antibiotic costs"
        )
        
        # Calculations
        current_antibiotic_cost = annual_dot * cost_per_dot
        dot_reduced = annual_dot * (dot_reduction / 100)
        dot_savings = dot_reduced * cost_per_dot
        
        # Additional cost reduction from optimized selection
        optimization_savings = current_antibiotic_cost * (cost_reduction / 100)
        
        # C. diff reduction savings (correlated with antibiotic use)
        cdiff_reduction = dot_reduction * 0.5  # 50% of DOT reduction translates to C. diff reduction
        cdiff_cases_prevented = (annual_dot / 10000) * (cdiff_reduction / 100) * 15  # Estimate
        cdiff_savings = cdiff_cases_prevented * 15000  # Cost per C. diff case
        
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
    
    def calculate_regulatory_reporting(self):
        """Calculate ROI for Regulatory Reporting module"""
        params = self.defaults['regulatory_reporting']
        
        # Parameters with sliders
        st.sidebar.markdown("### 📋 Regulatory Reporting Parameters")
        
        reports_per_year = st.sidebar.number_input(
            "Reports per Year",
            min_value=50,
            max_value=200,
            value=params['reports_per_year'],
            step=10,
            help="Number of regulatory reports generated annually"
        )
        
        hours_per_report = st.sidebar.number_input(
            "Hours per Report",
            min_value=1.0,
            max_value=8.0,
            value=float(params['hours_per_report']),
            step=0.5,
            help="Average hours to complete each report manually"
        )
        
        hourly_cost = st.sidebar.number_input(
            "Hourly Labor Cost ($)",
            min_value=30,
            max_value=100,
            value=params['hourly_labor_cost'],
            step=5,
            help="Cost per hour of staff time"
        )
        
        automation_efficiency = st.sidebar.slider(
            "Automation Efficiency (%)",
            min_value=50.0,
            max_value=90.0,
            value=params['automation_efficiency'],
            step=5.0,
            help="Percentage of time saved through automation"
        )
        
        # Calculations
        total_hours_manual = reports_per_year * hours_per_report
        hours_saved = total_hours_manual * (automation_efficiency / 100)
        labor_savings = hours_saved * hourly_cost
        
        # Additional benefits
        accuracy_improvement_value = reports_per_year * 50  # Value of improved accuracy
        compliance_risk_reduction = reports_per_year * 100  # Value of reduced compliance risk
        
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
            'total_savings': total_savings
        }
    
    def _show_executive_summary(self, total_savings, total_investment, roi_percentage, payback_months,
                                ipc_roi, antimicrobial_roi, regulatory_roi):
        """Display executive summary"""
        st.markdown("""
        <div class="main-header">
            <div class="header-title">PraediAlert ROI Executive Summary</div>
            <div class="header-subtitle">Comprehensive Clinical Surveillance Platform</div>
            <div class="header-subtitle" style="color: #006400; margin-top: 10px;">VISN 21 Implementation (7 Hospitals)</div>
        </div>
        """, unsafe_allow_html=True)
        
        # Key metrics
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.markdown(f"""
            <div class="metric-card">
                <div class="metric-value">${total_savings:,.0f}</div>
                <div class="metric-label">Annual Savings</div>
                <div class="metric-delta metric-positive">↑ Year 1 Total</div>
            </div>
            """, unsafe_allow_html=True)
        
        with col2:
            st.markdown(f"""
            <div class="metric-card">
                <div class="metric-value">{roi_percentage:.0f}%</div>
                <div class="metric-label">ROI Percentage</div>
                <div class="metric-delta metric-positive">↑ First Year</div>
            </div>
            """, unsafe_allow_html=True)
        
        with col3:
            st.markdown(f"""
            <div class="metric-card">
                <div class="metric-value">{payback_months:.1f}</div>
                <div class="metric-label">Payback (Months)</div>
                <div class="metric-delta metric-positive">↓ Fast Recovery</div>
            </div>
            """, unsafe_allow_html=True)
        
        with col4:
            st.markdown(f"""
            <div class="metric-card">
                <div class="metric-value">${total_investment:,.0f}</div>
                <div class="metric-label">Total Investment</div>
                <div class="metric-delta">One-time + Annual</div>
            </div>
            """, unsafe_allow_html=True)
        
        # Module breakdown
        st.markdown("### 📊 Savings by Module")
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.metric(
                "IPC Surveillance",
                f"${ipc_roi['total_savings']:,.0f}",
                f"{ipc_roi['hais_prevented']:.0f} HAIs prevented"
            )
        
        with col2:
            st.metric(
                "Antimicrobial Stewardship",
                f"${antimicrobial_roi['total_savings']:,.0f}",
                f"{antimicrobial_roi['dot_reduced']:,.0f} DOT reduced"
            )
        
        with col3:
            st.metric(
                "Regulatory Reporting",
                f"${regulatory_roi['total_savings']:,.0f}",
                f"{regulatory_roi['hours_saved']:,.0f} hours saved"
            )
        
        # Visualization
        import plotly.graph_objects as go
        
        fig = go.Figure(data=[
            go.Bar(
                x=['IPC Surveillance', 'Antimicrobial', 'Regulatory', 'Total Investment'],
                y=[ipc_roi['total_savings'], antimicrobial_roi['total_savings'], 
                   regulatory_roi['total_savings'], -total_investment],
                marker_color=['#00c389', '#0094d8', '#00609c', '#dc3545'],
                text=[f"${x:,.0f}" for x in [ipc_roi['total_savings'], antimicrobial_roi['total_savings'],
                      regulatory_roi['total_savings'], -total_investment]],
                textposition='outside'
            )
        ])
        
        fig.update_layout(
            title="Annual Savings vs Investment",
            yaxis_title="Amount ($)",
            showlegend=False,
            height=400
        )
        
        st.plotly_chart(fig, use_container_width=True)
        
        # Show actual budget information for VISN21
        if self.organization_type == 'visn21':
            self._show_budget_breakdown(total_savings)
    
    def _show_ipc_details(self, roi_data):
        """Display detailed IPC Surveillance metrics"""
        st.markdown("### 🦠 IPC Surveillance Module Details")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("#### Current State")
            st.metric("Annual Patient Days", f"{roi_data['annual_patient_days']:,.0f}")
            st.metric("Current HAI Rate", f"{roi_data['current_hai_rate']:.2f}%")
            st.metric("Estimated Annual HAIs", f"{roi_data['current_hais']:.0f}")
        
        with col2:
            st.markdown("#### With PraediAlert")
            st.metric("HAIs Prevented", f"{roi_data['hais_prevented']:.0f}")
            st.metric("Prevention Savings", f"${roi_data['prevention_savings']:,.0f}")
            st.metric("Early Detection Savings", f"${roi_data['early_detection_savings']:,.0f}")
        
        # Create trend visualization
        import plotly.express as px
        
        months = pd.date_range(start='2024-01', periods=12, freq='ME')
        baseline_hais = [roi_data['current_hais']/12] * 12
        with_praedialert = [roi_data['current_hais']/12 * (1 - roi_data['reduction_percentage']/100)] * 12
        
        df = pd.DataFrame({
            'Month': months.tolist() * 2,
            'HAIs': baseline_hais + with_praedialert,
            'Scenario': ['Baseline'] * 12 + ['With PraediAlert'] * 12
        })
        
        fig = px.line(df, x='Month', y='HAIs', color='Scenario',
                     title='Projected HAI Reduction',
                     color_discrete_map={'Baseline': '#dc3545', 'With PraediAlert': '#00c389'})
        
        st.plotly_chart(fig, use_container_width=True)
    
    def _show_antimicrobial_details(self, roi_data):
        """Display detailed Antimicrobial Stewardship metrics"""
        st.markdown("### 💊 Antimicrobial Stewardship Module Details")
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.markdown("#### DOT Metrics")
            st.metric("Annual DOT", f"{roi_data['annual_dot']:,.0f}")
            st.metric("DOT Reduced", f"{roi_data['dot_reduced']:,.0f}")
            st.metric("DOT Savings", f"${roi_data['dot_savings']:,.0f}")
        
        with col2:
            st.markdown("#### Cost Optimization")
            st.metric("Current Cost", f"${roi_data['current_cost']:,.0f}")
            st.metric("Optimization Savings", f"${roi_data['optimization_savings']:,.0f}")
            st.metric("Cost Reduction", f"{roi_data['optimization_savings']/roi_data['current_cost']*100:.1f}%")
        
        with col3:
            st.markdown("#### C. diff Impact")
            st.metric("Cases Prevented", f"{roi_data['cdiff_cases_prevented']:.0f}")
            st.metric("C. diff Savings", f"${roi_data['cdiff_savings']:,.0f}")
            st.metric("Total Savings", f"${roi_data['total_savings']:,.0f}")
        
        # Pie chart of savings breakdown
        import plotly.graph_objects as go
        
        fig = go.Figure(data=[go.Pie(
            labels=['DOT Reduction', 'Cost Optimization', 'C. diff Prevention'],
            values=[roi_data['dot_savings'], roi_data['optimization_savings'], roi_data['cdiff_savings']],
            hole=.3,
            marker_colors=['#00609c', '#0094d8', '#00c389']
        )])
        
        fig.update_layout(
            title="Antimicrobial Stewardship Savings Breakdown",
            height=400
        )
        
        st.plotly_chart(fig, use_container_width=True)
    
    def _show_regulatory_details(self, roi_data):
        """Display detailed Regulatory Reporting metrics"""
        st.markdown("### 📋 Regulatory Reporting Module Details")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("#### Time Metrics")
            st.metric("Reports per Year", f"{roi_data['reports_per_year']:,.0f}")
            st.metric("Manual Hours Required", f"{roi_data['total_hours_manual']:,.0f}")
            st.metric("Hours Saved", f"{roi_data['hours_saved']:,.0f}")
        
        with col2:
            st.markdown("#### Financial Impact")
            st.metric("Labor Savings", f"${roi_data['labor_savings']:,.0f}")
            st.metric("Accuracy Improvement Value", f"${roi_data['accuracy_value']:,.0f}")
            st.metric("Compliance Risk Reduction", f"${roi_data['compliance_value']:,.0f}")
        
        # Efficiency visualization
        import plotly.graph_objects as go
        
        fig = go.Figure()
        
        fig.add_trace(go.Bar(
            name='Manual Process',
            x=['Time Required'],
            y=[roi_data['total_hours_manual']],
            marker_color='#dc3545'
        ))
        
        fig.add_trace(go.Bar(
            name='With PraediAlert',
            x=['Time Required'],
            y=[roi_data['total_hours_manual'] - roi_data['hours_saved']],
            marker_color='#00c389'
        ))
        
        fig.update_layout(
            title="Annual Reporting Time Comparison (Hours)",
            yaxis_title="Hours",
            barmode='group',
            height=350
        )
        
        st.plotly_chart(fig, use_container_width=True)
    
    def _show_budget_breakdown(self, annual_savings):
        """Display actual PraediAlert budget information for VISN21"""
        st.markdown("### 💰 PraediAlert VISN21 Budget Details")
        st.markdown("""
        <p style="font-size: 1.3rem; font-weight: 600; color: #000080; margin-bottom: 20px;">
            Actual budgetary quote for VISN 21 implementation (July 23, 2025)
        </p>
        """, unsafe_allow_html=True)
        
        # Create two columns for budget vs savings comparison
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("#### 📊 5-Year Contract Costs")
            
            # Base year breakdown
            st.markdown(f"""
            <div class="metric-card">
                <div class="metric-label">Base Year Investment</div>
                <div class="metric-value" style="color: #8b0000;">${PRAEDIALERT_BUDGET['base_year']['total']:,}</div>
                <div style="font-size: 1.1rem; margin-top: 10px;">
                    • Annual License: ${PRAEDIALERT_BUDGET['base_year']['annual_license']:,}<br>
                    • Training (5 hospitals): ${PRAEDIALERT_BUDGET['base_year']['training']:,}<br>
                    • Installation: ${PRAEDIALERT_BUDGET['base_year']['installation']:,}
                </div>
            </div>
            """, unsafe_allow_html=True)
            
            # 5-year total
            st.markdown(f"""
            <div class="metric-card" style="margin-top: 20px;">
                <div class="metric-label">Total 5-Year Contract</div>
                <div class="metric-value" style="color: #8b0000;">${PRAEDIALERT_BUDGET['total_5_year_contract']:,}</div>
                <div style="font-size: 1.1rem; margin-top: 10px;">
                    • Per Hospital (5 years): ${PRAEDIALERT_BUDGET['cost_per_hospital']['average_annual'] * 5:,}<br>
                    • Average Annual Cost: ${PRAEDIALERT_BUDGET['total_5_year_contract'] // 5:,}
                </div>
            </div>
            """, unsafe_allow_html=True)
        
        with col2:
            st.markdown("#### 💵 5-Year Projected Savings")
            
            # Calculate 5-year savings
            five_year_savings = annual_savings * 5
            net_benefit = five_year_savings - PRAEDIALERT_BUDGET['total_5_year_contract']
            roi_5year = (net_benefit / PRAEDIALERT_BUDGET['total_5_year_contract']) * 100
            
            st.markdown(f"""
            <div class="metric-card">
                <div class="metric-label">Total 5-Year Savings</div>
                <div class="metric-value" style="color: #006400;">${five_year_savings:,}</div>
                <div style="font-size: 1.1rem; margin-top: 10px;">
                    • Annual Savings: ${annual_savings:,}<br>
                    • Per Hospital Annual: ${annual_savings // 7:,}<br>
                    • Per Hospital 5-Year: ${five_year_savings // 7:,}
                </div>
            </div>
            """, unsafe_allow_html=True)
            
            # Net benefit
            st.markdown(f"""
            <div class="metric-card" style="margin-top: 20px;">
                <div class="metric-label">5-Year Net Benefit</div>
                <div class="metric-value" style="color: {'#006400' if net_benefit > 0 else '#8b0000'};">
                    ${abs(net_benefit):,}
                </div>
                <div style="font-size: 1.1rem; margin-top: 10px;">
                    • 5-Year ROI: {roi_5year:.1f}%<br>
                    • Benefit per Hospital: ${net_benefit // 7:,}
                </div>
            </div>
            """, unsafe_allow_html=True)
        
        # Year-by-year breakdown table
        st.markdown("#### 📅 Year-by-Year Financial Analysis")
        
        years_data = []
        cumulative_cost = 0
        cumulative_savings = 0
        
        # Base year
        cumulative_cost += PRAEDIALERT_BUDGET['base_year']['total']
        cumulative_savings += annual_savings
        years_data.append({
            'Year': 'Base Year',
            'Contract Cost': f"${PRAEDIALERT_BUDGET['base_year']['total']:,}",
            'Annual Savings': f"${annual_savings:,}",
            'Net Benefit': f"${annual_savings - PRAEDIALERT_BUDGET['base_year']['total']:,}",
            'Cumulative Net': f"${cumulative_savings - cumulative_cost:,}"
        })
        
        # Option years
        for i, (year_key, cost) in enumerate(PRAEDIALERT_BUDGET['option_years'].items(), 1):
            cumulative_cost += cost
            cumulative_savings += annual_savings
            net = annual_savings - cost
            years_data.append({
                'Year': f'Option Year {i}',
                'Contract Cost': f"${cost:,}",
                'Annual Savings': f"${annual_savings:,}",
                'Net Benefit': f"${net:,}",
                'Cumulative Net': f"${cumulative_savings - cumulative_cost:,}"
            })
        
        df = pd.DataFrame(years_data)
        
        # Create HTML table with accessibility styling
        html_table = df.to_html(index=False, escape=False)
        html_table = html_table.replace('<table', '<table style="background-color: white !important; width: 100%; border-collapse: collapse;"')
        html_table = html_table.replace('<th', '<th style="background-color: #f5f5f5 !important; color: #000080 !important; padding: 20px !important; font-size: 1.8rem !important; font-weight: 900 !important; border: 2px solid #000080 !important; text-align: left;"')
        html_table = html_table.replace('<td', '<td style="background-color: white !important; color: black !important; padding: 18px !important; font-size: 1.7rem !important; font-weight: 700 !important; border: 1px solid #ddd !important;"')
        
        st.markdown(html_table, unsafe_allow_html=True)
        
        # Feature highlights
        st.markdown("#### ✨ Included Features")
        
        features = PRAEDIALERT_BUDGET['features']
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.markdown(f"""
            <div style="background: white; border: 2px solid #000080; border-radius: 8px; padding: 15px;">
                <h5 style="color: #000080; margin-bottom: 10px;">Infrastructure</h5>
                • VISN-level installation<br>
                • VistA integration<br>
                • PICIS integration<br>
                • {features['virtual_servers_by']}
            </div>
            """, unsafe_allow_html=True)
        
        with col2:
            st.markdown(f"""
            <div style="background: white; border: 2px solid #006400; border-radius: 8px; padding: 15px;">
                <h5 style="color: #006400; margin-bottom: 10px;">Data & Access</h5>
                • {features['historical_data_years']} years historical data<br>
                • {features['min_users_per_site']} users per site min<br>
                • Role-based permissions<br>
                • {features['number_of_hospitals']} hospitals covered
            </div>
            """, unsafe_allow_html=True)
        
        with col3:
            st.markdown(f"""
            <div style="background: white; border: 2px solid #8b0000; border-radius: 8px; padding: 15px;">
                <h5 style="color: #8b0000; margin-bottom: 10px;">Support</h5>
                • Annual maintenance<br>
                • Technical support<br>
                • Software updates<br>
                • Training included
            </div>
            """, unsafe_allow_html=True)