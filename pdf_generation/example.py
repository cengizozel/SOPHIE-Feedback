# Import the PyFPDF library
from fpdf import FPDF

# Create a new FPDF object
pdf = FPDF()

# Add a new page to the PDF
pdf.add_page()

# Set the font size and type for the title
pdf.set_font("Arial", size=16, style='B')

# Draw a bordered cell with the title
pdf.cell(200, 10, txt="Title", border=1, align="C")

# Set the font size and type for the paragraph
pdf.set_font("Arial", size=12)

# Draw a bordered cell with the paragraph
pdf.cell(200, 10, txt="Paragraph text", border=1, align="C")

# Save the PDF
pdf.output("example.pdf")
