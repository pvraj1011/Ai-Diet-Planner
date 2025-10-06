from fpdf import FPDF
import os
import re

def generate_pdf(content, filename, title):
    """Generate a PDF file from the provided content using fpdf2"""
    # Create directory for PDFs if it doesn't exist
    pdf_dir = "generated_pdfs"
    if not os.path.exists(pdf_dir):
        os.makedirs(pdf_dir)
    
    # Full path for the PDF file
    pdf_path = os.path.join(pdf_dir, filename)
    
    # Create PDF object
    pdf = FPDF(orientation='P', unit='mm', format='A4')
    pdf.add_page()
    
    # Set up fonts
    pdf.set_font('helvetica', 'B', 18)
    pdf.set_text_color(0, 100, 0)  # Dark green
    
    # Add title
    pdf.cell(0, 10, title, ln=True, align='C')
    pdf.ln(5)
    
    # Process the markdown content
    lines = content.split('\n')
    i = 0
    
    while i < len(lines):
        line = lines[i].strip()
        
        # Handle headings
        if line.startswith('# '):
            pdf.set_font('helvetica', 'B', 16)
            pdf.set_text_color(0, 100, 0)  # Dark green
            pdf.cell(0, 10, line[2:], ln=True)
            pdf.ln(2)
        elif line.startswith('## '):
            pdf.set_font('helvetica', 'B', 14)
            pdf.set_text_color(0, 100, 0)  # Dark green
            pdf.cell(0, 8, line[3:], ln=True)
            pdf.ln(2)
        elif line.startswith('### '):
            pdf.set_font('helvetica', 'B', 12)
            pdf.set_text_color(0, 100, 0)  # Dark green
            pdf.cell(0, 8, line[4:], ln=True)
            pdf.ln(2)
        # Handle lists
        elif line.startswith('- ') or line.startswith('* '):
            pdf.set_font('helvetica', '', 12)
            pdf.set_text_color(0, 0, 0)  # Black
            pdf.cell(5, 6, '•', ln=0)
            pdf.cell(0, 6, line[2:], ln=True)
        elif re.match(r'^\d+\.', line):
            pdf.set_font('helvetica', '', 12)
            pdf.set_text_color(0, 0, 0)  # Black
            num, text = line.split('.', 1)
            pdf.cell(10, 6, f"{num}.", ln=0)
            pdf.cell(0, 6, text.strip(), ln=True)
        # Handle normal text
        elif line:
            pdf.set_font('helvetica', '', 12)
            pdf.set_text_color(0, 0, 0)  # Black
            # Handle long text by using multi_cell
            pdf.multi_cell(0, 6, line)
            pdf.ln(1)
        
        # Add a small space after each paragraph
        if line:
            pdf.ln(1)
        
        i += 1
    
    # Save the PDF
    pdf.output(pdf_path)
    
    return pdf_path