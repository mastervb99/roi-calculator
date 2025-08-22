"""
PraediGene ROI Calculator
Handles PGx, TSO500, BIAS2015, and Cytogenetics pipelines
"""

import pandas as pd
import numpy as np
import streamlit as st
from datetime import datetime, timedelta
from config.defaults import PRAEDIGENE_DEFAULTS, FINANCIAL_DEFAULTS
import plotly.express as px
import plotly.graph_objects as go
import sys
from pathlib import Path
sys.path.append(str(Path(__file__).parent.parent))
from ui.data_viewer import show_data_viewer

class PraediGeneCalculator:
    def __init__(self, organization_type):
        self.organization_type = organization_type
        self.defaults = PRAEDIGENE_DEFAULTS.get(organization_type, PRAEDIGENE_DEFAULTS['medium_hospital'])
        self.financial = self._get_financial_defaults()
    
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
    
    def calculate_roi(self):
        """Calculate ROI for all PraediGene pipelines"""
        st.markdown("## 🧬 PraediGene ROI Analysis")
        
        # Create tabs for different views
        tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs([
            "📊 Executive Summary",
            "💊 PGx Pipeline",
            "🧫 TSO500 Pipeline", 
            "🔬 BIAS2015 Pipeline",
            "🧪 Cytogenetics Pipeline",
            "📋 Source Data"
        ])
        
        # Calculate individual pipelines
        pgx_roi = self.calculate_pgx()
        tso500_roi = self.calculate_tso500()
        bias2015_roi = self.calculate_bias2015()
        cytogenetics_roi = self.calculate_cytogenetics()
        
        # Combine results
        total_savings = (
            pgx_roi['total_savings'] +
            tso500_roi['total_savings'] +
            bias2015_roi['total_savings'] +
            cytogenetics_roi['total_savings']
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
                pgx_roi, tso500_roi, bias2015_roi, cytogenetics_roi
            )
        
        with tab2:
            self._show_pgx_details(pgx_roi)
        
        with tab3:
            self._show_tso500_details(tso500_roi)
        
        with tab4:
            self._show_bias2015_details(bias2015_roi)
        
        with tab5:
            self._show_cytogenetics_details(cytogenetics_roi)
        
        with tab6:
            show_data_viewer('praedigene', self.organization_type)
        
        return {
            'total_savings': total_savings,
            'total_investment': total_investment,
            'roi_percentage': roi_percentage,
            'payback_months': payback_months,
            'pgx': pgx_roi,
            'tso500': tso500_roi,
            'bias2015': bias2015_roi,
            'cytogenetics': cytogenetics_roi
        }
    
    def calculate_pgx(self):
        """Calculate ROI for PGx pipeline"""
        params = self.defaults['pgx']
        
        # Parameters with sliders
        st.sidebar.markdown("### 💊 PGx Parameters")
        
        annual_volume = st.sidebar.number_input(
            "Annual Test Volume",
            min_value=100,
            max_value=5000,
            value=params['annual_volume'],
            step=100,
            help="Number of PGx tests performed annually"
        )
        
        adr_cost = st.sidebar.number_input(
            "Cost per ADR ($)",
            min_value=2000,
            max_value=15000,
            value=params['adr_cost'],
            step=500,
            help="Average cost of an adverse drug reaction"
        )
        
        patient_impact = st.sidebar.slider(
            "Patient Impact (%)",
            min_value=10.0,
            max_value=40.0,
            value=params['patient_impact'],
            step=5.0,
            help="Percentage of patients benefiting from PGx testing"
        )
        
        readmission_rate = st.sidebar.slider(
            "Readmission Reduction (%)",
            min_value=2.0,
            max_value=15.0,
            value=params['readmission_rate'],
            step=1.0,
            help="Reduction in readmission rates"
        )
        
        # Cost assumptions
        in_house_cost_per_test = 200
        outsource_cost_per_test = 350
        adr_rate = 0.12  # 12% baseline ADR rate
        
        # Calculations
        in_house_total = annual_volume * in_house_cost_per_test
        outsource_total = annual_volume * outsource_cost_per_test
        cost_savings = outsource_total - in_house_total
        
        adrs_avoided = annual_volume * adr_rate * (patient_impact / 100)
        adr_savings = adrs_avoided * adr_cost
        
        readmissions_prevented = adrs_avoided * (readmission_rate / 100)
        readmission_savings = readmissions_prevented * 12000  # Average readmission cost
        
        # Medication optimization savings
        medication_savings = annual_volume * 50 * (patient_impact / 100)  # $50 per optimized patient
        
        total_savings = cost_savings + adr_savings + readmission_savings + medication_savings
        roi_percent = (total_savings / in_house_total) * 100 if in_house_total > 0 else 0
        
        return {
            'volume': annual_volume,
            'in_house_cost': in_house_total,
            'outsource_cost': outsource_total,
            'cost_savings': cost_savings,
            'adrs_avoided': adrs_avoided,
            'adr_savings': adr_savings,
            'readmissions_prevented': readmissions_prevented,
            'readmission_savings': readmission_savings,
            'medication_savings': medication_savings,
            'total_savings': total_savings,
            'roi_percent': roi_percent,
            'patient_impact': patient_impact
        }
    
    def calculate_tso500(self):
        """Calculate ROI for TSO500 pipeline"""
        params = self.defaults['tso500']
        
        # Parameters with sliders
        st.sidebar.markdown("### 🧫 TSO500 Parameters")
        
        annual_volume = st.sidebar.number_input(
            "Annual Test Volume",
            min_value=50,
            max_value=1000,
            value=params['annual_volume'],
            step=50,
            help="Number of TSO500 tests performed annually"
        )
        
        treatment_cost = st.sidebar.number_input(
            "Targeted Treatment Cost ($)",
            min_value=15000,
            max_value=50000,
            value=params['treatment_cost'],
            step=1000,
            help="Average cost of targeted therapy"
        )
        
        treatment_success = st.sidebar.slider(
            "Treatment Success Rate (%)",
            min_value=50.0,
            max_value=85.0,
            value=params['treatment_success'],
            step=5.0,
            help="Success rate of targeted therapies"
        )
        
        fte_daily_cost = st.sidebar.number_input(
            "FTE Daily Cost ($)",
            min_value=500,
            max_value=1500,
            value=params['fte_daily_cost'],
            step=100,
            help="Daily cost of FTE time"
        )
        
        # Cost assumptions
        in_house_cost_per_test = 1500
        outsource_cost_per_test = 1800
        in_house_turnaround = 14  # days
        outsource_turnaround = 21  # days
        actionable_rate = 0.28  # 28% of tests find actionable variants
        
        # Calculations
        in_house_total = annual_volume * in_house_cost_per_test
        outsource_total = annual_volume * outsource_cost_per_test
        cost_savings = outsource_total - in_house_total
        
        time_saved_days = annual_volume * (outsource_turnaround - in_house_turnaround)
        time_savings_value = time_saved_days * fte_daily_cost
        
        actionable_variants = annual_volume * actionable_rate
        successful_treatments = actionable_variants * (treatment_success / 100)
        treatment_value = successful_treatments * treatment_cost * 0.3  # 30% value capture
        
        # Clinical trial enrollment value
        trial_enrollment = actionable_variants * 0.15  # 15% eligible for trials
        trial_value = trial_enrollment * 25000  # Value per trial enrollment
        
        total_savings = cost_savings + time_savings_value + treatment_value + trial_value
        roi_percent = (total_savings / in_house_total) * 100 if in_house_total > 0 else 0
        
        return {
            'volume': annual_volume,
            'in_house_cost': in_house_total,
            'outsource_cost': outsource_total,
            'cost_savings': cost_savings,
            'time_saved_days': time_saved_days,
            'time_savings_value': time_savings_value,
            'actionable_variants': actionable_variants,
            'successful_treatments': successful_treatments,
            'treatment_value': treatment_value,
            'trial_enrollment': trial_enrollment,
            'trial_value': trial_value,
            'total_savings': total_savings,
            'roi_percent': roi_percent,
            'treatment_success': treatment_success
        }
    
    def calculate_bias2015(self):
        """Calculate ROI for BIAS2015 pipeline"""
        params = self.defaults['bias2015']
        
        # Parameters with sliders
        st.sidebar.markdown("### 🔬 BIAS2015 Parameters")
        
        annual_tests = st.sidebar.number_input(
            "Annual Test Volume",
            min_value=100,
            max_value=1500,
            value=params['annual_tests'],
            step=50,
            help="Number of BIAS2015 analyses annually"
        )
        
        patient_benefit = st.sidebar.slider(
            "Patient Benefit Score",
            min_value=5,
            max_value=10,
            value=int(params['patient_benefit']),
            step=1,
            help="Clinical benefit score (1-10 scale)"
        )
        
        fte_daily_cost = st.sidebar.number_input(
            "FTE Daily Cost ($)",
            min_value=500,
            max_value=1500,
            value=params['fte_daily_cost'],
            step=100,
            help="Daily cost of FTE time"
        )
        
        # Assumptions
        cost_per_test = 1000
        baseline_turnaround = 14  # days
        turnaround_improvement = 0.35  # 35% faster
        actionable_rate = 0.22  # 22% actionable findings
        
        # Calculations
        total_cost = annual_tests * cost_per_test
        
        time_saved = annual_tests * baseline_turnaround * turnaround_improvement
        time_savings_value = time_saved * fte_daily_cost * (patient_benefit / 10)
        
        actionable_findings = annual_tests * actionable_rate
        clinical_value = actionable_findings * 15000 * (patient_benefit / 10)
        
        # Research and grant value
        research_value = annual_tests * 500  # $500 per test in research value
        
        total_savings = time_savings_value + clinical_value + research_value
        roi_percent = (total_savings / total_cost) * 100 if total_cost > 0 else 0
        
        return {
            'volume': annual_tests,
            'total_cost': total_cost,
            'time_saved': time_saved,
            'time_savings_value': time_savings_value,
            'actionable_findings': actionable_findings,
            'clinical_value': clinical_value,
            'research_value': research_value,
            'total_savings': total_savings,
            'roi_percent': roi_percent,
            'patient_benefit': patient_benefit
        }
    
    def calculate_cytogenetics(self):
        """Calculate ROI for Cytogenetics pipeline"""
        params = self.defaults['cytogenetics']
        
        # Parameters with sliders
        st.sidebar.markdown("### 🧪 Cytogenetics Parameters")
        
        annual_volume = st.sidebar.number_input(
            "Annual Case Volume",
            min_value=100,
            max_value=1000,
            value=params['annual_volume'],
            step=50,
            help="Number of cytogenetics cases annually"
        )
        
        tech_time = st.sidebar.number_input(
            "Tech Time per Case (hours)",
            min_value=1.0,
            max_value=6.0,
            value=params['tech_time'],
            step=0.5,
            help="Technician hours per case"
        )
        
        rerun_cost = st.sidebar.number_input(
            "Cost per Rerun ($)",
            min_value=100,
            max_value=500,
            value=params['rerun_cost'],
            step=50,
            help="Cost when a test needs to be rerun"
        )
        
        fte_daily_cost = st.sidebar.number_input(
            "FTE Daily Cost ($)",
            min_value=500,
            max_value=1500,
            value=params['fte_daily_cost'],
            step=100,
            help="Daily cost of FTE time"
        )
        
        # Assumptions
        in_house_cost_per_case = 600
        outsource_cost_per_case = 850
        rerun_rate_manual = 0.08  # 8% rerun rate manual
        rerun_rate_automated = 0.02  # 2% rerun rate with automation
        turnaround_days = 5
        
        # Calculations
        in_house_total = annual_volume * in_house_cost_per_case
        outsource_total = annual_volume * outsource_cost_per_case
        cost_savings = outsource_total - in_house_total
        
        # Rerun savings
        reruns_prevented = annual_volume * (rerun_rate_manual - rerun_rate_automated)
        rerun_savings = reruns_prevented * rerun_cost
        
        # Labor savings from automation
        manual_hours = annual_volume * tech_time
        automated_hours = manual_hours * 0.4  # 60% reduction
        hours_saved = manual_hours - automated_hours
        labor_savings = (hours_saved / 8) * fte_daily_cost  # Convert to days
        
        # Quality improvements
        quality_value = annual_volume * 100  # $100 per case in quality improvements
        
        total_savings = cost_savings + rerun_savings + labor_savings + quality_value
        roi_percent = (total_savings / in_house_total) * 100 if in_house_total > 0 else 0
        
        return {
            'volume': annual_volume,
            'in_house_cost': in_house_total,
            'outsource_cost': outsource_total,
            'cost_savings': cost_savings,
            'reruns_prevented': reruns_prevented,
            'rerun_savings': rerun_savings,
            'hours_saved': hours_saved,
            'labor_savings': labor_savings,
            'quality_value': quality_value,
            'total_savings': total_savings,
            'roi_percent': roi_percent,
            'tech_time': tech_time
        }
    
    def _show_executive_summary(self, total_savings, total_investment, roi_percentage, payback_months,
                                pgx_roi, tso500_roi, bias2015_roi, cytogenetics_roi):
        """Display executive summary"""
        st.markdown("""
        <div class="main-header">
            <div class="header-title">PraediGene ROI Executive Summary</div>
            <div class="header-subtitle">Precision Medicine & Genetic Testing Platform</div>
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
        
        # Pipeline breakdown
        st.markdown("### 🧬 Savings by Pipeline")
        
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric(
                "PGx Pipeline",
                f"${pgx_roi['total_savings']:,.0f}",
                f"{pgx_roi['volume']} tests/year"
            )
        
        with col2:
            st.metric(
                "TSO500 Pipeline",
                f"${tso500_roi['total_savings']:,.0f}",
                f"{tso500_roi['volume']} tests/year"
            )
        
        with col3:
            st.metric(
                "BIAS2015 Pipeline",
                f"${bias2015_roi['total_savings']:,.0f}",
                f"{bias2015_roi['volume']} tests/year"
            )
        
        with col4:
            st.metric(
                "Cytogenetics",
                f"${cytogenetics_roi['total_savings']:,.0f}",
                f"{cytogenetics_roi['volume']} cases/year"
            )
        
        # Visualization
        fig = go.Figure(data=[
            go.Bar(
                x=['PGx', 'TSO500', 'BIAS2015', 'Cytogenetics', 'Investment'],
                y=[pgx_roi['total_savings'], tso500_roi['total_savings'],
                   bias2015_roi['total_savings'], cytogenetics_roi['total_savings'], -total_investment],
                marker_color=['#00c389', '#0094d8', '#00609c', '#FF6B00', '#dc3545'],
                text=[f"${x:,.0f}" for x in [pgx_roi['total_savings'], tso500_roi['total_savings'],
                      bias2015_roi['total_savings'], cytogenetics_roi['total_savings'], -total_investment]],
                textposition='outside'
            )
        ])
        
        fig.update_layout(
            title="Annual Savings vs Investment by Pipeline",
            yaxis_title="Amount ($)",
            showlegend=False,
            height=400
        )
        
        st.plotly_chart(fig, use_container_width=True)
        
        # Create sunburst chart for savings breakdown
        labels = ['Total', 'PGx', 'TSO500', 'BIAS2015', 'Cytogenetics',
                 'ADR Savings', 'Readmission', 'Medication', 'Cost Savings',
                 'Time Savings', 'Treatment Value', 'Trial Value',
                 'Clinical Value', 'Research Value',
                 'Rerun Savings', 'Labor Savings']
        
        parents = ['', 'Total', 'Total', 'Total', 'Total',
                  'PGx', 'PGx', 'PGx', 'PGx',
                  'TSO500', 'TSO500', 'TSO500',
                  'BIAS2015', 'BIAS2015',
                  'Cytogenetics', 'Cytogenetics']
        
        values = [total_savings, 
                 pgx_roi['total_savings'], tso500_roi['total_savings'],
                 bias2015_roi['total_savings'], cytogenetics_roi['total_savings'],
                 pgx_roi['adr_savings'], pgx_roi['readmission_savings'],
                 pgx_roi['medication_savings'], pgx_roi['cost_savings'],
                 tso500_roi['time_savings_value'], tso500_roi['treatment_value'],
                 tso500_roi['trial_value'],
                 bias2015_roi['clinical_value'], bias2015_roi['research_value'],
                 cytogenetics_roi['rerun_savings'], cytogenetics_roi['labor_savings']]
        
        fig = go.Figure(go.Sunburst(
            labels=labels,
            parents=parents,
            values=values,
            branchvalues="total",
            marker=dict(colorscale='Blues'),
        ))
        
        fig.update_layout(
            title="Savings Breakdown Hierarchy",
            height=500
        )
        
        st.plotly_chart(fig, use_container_width=True)
    
    def _show_pgx_details(self, roi_data):
        """Display detailed PGx metrics"""
        st.markdown("### 💊 PGx Pipeline Details")
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.markdown("#### Volume & Cost")
            st.metric("Annual Volume", f"{roi_data['volume']:,}")
            st.metric("In-house Cost", f"${roi_data['in_house_cost']:,.0f}")
            st.metric("Cost Savings", f"${roi_data['cost_savings']:,.0f}")
        
        with col2:
            st.markdown("#### Clinical Impact")
            st.metric("ADRs Avoided", f"{roi_data['adrs_avoided']:.0f}")
            st.metric("ADR Savings", f"${roi_data['adr_savings']:,.0f}")
            st.metric("Patient Impact", f"{roi_data['patient_impact']:.0f}%")
        
        with col3:
            st.markdown("#### Readmissions")
            st.metric("Prevented", f"{roi_data['readmissions_prevented']:.0f}")
            st.metric("Savings", f"${roi_data['readmission_savings']:,.0f}")
            st.metric("ROI", f"{roi_data['roi_percent']:.0f}%")
        
        # Monthly projection
        months = pd.date_range(start='2024-01', periods=12, freq='ME')
        monthly_savings = roi_data['total_savings'] / 12
        cumulative = np.cumsum([monthly_savings] * 12)
        
        fig = go.Figure()
        fig.add_trace(go.Scatter(
            x=months, y=cumulative,
            mode='lines+markers',
            name='Cumulative Savings',
            line=dict(color='#00c389', width=3),
            fill='tonexty'
        ))
        
        fig.update_layout(
            title="PGx Pipeline Cumulative Savings Projection",
            xaxis_title="Month",
            yaxis_title="Cumulative Savings ($)",
            height=350
        )
        
        st.plotly_chart(fig, use_container_width=True)
    
    def _show_tso500_details(self, roi_data):
        """Display detailed TSO500 metrics"""
        st.markdown("### 🧫 TSO500 Pipeline Details")
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.markdown("#### Testing Metrics")
            st.metric("Annual Volume", f"{roi_data['volume']:,}")
            st.metric("Actionable Variants", f"{roi_data['actionable_variants']:.0f}")
            st.metric("Cost Savings", f"${roi_data['cost_savings']:,.0f}")
        
        with col2:
            st.markdown("#### Treatment Impact")
            st.metric("Successful Treatments", f"{roi_data['successful_treatments']:.0f}")
            st.metric("Treatment Value", f"${roi_data['treatment_value']:,.0f}")
            st.metric("Success Rate", f"{roi_data['treatment_success']:.0f}%")
        
        with col3:
            st.markdown("#### Time & Trials")
            st.metric("Days Saved", f"{roi_data['time_saved_days']:.0f}")
            st.metric("Trial Enrollments", f"{roi_data['trial_enrollment']:.0f}")
            st.metric("ROI", f"{roi_data['roi_percent']:.0f}%")
        
        # Breakdown pie chart
        fig = go.Figure(data=[go.Pie(
            labels=['Cost Savings', 'Time Value', 'Treatment Value', 'Trial Value'],
            values=[roi_data['cost_savings'], roi_data['time_savings_value'],
                   roi_data['treatment_value'], roi_data['trial_value']],
            hole=.4,
            marker_colors=['#00609c', '#0094d8', '#00c389', '#FF6B00']
        )])
        
        fig.update_layout(
            title="TSO500 Savings Components",
            height=350
        )
        
        st.plotly_chart(fig, use_container_width=True)
    
    def _show_bias2015_details(self, roi_data):
        """Display detailed BIAS2015 metrics"""
        st.markdown("### 🔬 BIAS2015 Pipeline Details")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("#### Analysis Metrics")
            st.metric("Annual Tests", f"{roi_data['volume']:,}")
            st.metric("Time Saved (days)", f"{roi_data['time_saved']:.0f}")
            st.metric("Actionable Findings", f"{roi_data['actionable_findings']:.0f}")
        
        with col2:
            st.markdown("#### Value Generation")
            st.metric("Clinical Value", f"${roi_data['clinical_value']:,.0f}")
            st.metric("Research Value", f"${roi_data['research_value']:,.0f}")
            st.metric("ROI", f"{roi_data['roi_percent']:.0f}%")
        
        # Patient benefit visualization
        benefit_score = roi_data['patient_benefit']
        fig = go.Figure(go.Indicator(
            mode = "gauge+number",
            value = benefit_score,
            title = {'text': "Patient Benefit Score"},
            domain = {'x': [0, 1], 'y': [0, 1]},
            gauge = {
                'axis': {'range': [None, 10]},
                'bar': {'color': "#00c389"},
                'steps': [
                    {'range': [0, 3], 'color': "#f8f9fa"},
                    {'range': [3, 7], 'color': "#e9ecef"},
                    {'range': [7, 10], 'color': "#dee2e6"}
                ],
                'threshold': {
                    'line': {'color': "red", 'width': 4},
                    'thickness': 0.75,
                    'value': 9
                }
            }
        ))
        
        fig.update_layout(height=300)
        st.plotly_chart(fig, use_container_width=True)
    
    def _show_cytogenetics_details(self, roi_data):
        """Display detailed Cytogenetics metrics"""
        st.markdown("### 🧪 Cytogenetics Pipeline Details")
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.markdown("#### Case Metrics")
            st.metric("Annual Cases", f"{roi_data['volume']:,}")
            st.metric("Tech Time/Case", f"{roi_data['tech_time']:.1f} hrs")
            st.metric("Cost Savings", f"${roi_data['cost_savings']:,.0f}")
        
        with col2:
            st.markdown("#### Quality Impact")
            st.metric("Reruns Prevented", f"{roi_data['reruns_prevented']:.0f}")
            st.metric("Rerun Savings", f"${roi_data['rerun_savings']:,.0f}")
            st.metric("Quality Value", f"${roi_data['quality_value']:,.0f}")
        
        with col3:
            st.markdown("#### Efficiency")
            st.metric("Hours Saved", f"{roi_data['hours_saved']:.0f}")
            st.metric("Labor Savings", f"${roi_data['labor_savings']:,.0f}")
            st.metric("ROI", f"{roi_data['roi_percent']:.0f}%")
        
        # Efficiency comparison
        fig = go.Figure()
        
        categories = ['Manual Process', 'With PraediGene']
        manual_hours = roi_data['volume'] * roi_data['tech_time']
        automated_hours = manual_hours - roi_data['hours_saved']
        
        fig.add_trace(go.Bar(
            x=categories,
            y=[manual_hours, automated_hours],
            marker_color=['#dc3545', '#00c389'],
            text=[f"{manual_hours:.0f} hrs", f"{automated_hours:.0f} hrs"],
            textposition='outside'
        ))
        
        fig.update_layout(
            title="Annual Labor Hours Comparison",
            yaxis_title="Hours",
            height=350
        )
        
        st.plotly_chart(fig, use_container_width=True)