from flask import Flask,redirect,url_for
app = Flask(__name__)
@app.route('/')
def welcome():
    return 'Welcome to the practice session. lets practice hard. okay'
@app.route('/success/<int:score>/<number>') # passing score as int (default string) called variable rules
def success(score):
    return 'The practice session has passed with '+str(score)+"%"
@app.route('/fail/<int:score>/<number>')
def fail(score):
    fail_perc= 100 * (40-score)/40
    return " the practice session has failed by "+str(fail_perc) + '% ' 
# result checker
@app.route('/results/<int:score>/<number>')
def result(score):
    res = 'success' if score > 40 else 'fail'
    return redirect(url_for(res,score = score)) # for redirecting to other pages
if __name__ == '__main__':
    app.run(debug = True) 