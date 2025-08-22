"""
Enhanced Export Handler with Comprehensive Report Generation
Integrates Stage 1 data collection for detailed reports
"""

import pandas as pd
import numpy as np
import io
from datetime import datetime
import base64
from reportlab.lib import colors
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer, PageBreak
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.lib.enums import TA_CENTER, TA_RIGHT, TA_LEFT
from reportlab.platypus.flowables import Image
from reportlab.graphics.shapes import Drawing
from reportlab.graphics.charts.barcharts import VerticalBarChart
from reportlab.graphics.charts.lineplots import LinePlot
from reportlab.graphics.charts.piecharts import Pie
from reportlab.graphics.charts.legends import Legend
from reportlab.graphics.widgets.markers import makeMarker
import xlsxwriter

from utils.comprehensive_report_data import ComprehensiveReportData
from utils.calculation_documentation import CalculationDocumentation
from utils.visualization_charts import VisualizationCharts
from utils.report_layout import ReportLayout

class EnhancedExportHandler:
    def __init__(self):
        self.timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        self.report_data = ComprehensiveReportData()
        self.comprehensive_data = self.report_data.compile_all_data()
        self.calc_docs = CalculationDocumentation()
        self.viz_charts = VisualizationCharts()
        self.layout = ReportLayout()
        
    def generate_comprehensive_report(self, roi_results, product_type, organization_type):
        """Generate comprehensive PDF report integrating all 5 stages"""
        buffer = io.BytesIO()
        doc = SimpleDocTemplate(
            buffer, 
            pagesize=letter,
            rightMargin=72,
            leftMargin=72,
            topMargin=72,
            bottomMargin=72,
            title=f"PraediAlert ROI Report - {datetime.now().strftime('%B %Y')}",
            author="Bitscopic Analytics"
        )
        
        story = []
        
        # Generate all charts (Stage 3)
        charts = self.viz_charts.generate_all_charts(self.comprehensive_data)
        
        # Use professional layout (Stage 4)
        story = self.layout.create_cover_page(story, product_type, organization_type)
        story = self.layout.create_executive_summary(story, roi_results)
        story = self.layout.create_methodology_section(story)
        story = self.layout.create_results_section(story, charts)
        story = self.layout.create_comparison_section(story, charts)
        story = self.layout.create_appendices(story)
        
        # Build the document with page numbering
        doc.build(story, onFirstPage=self.layout.add_page_numbers, 
                 onLaterPages=self.layout.add_page_numbers)
        
        buffer.seek(0)
        return buffer.getvalue()
    
    def generate_comprehensive_report_legacy(self, roi_results, product_type, organization_type):
        """Legacy comprehensive PDF report generation - kept for compatibility"""
        buffer = io.BytesIO()
        doc = SimpleDocTemplate(
            buffer, 
            pagesize=letter,
            rightMargin=72,
            leftMargin=72,
            topMargin=72,
            bottomMargin=72
        )
        
        story = []
        styles = getSampleStyleSheet()
        
        # Custom styles
        title_style = ParagraphStyle(
            'CustomTitle',
            parent=styles['Title'],
            fontSize=28,
            textColor=colors.HexColor('#003F72'),
            alignment=TA_CENTER,
            spaceAfter=30
        )
        
        subtitle_style = ParagraphStyle(
            'CustomSubtitle',
            parent=styles['Heading1'],
            fontSize=20,
            textColor=colors.HexColor('#003F72'),
            alignment=TA_CENTER,
            spaceAfter=20
        )
        
        heading_style = ParagraphStyle(
            'CustomHeading',
            parent=styles['Heading1'],
            fontSize=18,
            textColor=colors.HexColor('#003F72'),
            spaceAfter=12,
            spaceBefore=20
        )
        
        subheading_style = ParagraphStyle(
            'Subheading',
            parent=styles['Heading2'],
            fontSize=14,
            textColor=colors.HexColor('#003F72'),
            spaceAfter=10
        )
        
        # Cover Page
        story.append(Spacer(1, 2*inch))
        story.append(Paragraph("PraediAlert™ ROI Analysis", title_style))
        story.append(Paragraph("Comprehensive Investment & Return Report", subtitle_style))
        story.append(Spacer(1, 0.5*inch))
        
        # Organization info - handle VISN21 specially
        if organization_type == 'visn21':
            org_text = 'VISN21'
        else:
            org_text = organization_type.replace('_', ' ').title()
        story.append(Paragraph(f"<b>Prepared for:</b> {org_text}", styles['Heading2']))
        story.append(Paragraph(f"<b>Report Date:</b> {datetime.now().strftime('%B %d, %Y')}", styles['Normal']))
        story.append(Spacer(1, 0.5*inch))
        
        # Key highlight box
        highlight_data = [
            ['Based on Proven Results from 8 VA Medical Centers'],
            ['43.6% HAI Reduction Achieved'],
            ['18.1% Better Than Control Facilities'],
            ['ROI: 742% First Year | Payback: 12 Months']
        ]
        
        highlight_table = Table(highlight_data, colWidths=[6.5*inch])
        highlight_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, -1), colors.HexColor('#E6F2FF')),
            ('TEXTCOLOR', (0, 0), (-1, -1), colors.HexColor('#003F72')),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, -1), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, -1), 12),
            ('BOX', (0, 0), (-1, -1), 2, colors.HexColor('#003F72')),
            ('LINEBELOW', (0, 0), (-1, -2), 1, colors.HexColor('#003F72')),
            ('TOPPADDING', (0, 0), (-1, -1), 12),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 12),
        ]))
        story.append(highlight_table)
        
        story.append(PageBreak())
        
        # Table of Contents
        story.append(Paragraph("Table of Contents", heading_style))
        toc_data = [
            ['Section', 'Page'],
            ['Executive Summary', '3'],
            ['Study Overview & Methodology', '4'],
            ['8-Facility Performance Analysis', '5'],
            ['Control Group Comparison', '7'],
            ['HAI Type Breakdown', '8'],
            ['Financial Impact Analysis', '9'],
            ['Monthly Trends & Projections', '11'],
            ['Sensitivity Analysis', '12'],
            ['Implementation Recommendations', '13'],
            ['Appendix: Raw Data Tables', '14']
        ]
        
        toc_table = Table(toc_data, colWidths=[4*inch, 1*inch])
        toc_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#003F72')),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('ALIGN', (1, 0), (1, -1), 'RIGHT'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 12),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('GRID', (0, 0), (-1, -1), 1, colors.black)
        ]))
        story.append(toc_table)
        
        story.append(PageBreak())
        
        # Executive Summary
        story.append(Paragraph("Executive Summary", heading_style))
        
        exec_summary_text = f"""
        This comprehensive ROI analysis demonstrates the significant value of implementing PraediAlert™ 
        based on proven results from 8 VA Medical Centers over an 18-month study period. The system 
        achieved a remarkable <b>43.6% reduction in hospital-acquired infections (HAIs)</b>, preventing 
        300 infections and saving an estimated 15 lives.
        """
        story.append(Paragraph(exec_summary_text, styles['Normal']))
        story.append(Spacer(1, 0.2*inch))
        
        # Key metrics table
        summary_data = [
            ['Key Performance Metrics', 'Value', 'Impact'],
            ['Total HAIs Prevented', '300', '$13.5M saved'],
            ['Reduction Rate', '43.6%', '18.1% better than control'],
            ['Lives Saved', '15', 'Invaluable'],
            ['Hospital Days Saved', '2,250', '$4.5M saved'],
            ['Outbreaks Detected', '2', '$2M prevented'],
            ['Total First Year Savings', f"${roi_results.get('total_savings', 0):,}", 'Proven ROI'],
            ['Implementation Investment', f"${roi_results.get('total_investment', 0):,}", '12-month payback'],
            ['First Year ROI', f"{roi_results.get('roi_percentage', 0)}%", 'Exceptional']
        ]
        
        summary_table = Table(summary_data, colWidths=[2.5*inch, 1.5*inch, 2*inch])
        summary_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#003F72')),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('ALIGN', (1, 1), (1, -1), 'CENTER'),
            ('ALIGN', (2, 1), (2, -1), 'RIGHT'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 11),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
            ('GRID', (0, 0), (-1, -1), 1, colors.black),
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE')
        ]))
        story.append(summary_table)
        
        story.append(PageBreak())
        
        # Study Overview & Methodology
        story.append(Paragraph("Study Overview & Methodology", heading_style))
        
        methodology_text = """
        <b>Study Design:</b> Prospective implementation study with concurrent controls<br/>
        <b>Study Period:</b> December 2020 - August 2024 (44 months)<br/>
        <b>Intervention Group:</b> 8 VA Medical Centers (3,093 total beds)<br/>
        <b>Control Group:</b> 117 VA facilities without PraediAlert<br/>
        <b>Primary Outcome:</b> Hospital-acquired infections (POA='N')<br/>
        <b>Secondary Outcomes:</b> Outbreak detection, cost savings, mortality reduction<br/>
        """
        story.append(Paragraph(methodology_text, styles['Normal']))
        story.append(Spacer(1, 0.2*inch))
        
        # Add calculation methodology
        story.append(Paragraph("Calculation Methodology", subheading_style))
        calc_method = self.comprehensive_data['methodology']['hai_reduction']
        calc_text = f"""
        <b>HAI Reduction Formula:</b> {calc_method['formula']}<br/>
        <b>Example:</b> {calc_method['example']}<br/>
        <b>Note:</b> {calc_method['notes']}<br/>
        """
        story.append(Paragraph(calc_text, styles['Normal']))
        
        story.append(PageBreak())
        
        # 8-Facility Performance Analysis
        story.append(Paragraph("8-Facility Performance Analysis", heading_style))
        
        facility_data = self.comprehensive_data['facility_data']['facilities']
        
        # Create facility performance table
        facility_table_data = [
            ['Facility', 'Go-Live', 'Beds', 'Pre-HAIs', 'Post-HAIs', 'Reduction', 'Outcome']
        ]
        
        for facility in facility_data:
            facility_table_data.append([
                facility['name'].replace(' VA Medical Center', ''),
                facility['go_live'].split(',')[0],  # Just month and day
                str(facility['beds']),
                str(facility['pre_hais']),
                str(facility['post_hais']),
                f"{facility['reduction_percent']:.1f}%",
                facility['outcome']
            ])
        
        # Add summary row
        summary_stats = self.comprehensive_data['facility_data']['summary_statistics']
        facility_table_data.append([
            'TOTAL/AVERAGE',
            '-',
            str(summary_stats['total_beds']),
            str(summary_stats['total_pre_hais']),
            str(summary_stats['total_post_hais']),
            f"{summary_stats['average_reduction_percent']}%",
            'Success'
        ])
        
        facility_table = Table(facility_table_data, colWidths=[1.5*inch, 0.8*inch, 0.5*inch, 0.7*inch, 0.7*inch, 0.8*inch, 1*inch])
        facility_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#003F72')),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('ALIGN', (0, 1), (0, -1), 'LEFT'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, -1), 9),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 8),
            ('GRID', (0, 0), (-1, -1), 1, colors.black),
            ('BACKGROUND', (0, -1), (-1, -1), colors.grey),
            ('TEXTCOLOR', (0, -1), (-1, -1), colors.whitesmoke),
            ('FONTNAME', (0, -1), (-1, -1), 'Helvetica-Bold'),
            # Highlight exceptional performers
            ('BACKGROUND', (0, 2), (-1, 2), colors.lightgreen),  # West Palm Beach
            ('BACKGROUND', (0, 8), (-1, 8), colors.lightgreen),  # Dallas
        ]))
        story.append(facility_table)
        
        story.append(Spacer(1, 0.2*inch))
        
        # Add notes about special cases
        special_notes = """
        <b>Special Notes:</b><br/>
        • West Palm Beach and Dallas achieved exceptional reduction rates >60%<br/>
        • New Orleans detected and contained an MRSA community surge<br/>
        • Shreveport identified a CDI cluster, preventing wider outbreak<br/>
        • Palo Alto served as the pilot facility, proving concept viability<br/>
        """
        story.append(Paragraph(special_notes, styles['Normal']))
        
        story.append(PageBreak())
        
        # Control Group Comparison
        story.append(Paragraph("Control Group Comparison", heading_style))
        
        control_data = self.comprehensive_data['control_data']
        
        comparison_data = [
            ['Metric', 'Intervention (8 facilities)', 'Control (117 facilities)', 'Difference'],
            ['Total Pre-Period HAIs', '688', '5,836', '-'],
            ['Total Post-Period HAIs', '388', '4,224', '-'],
            ['Absolute Reduction', '300', '1,612', '-'],
            ['Reduction Rate', '43.6%', '27.6%', '+16.0pp'],
            ['Average per Facility', '37.5', '13.8', '+23.7'],
            ['Relative Improvement', '-', '-', '58% better'],
            ['Statistical Significance', '-', '-', 'p < 0.001']
        ]
        
        comparison_table = Table(comparison_data, colWidths=[2*inch, 1.5*inch, 1.5*inch, 1.5*inch])
        comparison_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#003F72')),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('ALIGN', (0, 1), (0, -1), 'LEFT'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, -1), 10),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 8),
            ('GRID', (0, 0), (-1, -1), 1, colors.black),
            ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
            # Highlight key difference
            ('BACKGROUND', (0, 4), (-1, 4), colors.lightgreen),
            ('FONTNAME', (0, 4), (-1, 4), 'Helvetica-Bold'),
        ]))
        story.append(comparison_table)
        
        story.append(PageBreak())
        
        # Financial Impact Details
        story.append(Paragraph("Financial Impact Analysis", heading_style))
        
        financial_data = self.comprehensive_data['financial_impact']
        
        # Cost breakdown
        story.append(Paragraph("Cost per HAI Breakdown", subheading_style))
        
        cost_breakdown_data = [
            ['Component', 'Cost'],
            ['Direct medical costs', '$30,000'],
            ['Extended LOS (7.5 days × $2,000)', '$15,000'],
            ['Additional treatments', '$5,000'],
            ['Indirect costs', '$10,000'],
            ['Total Cost per HAI', '$45,000']
        ]
        
        cost_table = Table(cost_breakdown_data, colWidths=[3*inch, 1.5*inch])
        cost_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#003F72')),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('ALIGN', (1, 0), (1, -1), 'RIGHT'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, -1), 10),
            ('GRID', (0, 0), (-1, -1), 1, colors.black),
            ('BACKGROUND', (0, -1), (-1, -1), colors.grey),
            ('TEXTCOLOR', (0, -1), (-1, -1), colors.whitesmoke),
            ('FONTNAME', (0, -1), (-1, -1), 'Helvetica-Bold'),
        ]))
        story.append(cost_table)
        
        story.append(Spacer(1, 0.3*inch))
        
        # Investment vs Return
        story.append(Paragraph("Investment vs Return (Your Facility)", subheading_style))
        
        investment_data = [
            ['Category', 'Year 1', 'Years 2-5 (Annual)', '5-Year Total'],
            ['Implementation Cost', f"${roi_results.get('total_investment', 165000):,}", '-', f"${roi_results.get('total_investment', 165000):,}"],
            ['Annual Operating', f"${roi_results.get('annual_operating', 70000):,}", f"${roi_results.get('annual_operating', 70000):,}", f"${roi_results.get('annual_operating', 70000) * 5:,}"],
            ['Total Investment', f"${roi_results.get('total_investment', 235000):,}", f"${roi_results.get('annual_operating', 70000):,}", f"${roi_results.get('total_investment', 165000) + roi_results.get('annual_operating', 70000) * 5:,}"],
            ['', '', '', ''],
            ['HAI Prevention Savings', f"${int(roi_results.get('total_savings', 0) * 0.6):,}", f"${int(roi_results.get('total_savings', 0) * 0.6):,}", f"${int(roi_results.get('total_savings', 0) * 0.6 * 5):,}"],
            ['LOS Reduction Savings', f"${int(roi_results.get('total_savings', 0) * 0.2):,}", f"${int(roi_results.get('total_savings', 0) * 0.2):,}", f"${int(roi_results.get('total_savings', 0) * 0.2 * 5):,}"],
            ['Other Benefits', f"${int(roi_results.get('total_savings', 0) * 0.2):,}", f"${int(roi_results.get('total_savings', 0) * 0.2):,}", f"${int(roi_results.get('total_savings', 0) * 0.2 * 5):,}"],
            ['Total Savings', f"${roi_results.get('total_savings', 0):,}", f"${roi_results.get('total_savings', 0):,}", f"${roi_results.get('total_savings', 0) * 5:,}"],
            ['', '', '', ''],
            ['Net Benefit', f"${roi_results.get('total_savings', 0) - roi_results.get('total_investment', 235000):,}", f"${roi_results.get('total_savings', 0) - roi_results.get('annual_operating', 70000):,}", f"${roi_results.get('total_savings', 0) * 5 - (roi_results.get('total_investment', 165000) + roi_results.get('annual_operating', 70000) * 5):,}"],
            ['ROI %', f"{roi_results.get('roi_percentage', 0)}%", f"{int((roi_results.get('total_savings', 0) - roi_results.get('annual_operating', 70000)) / roi_results.get('annual_operating', 70000) * 100)}%", f"{int((roi_results.get('total_savings', 0) * 5 - (roi_results.get('total_investment', 165000) + roi_results.get('annual_operating', 70000) * 5)) / (roi_results.get('total_investment', 165000) + roi_results.get('annual_operating', 70000) * 5) * 100)}%"]
        ]
        
        investment_table = Table(investment_data, colWidths=[2*inch, 1.3*inch, 1.5*inch, 1.5*inch])
        investment_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#003F72')),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('ALIGN', (1, 0), (-1, -1), 'RIGHT'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, -1), 9),
            ('GRID', (0, 0), (-1, -1), 1, colors.black),
            # Highlight sections
            ('BACKGROUND', (0, 1), (-1, 3), colors.lightyellow),
            ('BACKGROUND', (0, 5), (-1, 8), colors.lightgreen),
            ('BACKGROUND', (0, 10), (-1, 11), colors.lightblue),
            ('FONTNAME', (0, 10), (-1, 11), 'Helvetica-Bold'),
        ]))
        story.append(investment_table)
        
        story.append(PageBreak())
        
        # STAGE 2: Detailed Calculation Documentation
        story.append(Paragraph("Detailed Calculation Methodology", heading_style))
        
        # HAI Reduction Calculations
        hai_calcs = self.calc_docs.get_hai_reduction_calculations()
        story.append(Paragraph("HAI Reduction Rate Calculation", subheading_style))
        
        # Step-by-step calculation table
        calc_steps_data = [['Step', 'Description', 'Formula', 'Example', 'Result']]
        for step in hai_calcs['step_by_step']:
            calc_steps_data.append([
                str(step['step']),
                step['name'],
                step['formula'][:40] + '...' if len(step['formula']) > 40 else step['formula'],
                step['example'][:35] + '...' if len(step['example']) > 35 else step['example'],
                step.get('notes', '')[:25] + '...' if step.get('notes', '') and len(step.get('notes', '')) > 25 else step.get('notes', '')
            ])
        
        calc_steps_table = Table(calc_steps_data, colWidths=[0.5*inch, 1.5*inch, 2*inch, 2*inch, 1.5*inch])
        calc_steps_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#003F72')),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, -1), 8),
            ('GRID', (0, 0), (-1, -1), 1, colors.black),
            ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
            ('VALIGN', (0, 0), (-1, -1), 'TOP')
        ]))
        story.append(calc_steps_table)
        
        story.append(Spacer(1, 0.3*inch))
        
        # Financial Calculations Detail
        story.append(Paragraph("Cost per HAI Detailed Breakdown", subheading_style))
        
        financial_calcs = self.calc_docs.get_financial_calculations()
        cost_components = financial_calcs['cost_per_hai']['components']
        
        cost_detail_data = [['Component', 'Description', 'Amount', 'Calculation']]
        for comp in cost_components:
            cost_detail_data.append([
                comp['item'],
                comp['description'],
                f"${comp['amount']:,}",
                comp['calculation']
            ])
        cost_detail_data.append(['TOTAL', 'Complete cost per HAI', '$45,000', 'Sum of all components'])
        
        cost_detail_table = Table(cost_detail_data, colWidths=[1.5*inch, 2*inch, 1*inch, 2.5*inch])
        cost_detail_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#003F72')),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('ALIGN', (2, 1), (2, -1), 'RIGHT'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, -1), 9),
            ('GRID', (0, 0), (-1, -1), 1, colors.black),
            ('BACKGROUND', (0, -1), (-1, -1), colors.grey),
            ('TEXTCOLOR', (0, -1), (-1, -1), colors.whitesmoke),
            ('FONTNAME', (0, -1), (-1, -1), 'Helvetica-Bold')
        ]))
        story.append(cost_detail_table)
        
        story.append(PageBreak())
        
        # ROI Calculation Walkthrough
        story.append(Paragraph("Return on Investment Calculation", heading_style))
        
        roi_calc = financial_calcs['roi_calculation']
        
        roi_text = f"""
        <b>ROI Formula:</b> {roi_calc['formula']}<br/><br/>
        
        <b>Step 1 - Calculate Benefits:</b><br/>
        {roi_calc['components']['benefits']['formula']}<br/>
        Example: {roi_calc['components']['benefits']['example']}<br/><br/>
        
        <b>Step 2 - Calculate Costs:</b><br/>
        {roi_calc['components']['costs']['formula']}<br/>
        Example: {roi_calc['components']['costs']['example']}<br/><br/>
        
        <b>Step 3 - Calculate ROI:</b><br/>
        {roi_calc['components']['calculation']['formula']}<br/>
        Result: {roi_calc['components']['calculation']['result']}<br/>
        """
        story.append(Paragraph(roi_text, styles['Normal']))
        
        story.append(Spacer(1, 0.3*inch))
        
        # Year-over-year projection table
        story.append(Paragraph("5-Year Financial Projection", subheading_style))
        
        yoy_data = roi_calc['year_over_year']
        projection_data = [['Year', 'Costs', 'Benefits', 'Net Benefit', 'Cumulative Net', 'ROI %']]
        
        for _, row in yoy_data.iterrows():
            projection_data.append([
                str(row['Year']),
                f"${row['Costs']:,}",
                f"${row['Benefits']:,}",
                f"${row['Net']:,}",
                f"${row['Cumulative_Net']:,}",
                f"{row['ROI_Percent']:,}%"
            ])
        
        projection_table = Table(projection_data, colWidths=[0.7*inch, 1.2*inch, 1.3*inch, 1.3*inch, 1.5*inch, 1*inch])
        projection_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#003F72')),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'RIGHT'),
            ('ALIGN', (0, 0), (0, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, -1), 9),
            ('GRID', (0, 0), (-1, -1), 1, colors.black),
            ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
            # Highlight year 1 and year 5
            ('BACKGROUND', (0, 1), (-1, 1), colors.lightgreen),
            ('BACKGROUND', (0, 5), (-1, 5), colors.lightblue)
        ]))
        story.append(projection_table)
        
        story.append(PageBreak())
        
        # Sensitivity Analysis
        story.append(Paragraph("Sensitivity Analysis", heading_style))
        
        sensitivity = self.calc_docs.get_sensitivity_calculations()
        
        sens_text = """
        The following analysis shows how changes in key parameters affect the ROI calculation.
        This helps identify which variables have the greatest impact on financial outcomes.
        """
        story.append(Paragraph(sens_text, styles['Normal']))
        story.append(Spacer(1, 0.2*inch))
        
        # Sensitivity parameters table
        sens_data = [['Parameter', 'Pessimistic', 'Base Case', 'Optimistic', 'Impact']]
        for param in sensitivity['parameters']:
            sens_data.append([
                param['variable'],
                f"{param['range']['pessimistic']}",
                f"{param['base_case']}",
                f"{param['range']['optimistic']}",
                param['impact_calculation']['base']['roi'] if 'base' in param['impact_calculation'] else 'Varies'
            ])
        
        sens_table = Table(sens_data, colWidths=[2*inch, 1.2*inch, 1.2*inch, 1.2*inch, 1*inch])
        sens_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#003F72')),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('ALIGN', (0, 1), (0, -1), 'LEFT'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, -1), 9),
            ('GRID', (0, 0), (-1, -1), 1, colors.black),
            ('BACKGROUND', (0, 1), (-1, -1), colors.beige)
        ]))
        story.append(sens_table)
        
        story.append(PageBreak())
        
        # Control Group Comparison Calculations
        story.append(Paragraph("Control Group Statistical Analysis", heading_style))
        
        control_calcs = self.calc_docs.get_control_comparison_calculations()
        
        did_text = f"""
        <b>Difference-in-Differences (DiD) Analysis</b><br/><br/>
        
        This statistical method isolates the true effect of PraediAlert by comparing changes
        in the intervention group against changes in the control group.<br/><br/>
        
        <b>Formula:</b> {control_calcs['methodology']['formula']}<br/>
        <b>Interpretation:</b> {control_calcs['methodology']['interpretation']}<br/>
        """
        story.append(Paragraph(did_text, styles['Normal']))
        
        # DiD calculation steps
        did_data = [['Step', 'Calculation', 'Result', 'Interpretation']]
        for calc in control_calcs['calculations']:
            did_data.append([
                calc['name'],
                calc['calculation'][:40] + '...' if len(calc['calculation']) > 40 else calc['calculation'],
                f"{calc['result']}{'%' if 'Change' in calc['name'] else 'pp' if 'Difference' in calc['name'] else '%'}",
                calc.get('interpretation', '')[:35] + '...' if calc.get('interpretation', '') and len(calc.get('interpretation', '')) > 35 else calc.get('interpretation', '')
            ])
        
        did_table = Table(did_data, colWidths=[1.8*inch, 2.2*inch, 1*inch, 2*inch])
        did_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#003F72')),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('ALIGN', (2, 0), (2, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, -1), 8),
            ('GRID', (0, 0), (-1, -1), 1, colors.black),
            ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
            ('VALIGN', (0, 0), (-1, -1), 'TOP')
        ]))
        story.append(did_table)
        
        story.append(Spacer(1, 0.2*inch))
        
        # Statistical significance
        stats = control_calcs['statistical_significance']
        stats_text = f"""
        <b>Statistical Validation:</b><br/>
        • Chi-square statistic: {stats['chi_square']}<br/>
        • P-value: {stats['p_value']}<br/>
        • 95% Confidence Interval: {stats['confidence_interval']}<br/>
        • Conclusion: {stats['interpretation']}<br/>
        """
        story.append(Paragraph(stats_text, styles['Normal']))
        
        # Add remaining sections (abbreviated for length)
        story.append(PageBreak())
        story.append(Paragraph("Implementation Recommendations", heading_style))
        
        recommendations = """
        <b>Based on the comprehensive analysis, we recommend:</b><br/><br/>
        
        1. <b>Immediate Implementation:</b> The proven 43.6% HAI reduction rate and 12-month payback period 
        make PraediAlert a high-priority investment.<br/><br/>
        
        2. <b>Phased Rollout:</b> Consider starting with high-risk units (ICU, surgical) where HAI rates 
        and costs are highest.<br/><br/>
        
        3. <b>Staff Training:</b> Allocate adequate resources for comprehensive training to ensure 
        optimal system utilization.<br/><br/>
        
        4. <b>Continuous Monitoring:</b> Establish KPIs and regular review cycles to track performance 
        against the 43.6% benchmark.<br/><br/>
        
        5. <b>Integration Planning:</b> Coordinate with IT to ensure smooth integration with existing 
        EMR and surveillance systems.<br/>
        """
        story.append(Paragraph(recommendations, styles['Normal']))
        
        # Build and return PDF
        doc.build(story)
        buffer.seek(0)
        return buffer.getvalue()
    
    def export_to_excel(self, roi_results, product_type):
        """Export comprehensive results to Excel workbook"""
        output = io.BytesIO()
        
        with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
            workbook = writer.book
            
            # Define formats
            header_format = workbook.add_format({
                'bold': True,
                'bg_color': '#003F72',
                'font_color': 'white',
                'align': 'center',
                'valign': 'vcenter',
                'border': 1
            })
            
            currency_format = workbook.add_format({
                'num_format': '$#,##0',
                'align': 'right',
                'border': 1
            })
            
            percent_format = workbook.add_format({
                'num_format': '0%',
                'align': 'center',
                'border': 1
            })
            
            # Sheet 1: Executive Summary
            summary_df = pd.DataFrame({
                'Metric': ['Total Savings', 'Total Investment', 'ROI %', 'Payback (months)', 'HAIs Prevented'],
                'Value': [
                    roi_results.get('total_savings', 0),
                    roi_results.get('total_investment', 0),
                    roi_results.get('roi_percentage', 0),
                    roi_results.get('payback_months', 0),
                    roi_results.get('hais_prevented', 0)
                ]
            })
            summary_df.to_excel(writer, sheet_name='Executive Summary', index=False)
            
            # Sheet 2: 8-Facility Study Data
            facilities_df = pd.DataFrame(self.comprehensive_data['facility_data']['facilities'])
            facilities_df.to_excel(writer, sheet_name='8 Facility Results', index=False)
            
            # Sheet 3: HAI Type Breakdown
            hai_df = self.comprehensive_data['hai_breakdown']
            hai_df.to_excel(writer, sheet_name='HAI Type Analysis', index=False)
            
            # Sheet 4: Financial Analysis
            financial_dict = self.comprehensive_data['financial_impact']
            financial_rows = []
            for category, values in financial_dict.items():
                if isinstance(values, dict):
                    for key, value in values.items():
                        financial_rows.append({
                            'Category': category.replace('_', ' ').title(),
                            'Item': key.replace('_', ' ').title(),
                            'Value': value
                        })
            financial_df = pd.DataFrame(financial_rows)
            financial_df.to_excel(writer, sheet_name='Financial Analysis', index=False)
            
            # Sheet 5: Monthly Trends
            trends_df = self.comprehensive_data['monthly_trends']
            trends_df.to_excel(writer, sheet_name='Monthly Trends', index=False)
            
            # Format each worksheet
            for sheet_name in writer.sheets:
                worksheet = writer.sheets[sheet_name]
                worksheet.set_column('A:A', 30)
                worksheet.set_column('B:Z', 15)
        
        output.seek(0)
        return output.getvalue()