from flask import Flask, redirect, url_for, render_template
import toy, helper

app = Flask(__name__)

@app.route('/')
def home():
    return redirect(url_for('modules'))

@app.route('/modules')
def modules():
    return render_template('modules.html', module1=helper.get_text('docs/module1.txt'), module2=helper.get_text('docs/module2.txt'), module3=helper.get_text('docs/module3.txt'))

@app.route('/dialogue/<name>')
def dialogue(name):
    return render_template('dialogue.html', name=name, responses=helper.random_empathy('docs/empathy.txt', 5), dialogue=helper.get_dialogue('docs/dialogue.txt'))


if __name__ == '__main__':
    app.run(debug=True)