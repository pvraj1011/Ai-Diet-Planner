from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Image, Table, TableStyle
from reportlab.lib.units import inch
import os
import re

def generate_pdf(content, filename, title):
    """Generate a PDF file from the provided content"""
    # Create directory for PDFs if it doesn't exist
    pdf_dir = "generated_pdfs"
    if not os.path.exists(pdf_dir):
        os.makedirs(pdf_dir)
    
    # Full path for the PDF file
    pdf_path = os.path.join(pdf_dir, filename)
    
    # Create the PDF document
    doc = SimpleDocTemplate(
        pdf_path,
        pagesize=A4,
        rightMargin=72,
        leftMargin=72,
        topMargin=72,
        bottomMargin=72
    )
    
    # Styles
    styles = getSampleStyleSheet()
    styles.add(ParagraphStyle(
        name='CustomHeading1',
        parent=styles['Heading1'],
        fontSize=18,
        spaceAfter=12,
        textColor=colors.darkgreen
    ))
    styles.add(ParagraphStyle(
        name='CustomHeading2',
        parent=styles['Heading2'],
        fontSize=16,
        spaceAfter=10,
        textColor=colors.darkgreen
    ))
    styles.add(ParagraphStyle(
        name='CustomHeading3',
        parent=styles['Heading3'],
        fontSize=14,
        spaceAfter=8,
        textColor=colors.darkgreen
    ))
    styles.add(ParagraphStyle(
        name='CustomNormal',
        parent=styles['Normal'],
        fontSize=12,
        spaceAfter=6
    ))
    
    # Content elements
    elements = []
    
    # Add title
    elements.append(Paragraph(f"<b>{title}</b>", styles['CustomHeading1']))
    elements.append(Spacer(1, 0.25*inch))
    
    # Process the markdown content
    lines = content.split('\n')
    i = 0
    while i < len(lines):
        line = lines[i].strip()
        
        # Handle headings
        if line.startswith('# '):
            elements.append(Paragraph(line[2:], styles['CustomHeading1']))
        elif line.startswith('## '):
            elements.append(Paragraph(line[3:], styles['CustomHeading2']))
        elif line.startswith('### '):
            elements.append(Paragraph(line[4:], styles['CustomHeading3']))
        # Handle lists
        elif line.startswith('- ') or line.startswith('* '):
            elements.append(Paragraph(f"• {line[2:]}", styles['CustomNormal']))
        elif re.match(r'^\d+\.', line):
            num, text = line.split('.', 1)
            elements.append(Paragraph(f"{num}. {text}", styles['CustomNormal']))
        # Handle normal text
        elif line:
            elements.append(Paragraph(line, styles['CustomNormal']))
        
        i += 1
    
    # Build the PDF
    doc.build(elements)
    
    return pdf_path