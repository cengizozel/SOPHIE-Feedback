from fpdf import FPDF
import os
import sys
import json

path = os.path.abspath(os.path.join(os.path.dirname(__file__)))
sys.path.append(path)
import dial_gauge
import word_cloud
import turn_taking


def generate_pdf(transcript_file, gpt3_response, highlights, feedback_json):
    print(f"HIGHLIGHTS: {highlights}")

    feedback = json.loads(feedback_json)
    pdf = FPDF()


    # Transcript page
    pdf.add_page()
    pdf.set_font('arial', size=30, style='B')  # page dimensions are 210 x 297
    pdf.set_line_width(0.5)

    # Title
    pdf.cell(190, 20, txt="Transcript", ln=1, align='C', border=True)
    # Add an empty line
    pdf.ln(10)
    pdf.set_font('arial', size=12)
    # read a txt file and add it to a new cell
    with open(transcript_file, 'r') as f:
        index = 0
        for line in f.readlines():
            if index in highlights:
                pdf.set_font('arial', size=12, style='B')
                pdf.set_text_color(255, 0, 0)
                pdf.multi_cell(190, 5, txt=line, ln=1, align='L', border=False)
            else:
                pdf.set_font('arial', size=12)
                pdf.set_text_color(0, 0, 0)
                pdf.multi_cell(190, 5, txt=line, ln=1, align='L', border=False)
            index += 1
    # Create a cell that can take multiple lines
    pdf.set_font('arial', size=20, style='B')
    pdf.cell(190, 15, txt="Feedback for Clinician on MVP Protocol", ln=1, align='C', border=True)
    pdf.set_font('arial', size=12)
    pdf.multi_cell(190, 7, txt=gpt3_response, align='L', border=True)


    # Empower page
    empower = feedback["empower"]
    pdf.add_page()
    pdf.set_font('arial', size=30, style='B')

    # Title
    pdf.cell(190, 20, txt="Empower", ln=1, align='C', border=True)
    # Add an empty line
    pdf.ln(10)
    pdf.set_font('arial', size=12)

    pdf.image(dial_gauge.gauge(labels=['LOW', 'OK', 'GOOD'],
                         colors=['#ED1C24', '#FFCC00', '#007A00'],
                         arrow=3, title='Questions Asked'),
              x=12, y=42, w=72, h=54)
    pdf.image(dial_gauge.gauge(labels=['LOW', 'OK', 'GOOD'],
                         colors=['#ED1C24', '#FFCC00', '#007A00'],
                         arrow=3, title='Open Ended Questions'),
              x=12, y=100, w=72, h=54)
    
    pdf.image(turn_taking.get_tt_graph(), x=0, y=158, w=200, h=60)

    # Add bordered text box next to the first pdf image
    pdf.set_xy(100, 64) # 42 + 54/2 - 10/2
    pdf.set_font('arial', size=14)
    qa = empower["questions_asked"]
    pdf.multi_cell(90, 10, txt=f"You have asked {qa} questions.", ln=1, align='C', border=True)

    # Add bordered text box next to the second pdf image
    pdf.set_xy(100, 122) # 100 + 54/2 - 10/2
    oe = empower["open_ended"]
    pdf.multi_cell(90, 10, txt=f"{oe} of your questions were open-ended.", ln=1, align='C', border=True)


    # Be Explicit page
    explicit = feedback["explicit"]
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
    pdf.image(dial_gauge.gauge(labels=['GOOD', 'OK', 'BAD'],
                         colors=['#007A00', '#FFCC00', '#ED1C24'],
                         arrow=3, title='Hedge Words (%)'),
              x=12, y=118, w=72, h=54)
    pdf.image(dial_gauge.gauge(labels=['SLOW', 'OK', 'GOOD', 'FAST', "VERY FAST"],
                         colors=['#ED1C24', '#FFCC00', '#007A00', '#0063BF', '#ED1C24'],
                         arrow=3, title='Speaking Rate'),
              x=12, y=176, w=72, h=54)
    pdf.image(dial_gauge.gauge(labels=['OK', 'GOOD', 'OK', 'COMPLEX'],
                         colors=['#FFCC00', '#007A00', '#FFCC00', '#ED1C24'],
                         arrow=3, title='Reading Level'),
              x=12, y=232, w=72, h=54)

    # Add bordered text box next to the first pdf image
    pdf.set_xy(100, 64) # 42 + 72/2 - 10/2
    pdf.set_font('arial', size=14)
    hwc = explicit["hedge_words"]
    pdf.multi_cell(90, 10, txt=f"Your most used hedge words were: ", ln=1, align='C', border=True)
    # pdf.multi_cell(90, 10, txt=f"Your most used hedge words were: " + ", ".join(hwc), ln=1, align='C', border=True)
    # Add bordered text box next to the second pdf image
    pdf.set_xy(100, 140) # 118 + 54/2 - 10/2
    hw = explicit["hedge_words"]
    pdf.multi_cell(90, 10, txt=f"{hw[0]} of your {hw[1]} ({round(hw[0]/hw[1]*100)}%) words were hedge words.", ln=1, align='C', border=True)
    # Add bordered text box next to the third pdf image
    pdf.set_xy(100, 198) # 176 + 54/2 - 10/2
    sr = explicit["speaking_rate"]
    pdf.multi_cell(90, 10, txt=f"Your speech rate is {sr} words/minute.", ln=1, align='C', border=True)
    # Add bordered text box next to the fourth pdf image
    pdf.set_xy(100, 254) # 232 + 54/2 - 10/2
    rl = explicit["reading_level"]
    pdf.multi_cell(90, 10, txt=f"You spoke at a {rl}th grade reading level.", ln=1, align='C', border=True)


    # Empathize page
    empathize = feedback["empathize"]
    pdf.add_page()
    pdf.set_font('arial', size=30, style='B')

    # Title
    pdf.cell(190, 20, txt="Empathize", ln=1, align='C', border=True)
    # Add an empty line
    pdf.ln(10)
    pdf.set_font('arial', size=12)

    pdf.image(dial_gauge.gauge(labels=['BAD', 'OK', 'GOOD'],
                         colors=['#ED1C24', '#FFCC00', '#007A00'],
                         arrow=3, title='Peronsal Pronouns'),
              x=12, y=42, w=72, h=54)
    pdf.image(word_cloud.get_word_cloud(
        "Empathy Word Cloud"), x=12, y=100, w=72, h=72)
    pdf.image(dial_gauge.gauge(labels=['BAD', 'OK', 'GOOD'],
                         colors=['#ED1C24', '#FFCC00', '#007A00'],
                         arrow=3, title='Average Empathy'),
              x=12, y=176, w=72, h=54)
    
    # Add bordered text box next to the first pdf image
    pdf.set_xy(100, 64) # 42 + 54/2 - 10/2
    pdf.set_font('arial', size=14)
    pp = empathize["personal_pronouns"]
    pdf.multi_cell(90, 10, txt=f"{pp[0]} of your {pp[1]} ({round(pp[0]/pp[1]*100)}%) words were personal pronouns.", ln=1, align='C', border=True)
    # Add bordered text box next to the second pdf image
    pdf.set_xy(100, 122) # 100 + 72/2 - 10/2
    ewc = empathize["empathy_word_cloud"]
    pdf.multi_cell(90, 10, txt=f"Your most empathetic word was {ewc[0]}. Your least empathetic word was {ewc[1]}.", ln=1, align='C', border=True)
    # Add bordered text box next to the third pdf image
    pdf.set_xy(100, 198) # 176 + 54/2 - 10/2
    ae = empathize["average_empathy"]
    pdf.multi_cell(90, 10, txt=f"Your average empathy score was {ae}", ln=1, align='C', border=True)

    pdf.output("docs/feedback/sophie_feedback.pdf")


def main():
    generate_pdf()


if __name__ == "__main__":
    main()
