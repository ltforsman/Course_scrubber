from flask import Flask, request, render_template, redirect,jsonify
import Scheduling as sch

app = Flask(__name__)

@app.route('/results/', methods = ['GET'])
def results():
    user_input = request.args.get("classes", None)
    # u = {}
    # u['user'] = user_input
    return f'<h1> {user_input} </h1>'


@app.route('/')
def home():
    return render_template('home-form.html')

@app.route('/', methods = ["POST"])
def home_to_result():
    text = request.form['text']
    url = '/results/?classes={}'.format(text)
    return redirect(url)

if __name__ == '__main__':
    app.run(threaded = True,port = 5000)
