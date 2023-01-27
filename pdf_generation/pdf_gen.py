from fpdf import FPDF
import os
import sys

path = os.path.abspath(os.path.join(os.path.dirname(__file__)))
sys.path.append(path)
import dial_gauge
import word_cloud


def generate_pdf(gpt3_response):
    pdf = FPDF()

    # Transcript page
    pdf.add_page()
    pdf.set_font('arial', size=30, style='B')  # page dimensions are 210 x 297

    # Title
    pdf.cell(190, 20, txt="Transcript", ln=1, align='C', border=True)
    # Add an empty line
    pdf.ln(10)
    pdf.set_font('arial', size=12)
    # read a txt file and add it to a new cell
    with open('docs/conversation-log/text.txt', 'r') as f:
        for line in f.readlines():
            pdf.multi_cell(190, 5, txt=line, ln=1, align='L', border=False)
    # Create a cell that can take multiple lines
    pdf.multi_cell(190, 5, txt=gpt3_response, align='L', border=True)

    # Empower page
    pdf.add_page()
    pdf.set_font('arial', size=30, style='B')

    # Title
    pdf.cell(190, 20, txt="Empower", ln=1, align='C', border=True)
    # Add an empty line
    pdf.ln(10)
    pdf.set_font('arial', size=12)

    pdf.image(dial_gauge.gauge(labels=['LOW', 'MEDIUM', 'HIGH', 'EXTREME'],
                         colors=['#007A00', '#0063BF', '#FFCC00', '#ED1C24'],
                         arrow=3, title='Questions Asked'),
              x=12, y=42, w=72, h=54)
    pdf.image(dial_gauge.gauge(labels=['LOW', 'MEDIUM', 'HIGH', 'EXTREME'],
                         colors=['#007A00', '#0063BF', '#FFCC00', '#ED1C24'],
                         arrow=3, title='Open Ended Questions'),
              x=12, y=100, w=72, h=54)

    # Be Explicit page
    pdf.add_page()
    pdf.set_font('arial', size=30, style='B')

    # Title
    pdf.cell(190, 20, txt="Be Explicit", ln=1, align='C', border=True)
    # Add an empty line
    pdf.ln(10)
    pdf.set_font('arial', size=12)

    # Graphs
    pdf.image(word_cloud.get_word_cloud(
        "Hedge Word Cloud"), x=12, y=42, w=72, h=72)
    pdf.image(dial_gauge.gauge(labels=['LOW', 'MEDIUM', 'HIGH', 'EXTREME'],
                         colors=['#007A00', '#0063BF', '#FFCC00', '#ED1C24'],
                         arrow=3, title='Hedge Words (%)'),
              x=12, y=118, w=72, h=54)
    pdf.image(dial_gauge.gauge(labels=['LOW', 'MEDIUM', 'HIGH', 'EXTREME'],
                         colors=['#007A00', '#0063BF', '#FFCC00', '#ED1C24'],
                         arrow=3, title='Speaking Rate'),
              x=12, y=176, w=72, h=54)
    pdf.image(dial_gauge.gauge(labels=['LOW', 'MEDIUM', 'HIGH', 'EXTREME'],
                         colors=['#007A00', '#0063BF', '#FFCC00', '#ED1C24'],
                         arrow=3, title='Reading Level'),
              x=12, y=232, w=72, h=54)

    # Empathize page
    pdf.add_page()
    pdf.set_font('arial', size=30, style='B')

    # Title
    pdf.cell(190, 20, txt="Empathize", ln=1, align='C', border=True)
    # Add an empty line
    pdf.ln(10)
    pdf.set_font('arial', size=12)

    pdf.image(dial_gauge.gauge(labels=['LOW', 'MEDIUM', 'HIGH', 'EXTREME'],
                         colors=['#007A00', '#0063BF', '#FFCC00', '#ED1C24'],
                         arrow=3, title='Peronsal Pronouns'),
              x=12, y=42, w=72, h=54)
    pdf.image(word_cloud.get_word_cloud(
        "Empathy Word Cloud"), x=12, y=100, w=72, h=72)
    pdf.image(dial_gauge.gauge(labels=['LOW', 'MEDIUM', 'HIGH', 'EXTREME'],
                         colors=['#007A00', '#0063BF', '#FFCC00', '#ED1C24'],
                         arrow=3, title='Average Empathy'),
              x=12, y=176, w=72, h=54)

    pdf.output("docs/feedback/sophie_feedback.pdf")


def main():
    generate_pdf()


if __name__ == "__main__":
    main()
