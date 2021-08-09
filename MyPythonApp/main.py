# integrating html with flask app
## using http verb get and post methods
from flask import Flask,redirect,url_for,render_template,request
app = Flask(__name__)
@app.route('/')
def welcome():
    return render_template('index.html')
@app.route('/success/<int:score>') # passing score as int (default string) called variable rules
def success(score):
    if score >=50:
        res = 'PASSED'
    else:
        res = 'FAILED'
    return render_template('result.html',result = res)
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
        science = float(request.form['science']) # the name of subject
        computer_science = float(request.form['computer science']) # the name of subject
        maths = float(request.form['maths']) # the name of subject
        c = float(request.form['c']) # the name of subject
        python = float(request.form['python']) # the name of subject
        total_score = (science + computer_science + maths + c + python)/5
    return redirect(url_for('success',score=total_score))
if __name__ == '__main__':
    app.run(debug = True)  