from fpdf import FPDF
import dial_gen

def generate_pdf():
    pdf = FPDF()

    # Add horizontal page
    pdf.add_page()
    pdf.set_font('times', size=24) # page dimensions are 210 x 297

    # Big rectangle
    # pdf.rect(5, 4, 200, 290, style='D')

    # 4 equally spaced reactangles inside the big rectangle
    pdf.rect(10, 6, 190, 70)
    pdf.text(12, 16, "Transcript")
    pdf.line(10, 20, 200, 20)
    pdf.text(12, 30, "Transcript goes here.")

    pdf.rect(10, 78, 190, 70)
    pdf.text(12, 88, "Be Explicit - Average")
    pdf.line(10, 92, 200, 92)
    pdf.image(dial_gen.gauge(labels=['LOW','MEDIUM','HIGH','EXTREME'], \
                colors=['#007A00','#0063BF','#FFCC00','#ED1C24'], \
                arrow=3, title='Hedge Words (%)'),\
                x=12, y=93, w=72, h=54)
    
    
    pdf.rect(10, 150, 190, 70)
    pdf.text(12, 160, "Empower - Worse than Average")
    pdf.line(10, 164, 200, 164)
    pdf.image(dial_gen.gauge(labels=['LOW','MEDIUM','HIGH','EXTREME'], \
                colors=['#007A00','#0063BF','#FFCC00','#ED1C24'], \
                arrow=3, title='Questions Asked'),\
                x=12, y=165, w=72, h=54)


    pdf.rect(10, 222, 190, 70)
    pdf.text(12, 232, "Empathize - Better than Average")
    pdf.line(10, 236, 200, 236)
    pdf.image(dial_gen.gauge(labels=['LOW','MEDIUM','HIGH','EXTREME'], \
                colors=['#007A00','#0063BF','#FFCC00','#ED1C24'], \
                arrow=3, title='Peronsal Pronouns'),\
                x=12, y=237, w=72, h=54)

    pdf.output("sophie_feedback.pdf")

def main():
    generate_pdf()

if __name__ == "__main__":
    main()
