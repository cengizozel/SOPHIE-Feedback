from flask import Flask, redirect, url_for, render_template
import toy, helper

# print(helper.get_dialogue('docs/dialogue.txt'))

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html', app_name="SOPHIE", responses=toy.random_string(10), dialogue=helper.get_dialogue('docs/dialogue.txt'))

@app.route('/admin')
def admin():
    return redirect(url_for('home'))

if __name__ == '__main__':
    app.run(debug=True)