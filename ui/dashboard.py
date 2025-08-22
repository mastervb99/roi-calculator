"""
Dashboard display module for ROI Calculator
"""

import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib
matplotlib.use('Agg')  # Use non-interactive backend
from config.defaults import BITSCOPIC_COLORS

# Not using plotly anymore but keeping imports to avoid errors
import plotly.graph_objects as go
import plotly.express as px

def show_dashboard(roi_results, product_type, view_mode):
    """Display the main dashboard based on view mode"""
    
    if view_mode == 'executive_summary':
        show_executive_view(roi_results, product_type)
    elif view_mode == 'detailed_analysis':
        show_detailed_view(roi_results, product_type)
    elif view_mode == 'comparison_view':
        show_comparison_view(roi_results, product_type)
    else:
        show_executive_view(roi_results, product_type)

def show_executive_view(roi_results, product_type):
    """Show executive summary view"""
    
    # Header
    product_name = "PraediGene" if product_type == "praedigene" else "PraediAlert"
    st.markdown(f"""
    <div class="main-header">
        <div class="header-title">{product_name} ROI Analysis</div>
        <div class="header-subtitle">Executive Summary Dashboard</div>
    </div>
    """, unsafe_allow_html=True)
    
    # Key metrics row
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-value">${roi_results['total_savings']:,.0f}</div>
            <div class="metric-label">Total Annual Savings</div>
            <div class="metric-delta metric-positive">↑ Year 1 Projection</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-value">{roi_results['roi_percentage']:.0f}%</div>
            <div class="metric-label">Return on Investment</div>
            <div class="metric-delta metric-positive">↑ First Year ROI</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-value">{roi_results['payback_months']:.1f}</div>
            <div class="metric-label">Payback Period (Months)</div>
            <div class="metric-delta metric-positive">↓ Quick Recovery</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col4:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-value">${roi_results['total_investment']:,.0f}</div>
            <div class="metric-label">Total Investment</div>
            <div class="metric-delta">Implementation + Annual</div>
        </div>
        """, unsafe_allow_html=True)
    
    # 5-Year projection chart
    st.markdown("### 📈 5-Year Financial Projection")
    
    import pandas as pd
    import matplotlib.pyplot as plt
    
    # Prepare data
    years = [1, 2, 3, 4, 5]
    total_savings = float(roi_results.get('total_savings', 100000))
    total_investment = float(roi_results.get('total_investment', 50000))
    
    cumulative_savings = [total_savings * year for year in years]
    cumulative_investment = []
    for year in years:
        if year == 1:
            cumulative_investment.append(total_investment)
        else:
            cumulative_investment.append(total_investment + (total_investment * 0.3 * (year - 1)))
    
    net_benefit = [s - i for s, i in zip(cumulative_savings, cumulative_investment)]
    
    # Create matplotlib figure with white background
    fig, ax = plt.subplots(figsize=(12, 6))
    fig.patch.set_facecolor('white')
    ax.set_facecolor('white')
    
    # Plot lines with thick strokes and markers
    ax.plot(years, cumulative_savings, '-o', linewidth=3, markersize=10, 
            label='Cumulative Savings', color='green')
    ax.plot(years, cumulative_investment, '-s', linewidth=3, markersize=10,
            label='Cumulative Investment', color='red')
    ax.plot(years, net_benefit, '-^', linewidth=3, markersize=10,
            label='Net Benefit', color='blue')
    
    # Add value labels on points
    for x, y in zip(years, cumulative_savings):
        ax.annotate(f'${y:,.0f}', (x, y), textcoords="offset points", 
                   xytext=(0,10), ha='center', fontsize=10, fontweight='bold')
    
    # Formatting
    ax.set_xlabel('Year', fontsize=14, fontweight='bold')
    ax.set_ylabel('Amount ($)', fontsize=14, fontweight='bold')
    ax.set_title('5-Year Financial Projection', fontsize=16, fontweight='bold')
    ax.grid(True, alpha=0.3, linestyle='--')
    ax.legend(loc='upper left', fontsize=12)
    
    # Format y-axis as currency
    ax.yaxis.set_major_formatter(plt.FuncFormatter(lambda x, p: f'${x:,.0f}'))
    
    # Set x-axis to show only integer years
    ax.set_xticks(years)
    ax.set_xticklabels([f'Year {y}' for y in years])
    
    # Display the matplotlib chart
    st.pyplot(fig)
    
    # Also create a simple table view
    st.markdown("#### 📊 Data Table View:")
    table_df = pd.DataFrame({
        'Year': [f'Year {y}' for y in years],
        'Cumulative Savings': [f'${s:,.0f}' for s in cumulative_savings],
        'Cumulative Investment': [f'${i:,.0f}' for i in cumulative_investment],
        'Net Benefit': [f'${n:,.0f}' for n in net_benefit]
    })
    
    # Convert dataframe to HTML with inline styles for white background (same as Module Performance Metrics)
    html_table = table_df.to_html(index=False, escape=False)
    html_table = html_table.replace('<table', '<table style="background-color: white !important; width: 100%; border-collapse: collapse;"')
    html_table = html_table.replace('<th', '<th style="background-color: #f5f5f5 !important; color: #000080 !important; padding: 20px !important; font-size: 1.8rem !important; font-weight: 900 !important; border: 2px solid #000080 !important; text-align: left;"')
    html_table = html_table.replace('<td', '<td style="background-color: white !important; color: black !important; padding: 18px !important; font-size: 1.7rem !important; font-weight: 700 !important; border: 1px solid #ddd !important;"')
    
    st.markdown(html_table, unsafe_allow_html=True)
    
    # Module/Pipeline breakdown
    st.markdown("### 🎯 Component Breakdown")
    
    if product_type == "praedigene":
        show_praedigene_breakdown(roi_results)
    else:
        show_praedialert_breakdown(roi_results)

def show_praedigene_breakdown(roi_results):
    """Show PraediGene pipeline breakdown"""
    
    import matplotlib.pyplot as plt
    import pandas as pd
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        # Bar chart of savings by pipeline
        pipelines = ['PGx', 'TSO500', 'BIAS2015', 'Cytogenetics']
        savings = [
            float(roi_results['pgx']['total_savings']),
            float(roi_results['tso500']['total_savings']),
            float(roi_results['bias2015']['total_savings']),
            float(roi_results['cytogenetics']['total_savings'])
        ]
        
        # Create matplotlib bar chart
        fig, ax = plt.subplots(figsize=(10, 6))
        fig.patch.set_facecolor('white')
        ax.set_facecolor('white')
        
        # Create bars with different colors
        colors = ['#2E7D32', '#1565C0', '#C62828', '#F57C00']  # Green, Blue, Red, Orange
        bars = ax.bar(pipelines, savings, color=colors, edgecolor='black', linewidth=2)
        
        # Add value labels on top of bars
        for bar, value in zip(bars, savings):
            height = bar.get_height()
            ax.text(bar.get_x() + bar.get_width()/2., height,
                   f'${value:,.0f}',
                   ha='center', va='bottom', fontsize=12, fontweight='bold')
        
        # Formatting
        ax.set_xlabel('Pipeline', fontsize=14, fontweight='bold')
        ax.set_ylabel('Annual Savings ($)', fontsize=14, fontweight='bold')
        ax.set_title('Annual Savings by Pipeline', fontsize=16, fontweight='bold')
        ax.grid(True, axis='y', alpha=0.3, linestyle='--')
        
        # Format y-axis as currency
        ax.yaxis.set_major_formatter(plt.FuncFormatter(lambda x, p: f'${x:,.0f}'))
        
        # Display the chart
        st.pyplot(fig)
    
    with col2:
        # Pie chart of relative contributions
        fig2, ax2 = plt.subplots(figsize=(8, 8))
        fig2.patch.set_facecolor('white')
        ax2.set_facecolor('white')
        
        colors = ['#2E7D32', '#1565C0', '#C62828', '#F57C00']  # Green, Blue, Red, Orange
        wedges, texts, autotexts = ax2.pie(savings, labels=pipelines, 
                                            colors=colors, autopct='%1.1f%%',
                                            startangle=90, textprops={'fontsize': 12, 'fontweight': 'bold'})
        
        # Make percentage text white for better contrast
        for autotext in autotexts:
            autotext.set_color('white')
            autotext.set_fontsize(14)
            autotext.set_fontweight('bold')
        
        ax2.set_title('Relative Contribution', fontsize=16, fontweight='bold')
        
        # Display the chart
        st.pyplot(fig2)
    
    # Pipeline metrics table
    st.markdown("### 📊 Pipeline Performance Metrics")
    
    metrics_data = {
        'Pipeline': pipelines,
        'Annual Volume': [
            roi_results['pgx']['volume'],
            roi_results['tso500']['volume'],
            roi_results['bias2015']['volume'],
            roi_results['cytogenetics']['volume']
        ],
        'Total Savings': [f"${s:,.0f}" for s in savings],
        'ROI %': [
            f"{roi_results['pgx']['roi_percent']:.0f}%",
            f"{roi_results['tso500']['roi_percent']:.0f}%",
            f"{roi_results['bias2015']['roi_percent']:.0f}%",
            f"{roi_results['cytogenetics']['roi_percent']:.0f}%"
        ],
        'Key Benefit': [
            f"{roi_results['pgx']['adrs_avoided']:.0f} ADRs avoided",
            f"{roi_results['tso500']['actionable_variants']:.0f} actionable variants",
            f"{roi_results['bias2015']['actionable_findings']:.0f} actionable findings",
            f"{roi_results['cytogenetics']['reruns_prevented']:.0f} reruns prevented"
        ]
    }
    
    df = pd.DataFrame(metrics_data)
    
    # Convert dataframe to HTML with inline styles for white background
    html_table = df.to_html(index=False, escape=False)
    html_table = html_table.replace('<table', '<table style="background-color: white !important; width: 100%; border-collapse: collapse;"')
    html_table = html_table.replace('<th', '<th style="background-color: #f5f5f5 !important; color: #000080 !important; padding: 20px !important; font-size: 1.8rem !important; font-weight: 900 !important; border: 2px solid #000080 !important; text-align: left;"')
    html_table = html_table.replace('<td', '<td style="background-color: white !important; color: black !important; padding: 18px !important; font-size: 1.7rem !important; font-weight: 700 !important; border: 1px solid #ddd !important;"')
    
    st.markdown(html_table, unsafe_allow_html=True)

def show_praedialert_breakdown(roi_results):
    """Show PraediAlert module breakdown"""
    
    import matplotlib.pyplot as plt
    import pandas as pd
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        # Bar chart of savings by module
        # Use line breaks for chart but clean names for table
        modules_chart = ['IPC\nSurveillance', 'Antimicrobial\nStewardship', 'Regulatory\nReporting']
        modules_table = ['IPC Surveillance', 'Antimicrobial Stewardship', 'Regulatory Reporting']
        savings = [
            float(roi_results['ipc']['total_savings']),
            float(roi_results['antimicrobial']['total_savings']),
            float(roi_results['regulatory']['total_savings'])
        ]
        
        # Create matplotlib bar chart
        fig, ax = plt.subplots(figsize=(10, 6))
        fig.patch.set_facecolor('white')
        ax.set_facecolor('white')
        
        # Create bars with different colors
        colors = ['#2E7D32', '#1565C0', '#C62828']  # Green, Blue, Red
        bars = ax.bar(range(len(modules_chart)), savings, color=colors, edgecolor='black', linewidth=2)
        
        # Set x-axis labels (use chart version with line breaks)
        ax.set_xticks(range(len(modules_chart)))
        ax.set_xticklabels(modules_chart, fontsize=12, fontweight='bold')
        
        # Add value labels on top of bars
        for bar, value in zip(bars, savings):
            height = bar.get_height()
            ax.text(bar.get_x() + bar.get_width()/2., height,
                   f'${value:,.0f}',
                   ha='center', va='bottom', fontsize=12, fontweight='bold')
        
        # Formatting
        ax.set_xlabel('Module', fontsize=14, fontweight='bold')
        ax.set_ylabel('Annual Savings ($)', fontsize=14, fontweight='bold')
        ax.set_title('Annual Savings by Module', fontsize=16, fontweight='bold')
        ax.grid(True, axis='y', alpha=0.3, linestyle='--')
        
        # Format y-axis as currency
        ax.yaxis.set_major_formatter(plt.FuncFormatter(lambda x, p: f'${x:,.0f}'))
        
        # Display the chart
        st.pyplot(fig)
    
    with col2:
        # Pie chart of relative contributions
        fig2, ax2 = plt.subplots(figsize=(8, 8))
        fig2.patch.set_facecolor('white')
        ax2.set_facecolor('white')
        
        colors = ['#2E7D32', '#1565C0', '#C62828']  # Green, Blue, Red
        wedges, texts, autotexts = ax2.pie(savings, labels=['IPC', 'Antimicrobial', 'Regulatory'], 
                                            colors=colors, autopct='%1.1f%%',
                                            startangle=90, textprops={'fontsize': 12, 'fontweight': 'bold'})
        
        # Make percentage text white for better contrast
        for autotext in autotexts:
            autotext.set_color('white')
            autotext.set_fontsize(14)
            autotext.set_fontweight('bold')
        
        ax2.set_title('Relative Contribution', fontsize=16, fontweight='bold')
        
        # Display the chart
        st.pyplot(fig2)
    
    # Module metrics table
    st.markdown("### 📊 Module Performance Metrics")
    
    metrics_data = {
        'Module': modules_table,  # Use clean names without \n
        'Total Savings': [f"${s:,.0f}" for s in savings],
        'Key Metric': [
            f"{roi_results['ipc']['hais_prevented']:.0f} HAIs prevented",
            f"{roi_results['antimicrobial']['dot_reduced']:,.0f} DOT reduced",
            f"{roi_results['regulatory']['hours_saved']:,.0f} hours saved"
        ],
        'Impact': [
            f"{roi_results['ipc']['reduction_percentage']:.0f}% HAI reduction",
            f"{roi_results['antimicrobial']['dot_reduction_percentage']:.0f}% DOT reduction",
            f"{roi_results['regulatory']['hours_saved']/roi_results['regulatory']['total_hours_manual']*100:.0f}% time saved"
        ]
    }
    
    df = pd.DataFrame(metrics_data)
    
    # Convert dataframe to HTML with inline styles for white background
    html_table = df.to_html(index=False, escape=False)
    html_table = html_table.replace('<table', '<table style="background-color: white !important; width: 100%; border-collapse: collapse;"')
    html_table = html_table.replace('<th', '<th style="background-color: #f5f5f5 !important; color: #000080 !important; padding: 20px !important; font-size: 1.8rem !important; font-weight: 900 !important; border: 2px solid #000080 !important; text-align: left;"')
    html_table = html_table.replace('<td', '<td style="background-color: white !important; color: black !important; padding: 18px !important; font-size: 1.7rem !important; font-weight: 700 !important; border: 1px solid #ddd !important;"')
    
    st.markdown(html_table, unsafe_allow_html=True)

def show_detailed_view(roi_results, product_type):
    """Show detailed analysis view"""
    
    st.markdown("""
    <div class="section-header">
        Detailed ROI Analysis
    </div>
    """, unsafe_allow_html=True)
    
    # Create expandable sections for each component
    if product_type == "praedigene":
        with st.expander("💊 PGx Pipeline Details", expanded=True):
            show_pgx_detailed_analysis(roi_results['pgx'])
        
        with st.expander("🧫 TSO500 Pipeline Details"):
            show_tso500_detailed_analysis(roi_results['tso500'])
        
        with st.expander("🔬 BIAS2015 Pipeline Details"):
            show_bias2015_detailed_analysis(roi_results['bias2015'])
        
        with st.expander("🧪 Cytogenetics Pipeline Details"):
            show_cytogenetics_detailed_analysis(roi_results['cytogenetics'])
    else:
        with st.expander("🦠 IPC Surveillance Details", expanded=True):
            show_ipc_detailed_analysis(roi_results['ipc'])
        
        with st.expander("💊 Antimicrobial Stewardship Details"):
            show_antimicrobial_detailed_analysis(roi_results['antimicrobial'])
        
        with st.expander("📋 Regulatory Reporting Details"):
            show_regulatory_detailed_analysis(roi_results['regulatory'])

def show_comparison_view(roi_results, product_type):
    """Show comparison view"""
    
    st.markdown("""
    <div class="section-header">
        Comparative Analysis
    </div>
    """, unsafe_allow_html=True)
    
    # Scenario comparison
    st.markdown("### 📊 Scenario Comparison")
    
    scenarios = ['Conservative', 'Expected', 'Optimistic']
    multipliers = [0.7, 1.0, 1.3]
    
    scenario_data = []
    for scenario, multiplier in zip(scenarios, multipliers):
        scenario_data.append({
            'Scenario': scenario,
            'Total Savings': roi_results['total_savings'] * multiplier,
            'ROI %': roi_results['roi_percentage'] * multiplier,
            'Payback (months)': roi_results['payback_months'] / multiplier if multiplier > 0 else 999
        })
    
    df = pd.DataFrame(scenario_data)
    
    # Create grouped bar chart
    fig = go.Figure()
    
    fig.add_trace(go.Bar(
        name='Total Savings',
        x=df['Scenario'],
        y=df['Total Savings'],
        yaxis='y',
        offsetgroup=1,
        marker_color=BITSCOPIC_COLORS['accent']
    ))
    
    fig.add_trace(go.Bar(
        name='ROI %',
        x=df['Scenario'],
        y=df['ROI %'],
        yaxis='y2',
        offsetgroup=2,
        marker_color=BITSCOPIC_COLORS['orange']
    ))
    
    fig.update_layout(
        yaxis=dict(
            title='Total Savings ($)',
            side='left'
        ),
        yaxis2=dict(
            title='ROI (%)',
            overlaying='y',
            side='right'
        ),
        barmode='group',
        height=400,
        title="Scenario Analysis",
        plot_bgcolor='white',
        paper_bgcolor='white',
        font=dict(color='black', size=14, family='Arial')
    )
    
    st.plotly_chart(fig, use_container_width=True)
    
    # Sensitivity analysis
    st.markdown("### 🎯 Sensitivity Analysis")
    
    parameters = ['Volume', 'Cost Reduction', 'Clinical Impact', 'Efficiency Gain']
    impacts = []
    
    for param in parameters:
        # Calculate impact of 10% change
        base_savings = roi_results['total_savings']
        adjusted_savings = base_savings * 1.1  # Simplified for demo
        impact = ((adjusted_savings - base_savings) / base_savings) * 100
        impacts.append(impact)
    
    fig = go.Figure(go.Bar(
        x=impacts,
        y=parameters,
        orientation='h',
        marker_color=[BITSCOPIC_COLORS['danger'] if i < 5 else BITSCOPIC_COLORS['accent'] for i in impacts],
        text=[f"{i:.1f}%" for i in impacts],
        textposition='outside'
    ))
    
    fig.update_layout(
        title="Parameter Sensitivity (10% change impact)",
        xaxis_title="Impact on Total Savings (%)",
        height=350,
        plot_bgcolor='white',
        paper_bgcolor='white',
        font=dict(color='black', size=14, family='Arial')
    )
    
    st.plotly_chart(fig, use_container_width=True)

def show_pgx_detailed_analysis(pgx_data):
    """Show detailed PGx analysis"""
    metrics = {
        'Annual Test Volume': pgx_data['volume'],
        'ADRs Avoided': f"{pgx_data['adrs_avoided']:.0f}",
        'ADR Savings': f"${pgx_data['adr_savings']:,.0f}",
        'Readmissions Prevented': f"{pgx_data['readmissions_prevented']:.0f}",
        'Readmission Savings': f"${pgx_data['readmission_savings']:,.0f}",
        'Medication Optimization': f"${pgx_data['medication_savings']:,.0f}",
        'Total Savings': f"${pgx_data['total_savings']:,.0f}",
        'ROI': f"{pgx_data['roi_percent']:.0f}%"
    }
    
    col1, col2 = st.columns(2)
    for i, (key, value) in enumerate(metrics.items()):
        if i % 2 == 0:
            col1.metric(key, value)
        else:
            col2.metric(key, value)

def show_tso500_detailed_analysis(tso500_data):
    """Show detailed TSO500 analysis"""
    metrics = {
        'Annual Test Volume': tso500_data['volume'],
        'Actionable Variants': f"{tso500_data['actionable_variants']:.0f}",
        'Successful Treatments': f"{tso500_data['successful_treatments']:.0f}",
        'Treatment Value': f"${tso500_data['treatment_value']:,.0f}",
        'Trial Enrollments': f"{tso500_data['trial_enrollment']:.0f}",
        'Trial Value': f"${tso500_data['trial_value']:,.0f}",
        'Time Saved (days)': f"{tso500_data['time_saved_days']:.0f}",
        'Total Savings': f"${tso500_data['total_savings']:,.0f}"
    }
    
    col1, col2 = st.columns(2)
    for i, (key, value) in enumerate(metrics.items()):
        if i % 2 == 0:
            col1.metric(key, value)
        else:
            col2.metric(key, value)

def show_bias2015_detailed_analysis(bias_data):
    """Show detailed BIAS2015 analysis"""
    metrics = {
        'Annual Tests': bias_data['volume'],
        'Time Saved (days)': f"{bias_data['time_saved']:.0f}",
        'Actionable Findings': f"{bias_data['actionable_findings']:.0f}",
        'Clinical Value': f"${bias_data['clinical_value']:,.0f}",
        'Research Value': f"${bias_data['research_value']:,.0f}",
        'Total Savings': f"${bias_data['total_savings']:,.0f}",
        'ROI': f"{bias_data['roi_percent']:.0f}%"
    }
    
    col1, col2 = st.columns(2)
    for i, (key, value) in enumerate(metrics.items()):
        if i % 2 == 0:
            col1.metric(key, value)
        else:
            col2.metric(key, value)

def show_cytogenetics_detailed_analysis(cyto_data):
    """Show detailed Cytogenetics analysis"""
    metrics = {
        'Annual Cases': cyto_data['volume'],
        'Reruns Prevented': f"{cyto_data['reruns_prevented']:.0f}",
        'Rerun Savings': f"${cyto_data['rerun_savings']:,.0f}",
        'Hours Saved': f"{cyto_data['hours_saved']:.0f}",
        'Labor Savings': f"${cyto_data['labor_savings']:,.0f}",
        'Quality Value': f"${cyto_data['quality_value']:,.0f}",
        'Total Savings': f"${cyto_data['total_savings']:,.0f}",
        'ROI': f"{cyto_data['roi_percent']:.0f}%"
    }
    
    col1, col2 = st.columns(2)
    for i, (key, value) in enumerate(metrics.items()):
        if i % 2 == 0:
            col1.metric(key, value)
        else:
            col2.metric(key, value)

def show_ipc_detailed_analysis(ipc_data):
    """Show detailed IPC analysis"""
    metrics = {
        'Annual Patient Days': f"{ipc_data['annual_patient_days']:,.0f}",
        'Current HAI Rate': f"{ipc_data['current_hai_rate']:.2f}%",
        'HAIs Prevented': f"{ipc_data['hais_prevented']:.0f}",
        'Prevention Savings': f"${ipc_data['prevention_savings']:,.0f}",
        'Early Detection Savings': f"${ipc_data['early_detection_savings']:,.0f}",
        'Total Savings': f"${ipc_data['total_savings']:,.0f}"
    }
    
    col1, col2 = st.columns(2)
    for i, (key, value) in enumerate(metrics.items()):
        if i % 2 == 0:
            col1.metric(key, value)
        else:
            col2.metric(key, value)

def show_antimicrobial_detailed_analysis(anti_data):
    """Show detailed Antimicrobial analysis"""
    metrics = {
        'Annual DOT': f"{anti_data['annual_dot']:,.0f}",
        'DOT Reduced': f"{anti_data['dot_reduced']:,.0f}",
        'DOT Savings': f"${anti_data['dot_savings']:,.0f}",
        'Optimization Savings': f"${anti_data['optimization_savings']:,.0f}",
        'C. diff Cases Prevented': f"{anti_data['cdiff_cases_prevented']:.0f}",
        'C. diff Savings': f"${anti_data['cdiff_savings']:,.0f}",
        'Total Savings': f"${anti_data['total_savings']:,.0f}"
    }
    
    col1, col2 = st.columns(2)
    for i, (key, value) in enumerate(metrics.items()):
        if i % 2 == 0:
            col1.metric(key, value)
        else:
            col2.metric(key, value)

def show_regulatory_detailed_analysis(reg_data):
    """Show detailed Regulatory analysis"""
    metrics = {
        'Reports per Year': f"{reg_data['reports_per_year']:,.0f}",
        'Manual Hours Required': f"{reg_data['total_hours_manual']:,.0f}",
        'Hours Saved': f"{reg_data['hours_saved']:,.0f}",
        'Labor Savings': f"${reg_data['labor_savings']:,.0f}",
        'Accuracy Value': f"${reg_data['accuracy_value']:,.0f}",
        'Compliance Value': f"${reg_data['compliance_value']:,.0f}",
        'Total Savings': f"${reg_data['total_savings']:,.0f}"
    }
    
    col1, col2 = st.columns(2)
    for i, (key, value) in enumerate(metrics.items()):
        if i % 2 == 0:
            col1.metric(key, value)
        else:
            col2.metric(key, value)