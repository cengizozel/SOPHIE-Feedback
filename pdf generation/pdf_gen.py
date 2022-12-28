from fpdf import FPDF

pdf = FPDF()

pdf.add_page()

pdf.set_font('helvetica', size=12)

# It should say "Transcript" in the top center of the page
pdf.cell(200, 10, txt="Transcript", ln=1, align="C")

pdf.output("sophie_feedback.pdf")