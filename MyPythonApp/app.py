from flask import Flask
app = Flask(__name__)
@app.route('/')
def welcome():
    return 'Welcome to the practice session. lets practice hard. okay
@app.route('/members')
def members():
    return 'Welcome to the practice session.'
if __name__ == '__main__':
    app.run(debug = True) 