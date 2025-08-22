"""
Stage 4: Report Layout and Formatting
Professional report layout with sections, headers, and structured content
"""

from reportlab.lib import colors
from reportlab.lib.pagesizes import letter, A4
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer, PageBreak, Image, KeepTogether
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.lib.enums import TA_CENTER, TA_RIGHT, TA_LEFT, TA_JUSTIFY
from reportlab.platypus.flowables import HRFlowable
from reportlab.lib.colors import HexColor
import io
import base64
from datetime import datetime

class ReportLayout:
    def __init__(self):
        self.styles = self._create_custom_styles()
        self.colors = {
            'primary': HexColor('#003F72'),      # VA Blue
            'secondary': HexColor('#205493'),    # Medium Blue
            'success': HexColor('#28A745'),      # Green
            'warning': HexColor('#FD7E14'),      # Orange
            'danger': HexColor('#DC3545'),       # Red
            'light': HexColor('#F8F9FA'),        # Light Gray
            'dark': HexColor('#1B3A57'),         # Dark Blue
            'gray': HexColor('#6C757D')          # Gray
        }
    
    def _create_custom_styles(self):
        """Create custom paragraph styles for the report"""
        styles = getSampleStyleSheet()
        
        # Title style
        styles.add(ParagraphStyle(
            name='CustomTitle',
            parent=styles['Title'],
            fontSize=28,
            textColor=HexColor('#003F72'),
            alignment=TA_CENTER,
            spaceAfter=30,
            fontName='Helvetica-Bold'
        ))
        
        # Subtitle style
        styles.add(ParagraphStyle(
            name='CustomSubtitle',
            parent=styles['Title'],
            fontSize=20,
            textColor=HexColor('#205493'),
            alignment=TA_CENTER,
            spaceAfter=20,
            fontName='Helvetica'
        ))
        
        # Section header style
        styles.add(ParagraphStyle(
            name='SectionHeader',
            parent=styles['Heading1'],
            fontSize=18,
            textColor=HexColor('#003F72'),
            alignment=TA_LEFT,
            spaceAfter=12,
            spaceBefore=24,
            fontName='Helvetica-Bold',
            borderColor=HexColor('#003F72'),
            borderWidth=2,
            borderPadding=6
        ))
        
        # Subsection header style
        styles.add(ParagraphStyle(
            name='SubsectionHeader',
            parent=styles['Heading2'],
            fontSize=14,
            textColor=HexColor('#205493'),
            alignment=TA_LEFT,
            spaceAfter=8,
            spaceBefore=12,
            fontName='Helvetica-Bold'
        ))
        
        # Body text style
        styles.add(ParagraphStyle(
            name='CustomBody',
            parent=styles['Normal'],
            fontSize=11,
            textColor=colors.black,
            alignment=TA_JUSTIFY,
            spaceAfter=8,
            leading=14,
            fontName='Helvetica'
        ))
        
        # Highlight box style
        styles.add(ParagraphStyle(
            name='HighlightBox',
            parent=styles['Normal'],
            fontSize=12,
            textColor=HexColor('#003F72'),
            alignment=TA_CENTER,
            spaceAfter=12,
            spaceBefore=12,
            fontName='Helvetica-Bold',
            backColor=HexColor('#E8F4F8'),
            borderColor=HexColor('#003F72'),
            borderWidth=1,
            borderPadding=10
        ))
        
        # Footer style
        styles.add(ParagraphStyle(
            name='Footer',
            parent=styles['Normal'],
            fontSize=9,
            textColor=HexColor('#6C757D'),
            alignment=TA_CENTER,
            fontName='Helvetica'
        ))
        
        return styles
    
    def create_cover_page(self, story, product_type, organization_type):
        """Create professional cover page"""
        # Logo placeholder (would be actual logo in production)
        story.append(Spacer(1, 1*inch))
        
        # Main title
        product_name = "PraediGene™" if product_type == "praedigene" else "PraediAlert™"
        story.append(Paragraph(
            f"{product_name} ROI Analysis",
            self.styles['CustomTitle']
        ))
        
        story.append(Paragraph(
            "Comprehensive Financial Impact Assessment",
            self.styles['CustomSubtitle']
        ))
        
        story.append(Spacer(1, 0.5*inch))
        
        # Organization info box
        org_display = 'VISN21' if organization_type == 'visn21' else organization_type.replace('_', ' ').title()
        
        org_info = f"""
        <para align="center">
        <b>Prepared for:</b><br/>
        {org_display}<br/>
        <br/>
        <b>Analysis Period:</b><br/>
        18-Month Implementation Study<br/>
        <br/>
        <b>Report Date:</b><br/>
        {datetime.now().strftime('%B %d, %Y')}
        </para>
        """
        
        story.append(Paragraph(org_info, self.styles['HighlightBox']))
        
        story.append(Spacer(1, 1*inch))
        
        # Confidence statement
        confidence_text = """
        This report presents a comprehensive return on investment analysis based on 
        real-world implementation data from 8 VA medical facilities. The analysis 
        demonstrates proven clinical outcomes and financial benefits achieved through 
        the deployment of advanced infection prevention and surveillance technology.
        """
        
        story.append(Paragraph(confidence_text, self.styles['CustomBody']))
        
        story.append(PageBreak())
        
        return story
    
    def create_executive_summary(self, story, roi_results):
        """Create executive summary section"""
        story.append(Paragraph("Executive Summary", self.styles['SectionHeader']))
        
        # Key metrics table
        key_metrics = [
            ['Key Performance Indicator', 'Value', 'Impact'],
            ['Total Annual Savings', f"${roi_results['total_savings']:,.0f}", 'Direct financial benefit'],
            ['Total Investment Required', f"${roi_results['total_investment']:,.0f}", 'One-time + annual costs'],
            ['Return on Investment', f"{roi_results['roi_percentage']:.0f}%", 'Net financial gain'],
            ['Payback Period', f"{roi_results['payback_months']:.1f} months", 'Investment recovery time'],
            ['Lives Saved Annually', '12-15', 'Based on mortality reduction'],
            ['HAIs Prevented', '633', 'Annual prevention estimate']
        ]
        
        table = Table(key_metrics, colWidths=[2.5*inch, 1.5*inch, 2.5*inch])
        table.setStyle(self._get_table_style())
        
        story.append(table)
        story.append(Spacer(1, 0.3*inch))
        
        # Key findings
        story.append(Paragraph("Key Findings", self.styles['SubsectionHeader']))
        
        findings = [
            "• 43.6% reduction in hospital-acquired infections across 8 implementation sites",
            "• 41.3 percentage point improvement versus control facilities",
            "• Successful detection of 2 outbreak clusters enabling rapid containment",
            "• Consistent performance across diverse facility sizes and patient populations",
            "• Sustained improvements throughout 18-month evaluation period"
        ]
        
        for finding in findings:
            story.append(Paragraph(finding, self.styles['CustomBody']))
        
        story.append(Spacer(1, 0.3*inch))
        
        # Recommendation box
        recommendation = """
        <para align="center">
        <b>Strategic Recommendation:</b><br/>
        Based on demonstrated clinical efficacy and financial returns, 
        immediate implementation is strongly recommended to maximize 
        patient safety improvements and cost savings.
        </para>
        """
        
        story.append(Paragraph(recommendation, self.styles['HighlightBox']))
        
        story.append(PageBreak())
        
        return story
    
    def create_methodology_section(self, story):
        """Create methodology section"""
        story.append(Paragraph("Methodology & Data Sources", self.styles['SectionHeader']))
        
        story.append(Paragraph(
            "Study Design",
            self.styles['SubsectionHeader']
        ))
        
        methodology_text = """
        This analysis employs a difference-in-differences (DiD) methodology to evaluate 
        the impact of PraediAlert implementation across 8 VA medical facilities. The study 
        compares outcomes between intervention sites and 333 control facilities over 
        equivalent 18-month periods.
        """
        
        story.append(Paragraph(methodology_text, self.styles['CustomBody']))
        
        story.append(Spacer(1, 0.2*inch))
        
        # Data sources table
        story.append(Paragraph("Data Sources", self.styles['SubsectionHeader']))
        
        data_sources = [
            ['Source', 'Description', 'Time Period'],
            ['VA IPEC Database', 'Infection surveillance data', '2019-2024'],
            ['CDW', 'Clinical Data Warehouse records', '2019-2024'],
            ['VSSC', 'VA Safety Surveillance Center', '2020-2024'],
            ['Financial Systems', 'Cost and billing data', '2019-2024']
        ]
        
        table = Table(data_sources, colWidths=[1.8*inch, 2.7*inch, 1.5*inch])
        table.setStyle(self._get_table_style())
        
        story.append(table)
        story.append(Spacer(1, 0.2*inch))
        
        # Statistical methods
        story.append(Paragraph("Statistical Methods", self.styles['SubsectionHeader']))
        
        stats_text = """
        • Primary outcome: Hospital-acquired infections (POA='N' designation)
        • Statistical test: Chi-square test for independence
        • Significance level: p < 0.001
        • Effect size: Cohen's h = 0.82 (large effect)
        • Time normalization: All rates adjusted to 18-month periods
        """
        
        story.append(Paragraph(stats_text, self.styles['CustomBody']))
        
        story.append(PageBreak())
        
        return story
    
    def create_results_section(self, story, charts):
        """Create results section with charts"""
        story.append(Paragraph("Clinical & Financial Results", self.styles['SectionHeader']))
        
        # Facility performance
        story.append(Paragraph("Individual Facility Performance", self.styles['SubsectionHeader']))
        
        performance_text = """
        The following chart demonstrates HAI reduction performance across all 8 implementation 
        facilities. Green bars indicate facilities exceeding the 30% reduction target, while 
        orange bars show facilities that detected outbreak clusters, enabling rapid response.
        """
        
        story.append(Paragraph(performance_text, self.styles['CustomBody']))
        story.append(Spacer(1, 0.2*inch))
        
        # Add facility performance chart
        if 'facility_performance' in charts:
            img = self._create_image_from_base64(charts['facility_performance'], width=5.5*inch)
            story.append(img)
            story.append(Spacer(1, 0.3*inch))
        
        # Timeline
        story.append(Paragraph("Implementation Timeline", self.styles['SubsectionHeader']))
        
        timeline_text = """
        The phased implementation approach allowed for continuous refinement and optimization 
        of the system based on lessons learned from early deployments.
        """
        
        story.append(Paragraph(timeline_text, self.styles['CustomBody']))
        story.append(Spacer(1, 0.2*inch))
        
        if 'timeline' in charts:
            img = self._create_image_from_base64(charts['timeline'], width=5.5*inch)
            story.append(img)
        
        story.append(PageBreak())
        
        # Financial analysis
        story.append(Paragraph("Financial Analysis", self.styles['SubsectionHeader']))
        
        if 'roi_breakdown' in charts:
            img = self._create_image_from_base64(charts['roi_breakdown'], width=5.5*inch)
            story.append(img)
            story.append(Spacer(1, 0.3*inch))
        
        if 'financial_projection' in charts:
            img = self._create_image_from_base64(charts['financial_projection'], width=5.5*inch)
            story.append(img)
        
        story.append(PageBreak())
        
        return story
    
    def create_comparison_section(self, story, charts):
        """Create comparison section"""
        story.append(Paragraph("Intervention vs Control Analysis", self.styles['SectionHeader']))
        
        comparison_text = """
        The following analysis compares outcomes between the 8 intervention facilities 
        implementing PraediAlert and 333 control facilities using traditional infection 
        control methods.
        """
        
        story.append(Paragraph(comparison_text, self.styles['CustomBody']))
        story.append(Spacer(1, 0.2*inch))
        
        if 'comparison' in charts:
            img = self._create_image_from_base64(charts['comparison'], width=5.5*inch)
            story.append(img)
            story.append(Spacer(1, 0.3*inch))
        
        # Statistical significance
        story.append(Paragraph("Statistical Significance", self.styles['SubsectionHeader']))
        
        stats_table = [
            ['Metric', 'Intervention', 'Control', 'Difference', 'P-Value'],
            ['Pre-Period HAIs', '1,453', '48,234', '-', '-'],
            ['Post-Period HAIs', '820', '47,123', '-', '-'],
            ['Reduction %', '43.6%', '2.3%', '41.3pp', '<0.001'],
            ['NNT', '28', 'N/A', '-', '<0.001']
        ]
        
        table = Table(stats_table, colWidths=[1.5*inch, 1.2*inch, 1.2*inch, 1.2*inch, 1*inch])
        table.setStyle(self._get_table_style())
        
        story.append(table)
        
        story.append(PageBreak())
        
        return story
    
    def create_appendices(self, story):
        """Create appendices section"""
        story.append(Paragraph("Appendices", self.styles['SectionHeader']))
        
        # Appendix A: Facility Details
        story.append(Paragraph("Appendix A: Facility Implementation Details", self.styles['SubsectionHeader']))
        
        facility_details = [
            ['Facility', 'Go-Live Date', 'Beds', 'Specialties', 'Region'],
            ['Palo Alto VA', 'Dec 2, 2020', '308', 'Tertiary Care', 'West'],
            ['West Palm Beach VA', 'Jul 22, 2021', '296', 'General Medical', 'Southeast'],
            ['Las Vegas VA', 'Jun 30, 2022', '228', 'General Medical', 'Southwest'],
            ['Greater Los Angeles', 'Aug 1, 2022', '1,087', 'Tertiary Care', 'West'],
            ['New Orleans VA', 'Sep 8, 2022', '198', 'General Medical', 'South'],
            ['Loma Linda VA', 'Oct 11, 2022', '270', 'Tertiary Care', 'West'],
            ['Shreveport VA', 'Apr 23, 2024', '155', 'General Medical', 'South'],
            ['Dallas VA', 'May 21, 2024', '875', 'Tertiary Care', 'Southwest']
        ]
        
        table = Table(facility_details, colWidths=[1.5*inch, 1.2*inch, 0.7*inch, 1.3*inch, 1*inch])
        table.setStyle(self._get_table_style(header_color=self.colors['secondary']))
        
        story.append(table)
        story.append(Spacer(1, 0.3*inch))
        
        # Appendix B: Calculation Details
        story.append(Paragraph("Appendix B: ROI Calculation Methodology", self.styles['SubsectionHeader']))
        
        calc_text = """
        <b>Cost per HAI:</b> $45,000 (CMS estimate, 2024)<br/>
        <b>Annual HAIs Prevented:</b> 633 (based on 43.6% reduction rate)<br/>
        <b>Direct Savings:</b> 633 × $45,000 = $28,485,000<br/>
        <b>Operational Savings:</b> 15% of direct savings = $4,272,750<br/>
        <b>Total Annual Savings:</b> $32,757,750<br/>
        <br/>
        <b>Software Investment:</b> $450,000 (annual license)<br/>
        <b>Implementation Cost:</b> $200,000 (one-time)<br/>
        <b>Training & Support:</b> $350,000 (annual)<br/>
        <b>Total First Year Investment:</b> $1,000,000<br/>
        <br/>
        <b>ROI Calculation:</b> (Savings - Investment) / Investment × 100<br/>
        <b>ROI:</b> ($32,757,750 - $1,000,000) / $1,000,000 × 100 = 3,176%
        """
        
        story.append(Paragraph(calc_text, self.styles['CustomBody']))
        
        return story
    
    def _get_table_style(self, header_color=None):
        """Get standard table style"""
        if header_color is None:
            header_color = self.colors['primary']
        
        return TableStyle([
            # Header row
            ('BACKGROUND', (0, 0), (-1, 0), header_color),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 11),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            
            # Data rows
            ('BACKGROUND', (0, 1), (-1, -1), colors.white),
            ('TEXTCOLOR', (0, 1), (-1, -1), colors.black),
            ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),
            ('FONTSIZE', (0, 1), (-1, -1), 10),
            ('ALIGN', (0, 1), (-1, -1), 'CENTER'),
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
            
            # Alternating row colors
            ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, self.colors['light']]),
            
            # Grid
            ('GRID', (0, 0), (-1, -1), 1, colors.grey),
            ('LINEBELOW', (0, 0), (-1, 0), 2, header_color),
        ])
    
    def _create_image_from_base64(self, base64_string, width=None, height=None):
        """Create ReportLab Image from base64 string with aspect ratio preservation"""
        image_data = base64.b64decode(base64_string)
        image_buffer = io.BytesIO(image_data)
        
        # Create image with aspect ratio preservation
        img = Image(image_buffer)
        
        # Get original dimensions
        img_width, img_height = img.drawWidth, img.drawHeight
        
        # Calculate scaling to fit within page boundaries
        max_width = width or 5.5*inch  # Default max width
        max_height = height or 4*inch   # Default max height
        
        # Calculate scale factors
        scale_w = max_width / img_width if img_width > max_width else 1
        scale_h = max_height / img_height if img_height > max_height else 1
        
        # Use the smaller scale factor to maintain aspect ratio
        scale = min(scale_w, scale_h)
        
        # Apply scaling
        img.drawWidth = img_width * scale
        img.drawHeight = img_height * scale
        
        return img
    
    def add_page_numbers(self, canvas, doc):
        """Add page numbers to each page"""
        canvas.saveState()
        canvas.setFont('Helvetica', 9)
        canvas.setFillColor(self.colors['gray'])
        
        page_num = canvas.getPageNumber()
        text = f"Page {page_num}"
        
        canvas.drawCentredString(letter[0]/2, 0.5*inch, text)
        canvas.restoreState()