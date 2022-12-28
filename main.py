from flask import Flask, redirect, url_for, render_template
import helper

app = Flask(__name__)

@app.route('/')
def home():
    return redirect(url_for('modules'))

@app.route('/modules')
def modules():
    PATH = 'docs/modules/'
    return render_template('modules.html', module1=helper.get_text(PATH+'module1.txt'), module2=helper.get_text(PATH+'module2.txt'), module3=helper.get_text(PATH+'module3.txt'))

@app.route('/dialogue/<name>')
def dialogue(name):
    return render_template('dialogue.html', name=name, responses=helper.random_empathy('docs/dialogue/empathy.txt', 5), dialogue=helper.get_dialogue('docs/conversation-log/text.txt'), inference=helper.get_inference('docs/conversation-log/inference.txt'))


if __name__ == '__main__':
    app.run(debug=True)
