from fpdf import FPDF
import os
import sys
import json

path = os.path.abspath(os.path.join(os.path.dirname(__file__)))
sys.path.append(path)
import dial_gauge
import word_cloud
import turn_taking
import compute_metrics


def generate_pdf(transcript_file, gpt3_response, module_type, three_es, feedback_json):
    tips_path = "docs/tips/"

    feedback = json.loads(feedback_json)
    pdf = FPDF()

    # Transcript page
    pdf.add_page()
    pdf.set_font('arial', size=30, style='B')  # page dimensions are 210 x 297
    pdf.set_line_width(0.5)

    # Create a cell that can take multiple lines
    pdf.set_font('arial', size=20, style='B')
    pdf.cell(190, 20, txt="Feedback for Clinician on MVP Protocol", ln=1, align='C', border=True)
    pdf.ln(10)
    pdf.set_font('arial', size=12)
    pdf.multi_cell(190, 7, txt=gpt3_response, align='L')
    pdf.ln(10)

    # Title
    pdf.set_font('arial', size=20, style='B')
    pdf.cell(190, 20, txt="Transcript", ln=1, align='C', border=True)
    # Add an empty line
    pdf.ln(10)
    pdf.set_font('arial', size=12)
    # read a txt file and add it to a new cell
    with open(transcript_file, 'r') as f:
        index = 0
        for line in f.readlines():
            txt=line
            if index in [x[1] for x in three_es if x[0] == "Empowering"]:
                pdf.set_text_color(0, 200, 0)
                txt = f"{line.rstrip()}    >> " + "Empowering\n"
            elif index in [x[1] for x in three_es if x[0] == "Explicit"]:
                pdf.set_text_color(0, 200, 0)
                txt = f"{line.rstrip()}    >> " + "Explicit\n"
            elif index in [x[1] for x in three_es if x[0] == "Empathy"]:
                pdf.set_text_color(0, 200, 0)
                txt = f"{line.rstrip()}    >> " + "Empathy\n"
            else:
                pdf.set_text_color(0, 0, 0)
            pdf.set_font('arial', size=12)
            pdf.multi_cell(190, 5, txt=txt, ln=1, align='L', border=False)
            index += 1
    pdf.set_text_color(0, 0, 0)

    bad_color = '#207068'
    good_color = '#9fefe7'

    if module_type == "Empowering" or module_type == "Master":
        # Empower page
        empower = feedback["empower"]
        pdf.add_page()
        pdf.set_font('arial', size=30, style='B')

        # Title
        pdf.cell(190, 20, txt="Empower", ln=1, align='C', border=True)
        # Add an empty line
        pdf.ln(10)
        pdf.set_font('arial', size=12)

        qa = empower["questions_asked"]
        qa_arrow = compute_metrics.get_questions_asked_result(qa)
        pdf.image(dial_gauge.gauge(labels=['GOOD', 'GREAT'],
                            colors=[bad_color, good_color],
                            arrow=qa_arrow, title='Questions Asked'),
                x=12, y=42, w=72, h=54)

        oe = empower["open_ended"]
        oe_arrow = compute_metrics.get_open_ended_result(oe)
        pdf.image(dial_gauge.gauge(labels=['GOOD', 'GREAT'],
                            colors=[bad_color, good_color],
                            arrow=oe_arrow, title='Open Ended Questions'),
                x=12, y=100, w=72, h=54)
        
        tt = empower["turn_taking"]
        pdf.image(turn_taking.get_tt_graph(tt), x=0, y=158, w=200, h=60)


        # qs = empower["questions"]
        # questions_feedback = f"You have asked {qa} questions:\n"
        # for q in qs:
            # questions_feedback += q.split(":")[1]
        # Add bordered text box next to the first pdf image
        pdf.set_font('arial', size=14)
        questions_text = ""
        if qa == 0:
            pdf.set_xy(100, 51)
            questions_text = "You did not ask any questions. Asking questions is important to empower your patient."
        else:
            pdf.set_xy(100, 64)
            questions_text = f"You have asked {qa} questions."
        pdf.multi_cell(90, 10, txt=questions_text, ln=1, align='C', border=True)

        # Add bordered text box next to the second pdf image
        
        open_ended_text = ""
        if oe == 0:
             pdf.set_xy(100, 104)
             open_ended_text = "You did not ask any open-ended questions. Open-ended questions are important because it empowers your patient to steer the conversation."
        else:
            pdf.set_xy(100, 122) # 100 + 54/2 - 10/2
            open_ended_text = f"{oe} of your questions were open-ended."
        pdf.multi_cell(90, 10, txt=open_ended_text, ln=1, align='C', border=True)
        
        pdf.add_page()
        pdf.set_font('arial', size=30, style='B')

        # Title
        pdf.cell(190, 20, txt="Empower - Tips and Examples", ln=1, align='C', border=True)
        # Add an empty line
        pdf.ln(10)

        with open(tips_path + "empower.txt", 'r') as f:
            empower_tips = f.readlines()
            for tip in empower_tips:
                tip = '> ' + tip
                pdf.set_font('arial', size=16)
                pdf.multi_cell(190, 7, txt=tip, align='L')


    if module_type == "Explicit" or module_type == "Master":
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
        # hwc = explicit["hedge_word_cloud"]
        # pdf.image(word_cloud.get_word_cloud(
        #     "Hedge Word Cloud", hwc), x=12, y=42, w=72, h=72)

        top_img_y = 45
        img_dif = 70

        top_text_y = 42
        text_dif = 79

        hw = explicit["hedge_words"]
        hw_percent = round(hw[0]/hw[1]*100)
        hw_arrow = compute_metrics.get_hedge_result(hw_percent)
        pdf.image(dial_gauge.gauge(labels=['GOOD', 'HIGH'],
                            colors=[good_color, bad_color],
                            arrow=hw_arrow, title='Hedge Word Usage'),
                x=12, y=top_img_y, w=72, h=54)
    
        sr = explicit["speaking_rate"]
        sr_arrow = compute_metrics.get_speaking_rate_result(sr)
        pdf.image(dial_gauge.gauge(labels=['GOOD', "FAST"],
                            colors=[good_color, bad_color],
                            arrow=sr_arrow, title='Speaking Rate'),
                x=12, y=top_img_y+img_dif, w=72, h=54)
    
        rl, rl_text = explicit["reading_level"]
        rl_arrow = compute_metrics.get_reading_level_result(rl)
        pdf.image(dial_gauge.gauge(labels=['GOOD', 'COMPLEX'],
                            colors=[good_color, bad_color],
                            arrow=rl_arrow, title='Reading Level'),
                x=12, y=top_img_y+2*img_dif, w=72, h=54)

        # Add bordered text box next to the first pdf image
        pdf.set_xy(100, 64) # 42 + 72/2 - 10/2
        pdf.set_font('arial', size=14)
        
        # get the most used hedge words from hwc
        # most_used_hedge_words = []
        # for word in hwc:
        #     if word not in most_used_hedge_words:
        #         most_used_hedge_words.append(word)
        #     if len(most_used_hedge_words) == 3:
        #         break
        # muhw = ", ".join(most_used_hedge_words)

        # pdf.multi_cell(90, 10, txt=f"Your most used hedge words were: {muhw}", ln=1, align='C', border=True)
        # Add bordered text box next to the second pdf image
        pdf.set_xy(100, top_text_y)
        #hedge_text = f"{hw[0]} of your {hw[1]} ({hw_percent}%) words\nwere hedge words."
        hedge_text = "Hedge words are used to soften the\nimpact of a statement and are often fine to use in a clinical setting. However, using too many of these words can make a response sound indecisive or unclear. Examples of hedge words include: 'kind of,' 'sort of,' 'maybe,' or 'probably.' Use your judgement to determine if a hedge word is necessary."
        pdf.multi_cell(90, 7, txt=hedge_text, ln=1, align='C', border=True)
        # Add bordered text box next to the third pdf image
        pdf.set_xy(100, top_text_y+text_dif+10)
        pdf.multi_cell(90, 10, txt=f"Your speech rate is {sr} words/second.", ln=1, align='C', border=True)
        # Add bordered text box next to the fourth pdf image
        pdf.set_xy(100, top_text_y+2*text_dif)
        pdf.multi_cell(90, 10, txt=f"You spoke at a {rl_text} reading level.", ln=1, align='C', border=True)
        
        pdf.add_page()
        pdf.set_font('arial', size=30, style='B')

        # Title
        pdf.cell(190, 20, txt="Be Explicit - Tips and Examples", ln=1, align='C', border=True)
        # Add an empty line
        pdf.ln(10)

        with open(tips_path + "explicit.txt", 'r') as f:
            empower_tips = f.readlines()
            for tip in empower_tips:
                tip = '> ' + tip
                pdf.set_font('arial', size=16)
                pdf.multi_cell(190, 7, txt=tip, align='L')


    if module_type == "Empathy" or module_type == "Master":
        # Empathize page
        # empathize = feedback["empathize"]
        # pdf.add_page()
        # pdf.set_font('arial', size=30, style='B')

        # # Title
        # pdf.cell(190, 20, txt="Empathize", ln=1, align='C', border=True)
        # # Add an empty line
        # pdf.ln(10)
        # pdf.set_font('arial', size=12)
        

        pdf.add_page()
        pdf.set_font('arial', size=30, style='B')

        # Title
        pdf.cell(190, 20, txt="Empathy - Tips and Examples", ln=1, align='C', border=True)
        # Add an empty line
        pdf.ln(10)

        with open(tips_path + "empathize.txt", 'r') as f:
            empower_tips = f.readlines()
            for tip in empower_tips:
                tip = '> ' + tip
                pdf.set_font('arial', size=16)
                pdf.multi_cell(190, 7, txt=tip, align='L')

    pdf.output("docs/feedback/sophie_feedback.pdf")


def main():
    generate_pdf()


if __name__ == "__main__":
    main()
