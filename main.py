from flask import Flask, redirect, url_for, render_template, send_from_directory
import helper.helper as helper
import helper.gpt3_feedback as gpt3_feedback
import pdf_generation.pdf_gen as pdf_gen

app = Flask(__name__)


@app.route('/')
def home():
    return redirect(url_for('feedback'))


@app.route('/modules')
def modules():
    PATH = 'docs/modules/'
    module1 = helper.get_text(PATH+'module1.txt')
    module2 = helper.get_text(PATH+'module2.txt')
    module3 = helper.get_text(PATH+'module3.txt')

    return render_template('modules.html', module1=module1, module2=module2, module3=module3)


@app.route('/dialogue/<name>')
def dialogue(name):
    global processed_file, inference_file
    responses = helper.random_empathy('docs/dialogue/empathy.txt', 5)
    dialogue = helper.get_dialogue(processed_file)
    inference = helper.get_inference(inference_file, processed_file)

    return render_template('dialogue.html', name=name, responses=responses, dialogue=dialogue, inference=inference)


@app.route('/feedback')
def feedback():
    global processed_file, inference_file, empower, explicit, empathy, highlights, missed_opportunities, gpt3_response
    return render_template('feedback.html', empower=empower, explicit=explicit, empathy=empathy, missed_opportunities=missed_opportunities, gpt3_response=gpt3_response)


@app.route('/full-feedback')
def full_feedback():
    global processed_file, gpt3_response
    pdf_gen.generate_pdf(processed_file, gpt3_response, highlights, helper.create_json())
    return send_from_directory('docs/feedback', 'sophie_feedback.pdf')


if __name__ == '__main__':
    global text_file, processed_file, inference_file, gpt3_response
    global empower, explicit, empathy, highlights, missed_opportunities
    
    inference_file = "docs/conversation-log/inference.txt"
    text_file = "docs/conversation-log/text.txt"
    processed_file = "docs/conversation-log/text_processed.txt"
    helper.convert_text(text_file, processed_file)
    empower, explicit, empathy, highlights, missed_opportunities = helper.get_inference(inference_file, processed_file)
    
    # gpt3_response = gpt3_feedback.get_feedback('docs/conversation-log/text.txt')
    gpt3_response = "Well done, clinician! You used the 3E skillset to communicate effectively with your patient. You successfully empowered them by listening and asking first, and then being explicit with the facts. You empathized with your patient by acknowledging the difficulty of the conversation and validating their feelings. Great job! To take your communication skills even further, you could try to anticipate more of the patient's needs and concerns, and provide further emotional support."
    app.run(debug=True)
