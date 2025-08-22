"""
Export handler for ROI Calculator
Generates reports and Excel exports
"""

import pandas as pd
import io
from datetime import datetime
import base64
from reportlab.lib import colors
from reportlab.lib.pagesizes import letter, A4
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer, PageBreak, Image
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.lib.enums import TA_CENTER, TA_RIGHT
import xlsxwriter

class ExportHandler:
    def __init__(self):
        self.timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    
    def generate_report(self, roi_results, product_type, organization_type):
        """Generate PDF report"""
        buffer = io.BytesIO()
        doc = SimpleDocTemplate(buffer, pagesize=letter)
        story = []
        styles = getSampleStyleSheet()
        
        # Custom styles
        title_style = ParagraphStyle(
            'CustomTitle',
            parent=styles['Title'],
            fontSize=24,
            textColor=colors.HexColor('#00609c'),
            alignment=TA_CENTER
        )
        
        heading_style = ParagraphStyle(
            'CustomHeading',
            parent=styles['Heading1'],
            fontSize=16,
            textColor=colors.HexColor('#00609c'),
            spaceAfter=12
        )
        
        # Title page
        product_name = "PraediGene" if product_type == "praedigene" else "PraediAlert"
        story.append(Paragraph(f"{product_name} ROI Analysis Report", title_style))
        story.append(Spacer(1, 0.5*inch))
        
        # Organization info - handle VISN21 specially
        if organization_type == 'visn21':
            org_text = 'VISN21'
        else:
            org_text = organization_type.replace('_', ' ').title()
        story.append(Paragraph(f"Organization: {org_text}", styles['Heading2']))
        story.append(Paragraph(f"Report Date: {datetime.now().strftime('%B %d, %Y')}", styles['Normal']))
        story.append(Spacer(1, 0.5*inch))
        
        # Executive Summary
        story.append(Paragraph("Executive Summary", heading_style))
        
        summary_data = [
            ['Metric', 'Value'],
            ['Total Annual Savings', f"${roi_results['total_savings']:,.0f}"],
            ['Total Investment', f"${roi_results['total_investment']:,.0f}"],
            ['Return on Investment', f"{roi_results['roi_percentage']:.0f}%"],
            ['Payback Period', f"{roi_results['payback_months']:.1f} months"]
        ]
        
        summary_table = Table(summary_data, colWidths=[3*inch, 2*inch])
        summary_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#00609c')),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 12),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
            ('GRID', (0, 0), (-1, -1), 1, colors.black)
        ]))
        
        story.append(summary_table)
        story.append(PageBreak())
        
        # Detailed breakdown
        if product_type == "praedigene":
            story.append(Paragraph("Pipeline Analysis", heading_style))
            
            pipeline_data = [
                ['Pipeline', 'Volume', 'Savings', 'ROI %'],
                ['PGx', f"{roi_results['pgx']['volume']:,}", 
                 f"${roi_results['pgx']['total_savings']:,.0f}",
                 f"{roi_results['pgx']['roi_percent']:.0f}%"],
                ['TSO500', f"{roi_results['tso500']['volume']:,}",
                 f"${roi_results['tso500']['total_savings']:,.0f}",
                 f"{roi_results['tso500']['roi_percent']:.0f}%"],
                ['BIAS2015', f"{roi_results['bias2015']['volume']:,}",
                 f"${roi_results['bias2015']['total_savings']:,.0f}",
                 f"{roi_results['bias2015']['roi_percent']:.0f}%"],
                ['Cytogenetics', f"{roi_results['cytogenetics']['volume']:,}",
                 f"${roi_results['cytogenetics']['total_savings']:,.0f}",
                 f"{roi_results['cytogenetics']['roi_percent']:.0f}%"]
            ]
        else:
            story.append(Paragraph("Module Analysis", heading_style))
            
            pipeline_data = [
                ['Module', 'Key Metric', 'Savings'],
                ['IPC Surveillance', 
                 f"{roi_results['ipc']['hais_prevented']:.0f} HAIs prevented",
                 f"${roi_results['ipc']['total_savings']:,.0f}"],
                ['Antimicrobial', 
                 f"{roi_results['antimicrobial']['dot_reduced']:,.0f} DOT reduced",
                 f"${roi_results['antimicrobial']['total_savings']:,.0f}"],
                ['Regulatory', 
                 f"{roi_results['regulatory']['hours_saved']:,.0f} hours saved",
                 f"${roi_results['regulatory']['total_savings']:,.0f}"]
            ]
        
        detail_table = Table(pipeline_data, colWidths=[2*inch, 2.5*inch, 2*inch])
        detail_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#FF6B00')),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 11),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('BACKGROUND', (0, 1), (-1, -1), colors.lightgrey),
            ('GRID', (0, 0), (-1, -1), 1, colors.black)
        ]))
        
        story.append(detail_table)
        
        # Build PDF
        doc.build(story)
        buffer.seek(0)
        return buffer.getvalue()
    
    def export_to_excel(self, roi_results, product_type):
        """Export results to Excel workbook"""
        output = io.BytesIO()
        
        with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
            workbook = writer.book
            
            # Define formats
            header_format = workbook.add_format({
                'bold': True,
                'bg_color': '#00609c',
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
                'align': 'right',
                'border': 1
            })
            
            number_format = workbook.add_format({
                'num_format': '#,##0',
                'align': 'right',
                'border': 1
            })
            
            # Executive Summary sheet
            summary_data = pd.DataFrame({
                'Metric': ['Total Annual Savings', 'Total Investment', 'ROI Percentage', 'Payback Months'],
                'Value': [
                    roi_results['total_savings'],
                    roi_results['total_investment'],
                    roi_results['roi_percentage'],
                    roi_results['payback_months']
                ]
            })
            
            summary_data.to_excel(writer, sheet_name='Executive Summary', index=False)
            worksheet = writer.sheets['Executive Summary']
            
            # Format the summary sheet
            for row in range(1, len(summary_data) + 1):
                if row <= 2:
                    worksheet.write(row, 1, summary_data.iloc[row-1, 1], currency_format)
                elif row == 3:
                    worksheet.write(row, 1, summary_data.iloc[row-1, 1]/100, percent_format)
                else:
                    worksheet.write(row, 1, summary_data.iloc[row-1, 1], number_format)
            
            # Component sheets
            if product_type == "praedigene":
                # PGx sheet
                pgx_data = pd.DataFrame({
                    'Metric': ['Volume', 'ADRs Avoided', 'ADR Savings', 'Readmission Savings', 
                              'Medication Savings', 'Total Savings', 'ROI %'],
                    'Value': [
                        roi_results['pgx']['volume'],
                        roi_results['pgx']['adrs_avoided'],
                        roi_results['pgx']['adr_savings'],
                        roi_results['pgx']['readmission_savings'],
                        roi_results['pgx']['medication_savings'],
                        roi_results['pgx']['total_savings'],
                        roi_results['pgx']['roi_percent']
                    ]
                })
                pgx_data.to_excel(writer, sheet_name='PGx Pipeline', index=False)
                
                # TSO500 sheet
                tso500_data = pd.DataFrame({
                    'Metric': ['Volume', 'Actionable Variants', 'Treatment Value', 
                              'Trial Value', 'Time Savings', 'Total Savings', 'ROI %'],
                    'Value': [
                        roi_results['tso500']['volume'],
                        roi_results['tso500']['actionable_variants'],
                        roi_results['tso500']['treatment_value'],
                        roi_results['tso500']['trial_value'],
                        roi_results['tso500']['time_savings_value'],
                        roi_results['tso500']['total_savings'],
                        roi_results['tso500']['roi_percent']
                    ]
                })
                tso500_data.to_excel(writer, sheet_name='TSO500 Pipeline', index=False)
                
                # BIAS2015 sheet
                bias_data = pd.DataFrame({
                    'Metric': ['Volume', 'Time Saved', 'Clinical Value', 
                              'Research Value', 'Total Savings', 'ROI %'],
                    'Value': [
                        roi_results['bias2015']['volume'],
                        roi_results['bias2015']['time_saved'],
                        roi_results['bias2015']['clinical_value'],
                        roi_results['bias2015']['research_value'],
                        roi_results['bias2015']['total_savings'],
                        roi_results['bias2015']['roi_percent']
                    ]
                })
                bias_data.to_excel(writer, sheet_name='BIAS2015 Pipeline', index=False)
                
                # Cytogenetics sheet
                cyto_data = pd.DataFrame({
                    'Metric': ['Volume', 'Reruns Prevented', 'Rerun Savings',
                              'Labor Savings', 'Quality Value', 'Total Savings', 'ROI %'],
                    'Value': [
                        roi_results['cytogenetics']['volume'],
                        roi_results['cytogenetics']['reruns_prevented'],
                        roi_results['cytogenetics']['rerun_savings'],
                        roi_results['cytogenetics']['labor_savings'],
                        roi_results['cytogenetics']['quality_value'],
                        roi_results['cytogenetics']['total_savings'],
                        roi_results['cytogenetics']['roi_percent']
                    ]
                })
                cyto_data.to_excel(writer, sheet_name='Cytogenetics', index=False)
                
            else:  # PraediAlert
                # IPC Surveillance sheet
                ipc_data = pd.DataFrame({
                    'Metric': ['Patient Days', 'HAI Rate', 'HAIs Prevented',
                              'Prevention Savings', 'Early Detection Savings', 'Total Savings'],
                    'Value': [
                        roi_results['ipc']['annual_patient_days'],
                        roi_results['ipc']['current_hai_rate'],
                        roi_results['ipc']['hais_prevented'],
                        roi_results['ipc']['prevention_savings'],
                        roi_results['ipc']['early_detection_savings'],
                        roi_results['ipc']['total_savings']
                    ]
                })
                ipc_data.to_excel(writer, sheet_name='IPC Surveillance', index=False)
                
                # Antimicrobial sheet
                anti_data = pd.DataFrame({
                    'Metric': ['Annual DOT', 'DOT Reduced', 'DOT Savings',
                              'Optimization Savings', 'C.diff Savings', 'Total Savings'],
                    'Value': [
                        roi_results['antimicrobial']['annual_dot'],
                        roi_results['antimicrobial']['dot_reduced'],
                        roi_results['antimicrobial']['dot_savings'],
                        roi_results['antimicrobial']['optimization_savings'],
                        roi_results['antimicrobial']['cdiff_savings'],
                        roi_results['antimicrobial']['total_savings']
                    ]
                })
                anti_data.to_excel(writer, sheet_name='Antimicrobial', index=False)
                
                # Regulatory sheet
                reg_data = pd.DataFrame({
                    'Metric': ['Reports/Year', 'Hours Saved', 'Labor Savings',
                              'Accuracy Value', 'Compliance Value', 'Total Savings'],
                    'Value': [
                        roi_results['regulatory']['reports_per_year'],
                        roi_results['regulatory']['hours_saved'],
                        roi_results['regulatory']['labor_savings'],
                        roi_results['regulatory']['accuracy_value'],
                        roi_results['regulatory']['compliance_value'],
                        roi_results['regulatory']['total_savings']
                    ]
                })
                reg_data.to_excel(writer, sheet_name='Regulatory', index=False)
            
            # 5-year projection sheet
            years = list(range(1, 6))
            projection_data = pd.DataFrame({
                'Year': years,
                'Annual Savings': [roi_results['total_savings'] * year for year in years],
                'Cumulative Investment': [
                    roi_results['total_investment'] if year == 1 
                    else roi_results['total_investment'] + (roi_results['total_investment'] * 0.3 * (year - 1))
                    for year in years
                ],
                'Net Benefit': [
                    roi_results['total_savings'] * year - (
                        roi_results['total_investment'] if year == 1 
                        else roi_results['total_investment'] + (roi_results['total_investment'] * 0.3 * (year - 1))
                    )
                    for year in years
                ]
            })
            projection_data.to_excel(writer, sheet_name='5-Year Projection', index=False)
            
            # Format all sheets
            for sheet_name in writer.sheets:
                worksheet = writer.sheets[sheet_name]
                worksheet.set_column('A:A', 30)
                worksheet.set_column('B:D', 15)
        
        output.seek(0)
        return output.getvalue()
    
    def generate_csv_export(self, roi_results, product_type):
        """Generate CSV export of key metrics"""
        data = {
            'Metric': [],
            'Value': []
        }
        
        # Add summary metrics
        data['Metric'].extend([
            'Total Annual Savings',
            'Total Investment',
            'ROI Percentage',
            'Payback Months'
        ])
        
        data['Value'].extend([
            roi_results['total_savings'],
            roi_results['total_investment'],
            roi_results['roi_percentage'],
            roi_results['payback_months']
        ])
        
        # Add component metrics
        if product_type == "praedigene":
            for pipeline in ['pgx', 'tso500', 'bias2015', 'cytogenetics']:
                data['Metric'].append(f"{pipeline.upper()} Savings")
                data['Value'].append(roi_results[pipeline]['total_savings'])
        else:
            for module in ['ipc', 'antimicrobial', 'regulatory']:
                data['Metric'].append(f"{module.title()} Savings")
                data['Value'].append(roi_results[module]['total_savings'])
        
        df = pd.DataFrame(data)
        return df.to_csv(index=False)