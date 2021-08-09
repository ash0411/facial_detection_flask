# integrating html with flask app
## using http verb get and post methods
#Jinja2 template
'''
{%...%} any kind of statement if or for
{{    }} expression to print output
{#....#} this is for comments
'''
from flask import Flask,redirect,url_for,render_template,request
import json
app = Flask(__name__)
@app.route('/')
def welcome():
    return render_template('index.html')
@app.route('/success/<string:score>') # passing score as int (default string) called variable rules
def success(score):
    score = json.loads(score)
    return render_template('result.html',result = score)
@app.route('/fail/<int:score>')
def fail(score):
    fail_perc= 100 * (40-score)/40
    return render_template('result.html',result = fail_perc)
# result checker
@app.route('/results/<int:score>')
def result(score):
    res = 'success' if score > 40 else 'fail'
    return redirect(url_for(res,score = score)) # for redirecting to other pages
@app.route('/submit',methods = ['POST','GET']) # this will be my result checker html page
def submit():
    total_score = 0
    if request.method == 'POST':
        res = {}
        res['science'] = float(request.form['science']) # the name of subject
        res['computer_science'] = float(request.form['computer science']) # the name of subject
        res['maths'] = float(request.form['maths']) # the name of subject
        res['c'] = float(request.form['c']) # the name of subject
        res['python'] = float(request.form['python']) # the name of subject
        print(type(res))
        res['whole exam'] = (res['science'] + res['computer_science'] + res['maths'] + res['c'] + res['python'])/5
        inp = json.dumps(res)
    return redirect(url_for('success',score=inp))
if __name__ == '__main__':
    app.run(debug = True)  