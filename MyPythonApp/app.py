from flask import Flask,redirect,url_for
app = Flask(__name__)
@app.route('/')
def welcome():
    return 'Welcome to the practice session. lets practice hard. okay'
@app.route('/success/<int:score>/<number>') # passing score as int (default string) called variable rules
def success(score,number):
    return 'The practice session has passed with '+str(score)+"%"
@app.route('/fail/<int:score>/<number>')
def fail(score,number):
    fail_perc= 100 * (40-score)/40
    return " the practice session has failed by "+str(fail_perc) + '% ' + number
# result checker
@app.route('/results/<int:score>/<number>')
def result(score,number):
    number=str(5)
    res = 'success' if score > 40 else 'fail'
    return redirect(url_for(res,score = score,number = number)) # for redirecting to other pages
if __name__ == '__main__':
    app.run(debug = True) 