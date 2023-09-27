from flask import Flask, redirect, url_for, render_template, send_from_directory
from flask_caching import Cache
import helper.helper as helper
import helper.gpt3_feedback as gpt3_feedack
import pdf_generation.compute_metrics as compute_metrics
import pdf_generation.pdf_gen as pdf_gen

cache = Cache(config={'CACHE_TYPE': 'null'})

# import logging
# log = logging.getLogger('werkzeug')
# log.setLevel(logging.ERROR)

def create_pdf():
    pdf_gen.generate_pdf(processed_file, gpt3_response, module_type, three_es, compute_metrics.main())


app = Flask(__name__)
cache.init_app(app)


@app.route('/')
def home():
    return redirect(url_for('feedback'))


@app.route('/feedback')
def feedback():
    with app.app_context():
        cache.clear()

    global processed_file, inference_file, three_es, missed_opportunities, gpt3_response, gpt3_response_list, full_feedback

    if module_type != "Master":
        missed_opportunities = [x for x in missed_opportunities if x[2] == module_type]
        three_es = [x for x in three_es if x[0] == module_type]

    return render_template('feedback.html', module_type=module_type, three_es=three_es, missed_opportunities=missed_opportunities, gpt3_response_list=gpt3_response_list, full_feedback_func=full_feedback)


@app.route('/full-feedback')
def full_feedback():
    response = send_from_directory('docs/feedback', 'sophie_feedback.pdf')
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Pragma"] = "no-cache"
    response.headers["Expires"] = "0"
    return response


if __name__ == '__main__':
    global text_file, processed_file, inference_file, obligations_file, gpt3_response, gpt3_response_list
    global three_es, missed_opportunities
    global module_type

    # 1 == Empathize
    # 2 == be Explicit
    # 3 == Empower
    # 4 == Master
    module_type = "Empathize"
    
    # root_path = "docs/conversation-log-obligations/"
    root_path = "E:/SOPHIE/eta-py/io/sophie-gpt/doctor/conversation-log/"
    inference_file = root_path+"pragmatic.txt"
    obligations_file = root_path+"obligations.txt"
    text_file = root_path+"text.txt"
    processed_file = root_path+"text_processed.txt"

    helper.convert_text(text_file, processed_file)
    three_es, missed_opportunities = helper.get_inference(
        processed_file,
        inference_file,
        obligations_file)
    
    with open(processed_file, 'r') as f:
        processed_file_str = f.read()

    chars_replace = {"“": "\"", "”": "\"", "’": "'", "‘": "'"}

    gpt3_response = gpt3_feedack.run_gpt(processed_file_str, three_es, missed_opportunities, module_type)

    for char in chars_replace:
        gpt3_response = gpt3_response.replace(char, chars_replace[char])

    gpt3_response_list = gpt3_response.split("\n")

    create_pdf()
    
    app.run(debug=True, use_reloader=False)
