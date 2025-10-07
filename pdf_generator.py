from reportlab.lib.pagesizes import letter, A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, PageBreak, Table, TableStyle, KeepTogether
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_RIGHT, TA_JUSTIFY
from reportlab.lib import colors
from reportlab.pdfgen import canvas
import os
import re
from datetime import datetime

class NumberedCanvas(canvas.Canvas):
    """Custom canvas to add page numbers and headers"""
    def __init__(self, *args, **kwargs):
        canvas.Canvas.__init__(self, *args, **kwargs)
        self._saved_page_states = []

    def showPage(self):
        self._saved_page_states.append(dict(self.__dict__))
        self._startPage()

    def save(self):
        num_pages = len(self._saved_page_states)
        for state in self._saved_page_states:
            self.__dict__.update(state)
            self.draw_page_number(num_pages)
            canvas.Canvas.showPage(self)
        canvas.Canvas.save(self)

    def draw_page_number(self, page_count):
        page_num = self._pageNumber
        
        if page_num == 1:  # First page (title page)
            # Add "Generated on" date in top right corner
            gen_date = datetime.now().strftime("Generated on: %B %d, %Y")
            self.setFont("Helvetica-Oblique", 9)
            self.setFillColor(colors.grey)
            self.drawRightString(letter[0] - 0.75*inch, letter[1] - 0.75*inch, gen_date)
        
        elif page_num > 1:  # Other pages
            # Header
            self.setFont("Helvetica", 9)
            self.setFillColor(colors.grey)
            self.drawString(inch, letter[1] - 0.5*inch, "Combined Diet & Workout Plan")
            
            # Page number
            text = f"Page {page_num} of {page_count}"
            self.drawRightString(letter[0] - inch, 0.5*inch, text)

def create_custom_styles():
    """Create custom paragraph styles"""
    styles = getSampleStyleSheet()
    
    # Title style
    styles.add(ParagraphStyle(
        name='CustomTitle',
        parent=styles['Heading1'],
        fontSize=24,
        textColor=colors.HexColor('#1a5490'),
        spaceAfter=12,
        alignment=TA_CENTER,
        fontName='Helvetica-Bold'
    ))
    
    # Section header style
    styles.add(ParagraphStyle(
        name='SectionHeader',
        parent=styles['Heading1'],
        fontSize=18,
        textColor=colors.HexColor('#1a5490'),
        spaceAfter=12,
        spaceBefore=16,
        fontName='Helvetica-Bold',
        borderWidth=2,
        borderColor=colors.HexColor('#1a5490'),
        borderPadding=8,
        backColor=colors.HexColor('#e8f4f8')
    ))
    
    # Day header style
    styles.add(ParagraphStyle(
        name='DayHeader',
        parent=styles['Heading2'],
        fontSize=16,
        textColor=colors.white,
        spaceAfter=10,
        spaceBefore=12,
        fontName='Helvetica-Bold',
        backColor=colors.HexColor('#2c7bb6'),
        borderPadding=6
    ))
    
    # Meal category style
    styles.add(ParagraphStyle(
        name='MealCategory',
        parent=styles['Heading3'],
        fontSize=13,
        textColor=colors.HexColor('#2c7bb6'),
        spaceAfter=6,
        fontName='Helvetica-Bold'
    ))
    
    # Important note style
    styles.add(ParagraphStyle(
        name='ImportantNote',
        parent=styles['Normal'],
        fontSize=11,
        textColor=colors.HexColor('#d9534f'),
        fontName='Helvetica-Bold',
        leftIndent=20
    ))
    
    # Bullet style
    styles.add(ParagraphStyle(
        name='CustomBullet',
        parent=styles['Normal'],
        fontSize=11,
        leftIndent=20,
        spaceAfter=6,
        bulletIndent=10
    ))
    
    # Info box style
    styles.add(ParagraphStyle(
        name='InfoBox',
        parent=styles['Normal'],
        fontSize=10,
        backColor=colors.HexColor('#f9f9f9'),
        borderWidth=1,
        borderColor=colors.HexColor('#ddd'),
        borderPadding=10,
        spaceAfter=12
    ))
    
    return styles

def clean_markdown(text):
    """Remove markdown formatting and clean text"""
    # Remove asterisks used for bold/italic
    text = re.sub(r'\*\*\*(.+?)\*\*\*', r'\1', text)  # Bold italic
    text = re.sub(r'\*\*(.+?)\*\*', r'<b>\1</b>', text)  # Bold
    text = re.sub(r'\*(.+?)\*', r'<i>\1</i>', text)  # Italic
    text = re.sub(r'__(.+?)__', r'<b>\1</b>', text)  # Alternative bold
    text = re.sub(r'_(.+?)_', r'<i>\1</i>', text)  # Alternative italic
    
    return text.strip()

def parse_meal_line(line):
    """Parse meal lines and format them properly"""
    # Check if line contains calories
    calorie_match = re.search(r'\((\d+)\s*calories?\)', line, re.IGNORECASE)
    if calorie_match:
        calories = calorie_match.group(1)
        meal_name = line[:calorie_match.start()].strip()
        meal_name = clean_markdown(meal_name)
        return f"<b>{meal_name}</b> <font color='#2c7bb6'>({calories} cal)</font>"
    return clean_markdown(line)

def generate_pdf(content, filename, title, user_details=""):
    """Generate a professional PDF file from the provided content"""
    # Create directory for PDFs if it doesn't exist
    pdf_dir = "generated_pdfs"
    if not os.path.exists(pdf_dir):
        os.makedirs(pdf_dir)
    
    # Full path for the PDF file
    pdf_path = os.path.join(pdf_dir, filename)
    
    # Create the PDF document with custom canvas
    doc = SimpleDocTemplate(
        pdf_path,
        pagesize=letter,
        rightMargin=0.75*inch,
        leftMargin=0.75*inch,
        topMargin=inch,
        bottomMargin=0.75*inch
    )
    
    # Get custom styles
    styles = create_custom_styles()
    
    # Content elements
    elements = []
    
    # Title Page
    elements.append(Spacer(1, 1.5*inch))
    elements.append(Paragraph(title, styles["CustomTitle"]))
    elements.append(Spacer(1, 0.3*inch))
    
    # Format user details nicely
    if user_details and user_details.strip():
        user_info_style = ParagraphStyle(
            'UserInfo',
            parent=styles['Normal'],
            fontSize=12,
            alignment=TA_CENTER,
            spaceAfter=6,
            textColor=colors.HexColor('#555555')
        )
        
        # Split user details by line breaks or commas
        if '\n' in user_details or '|' in user_details:
            details_lines = user_details.replace('|', '<br/>').replace('\n', '<br/>')
            elements.append(Paragraph(details_lines, user_info_style))
        else:
            elements.append(Paragraph(user_details, user_info_style))
    
    # Add generation date
    gen_date = datetime.now().strftime("%B %d, %Y")
    elements.append(Spacer(1, 0.2*inch))
    elements.append(Paragraph(f"<i>Generated on: {gen_date}</i>", 
                             ParagraphStyle('DateStyle', parent=styles['Normal'], 
                                          alignment=TA_CENTER, fontSize=10, textColor=colors.grey)))
    elements.append(PageBreak())
    
    # Process content
    lines = content.split("\n")
    i = 0
    in_list = False
    current_section = []
    
    while i < len(lines):
        line = lines[i].strip()
        
        # Skip empty lines but add spacing
        if not line:
            if current_section:
                elements.extend(current_section)
                current_section = []
            elements.append(Spacer(1, 0.15*inch))
            i += 1
            continue
        
        # Section headers (all caps titles) - Keep with next content
        if line.isupper() and len(line) > 5 and not line.startswith('-'):
            if current_section:
                elements.extend(current_section)
                current_section = []
            elements.append(Spacer(1, 0.2*inch))
            header = Paragraph(line.title(), styles["SectionHeader"])
            elements.append(KeepTogether([header, Spacer(1, 0.15*inch)]))
        
        # Day headers - Keep with next content
        elif line.startswith("**Day ") or re.match(r'\*\*Day \d+', line):
            if current_section:
                elements.extend(current_section)
                current_section = []
            day_text = clean_markdown(line)
            day_header = Paragraph(day_text, styles["DayHeader"])
            elements.append(KeepTogether([day_header]))
        
        # Meal categories (Breakfast, Lunch, Dinner, Snack) - Keep with next content
        elif any(meal in line for meal in ["**Breakfast", "**Lunch", "**Dinner", "**Snack", "**Workout"]):
            if current_section:
                elements.extend(current_section)
                current_section = []
            formatted_line = parse_meal_line(line)
            meal_header = Paragraph(formatted_line, styles["MealCategory"])
            elements.append(KeepTogether([meal_header]))
        
        # Important notes and bold items
        elif line.startswith("**") and ":" in line:
            if current_section:
                elements.extend(current_section)
                current_section = []
            note_text = clean_markdown(line)
            elements.append(Paragraph(f"<b>⚠ {note_text}</b>", styles["ImportantNote"]))
        
        # Bullet points and list items - Collect them
        elif line.startswith("- ") or line.startswith("* "):
            item_text = clean_markdown(line[2:])
            current_section.append(Paragraph(f"• {item_text}", styles["CustomBullet"]))
            in_list = True
        
        # Shopping list categories - Keep with next content
        elif line.startswith("**") and line.endswith(":**"):
            if current_section:
                elements.extend(current_section)
                current_section = []
            category = clean_markdown(line)
            category_header = Paragraph(category, styles["MealCategory"])
            elements.append(KeepTogether([category_header]))
        
        # Section explanations - Keep as single block
        elif "**" in line and ":" in line and len(line) > 30:
            if current_section:
                elements.extend(current_section)
                current_section = []
            formatted = clean_markdown(line)
            elements.append(KeepTogether([Paragraph(formatted, styles["InfoBox"])]))
        
        # Regular text
        else:
            if in_list and not line.startswith(("-", "*")):
                # End of list - wrap list items together
                if current_section:
                    elements.append(KeepTogether(current_section))
                    current_section = []
                in_list = False
            
            clean_line = clean_markdown(line)
            if clean_line:
                elements.append(Paragraph(clean_line, styles["Normal"]))
        
        i += 1
    
    # Add remaining items - wrap list items together
    if current_section:
        if in_list:
            elements.append(KeepTogether(current_section))
        else:
            elements.extend(current_section)
    
    # Build PDF with custom canvas
    doc.build(elements, canvasmaker=NumberedCanvas)
    
    return pdf_path