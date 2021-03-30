from  flask import render_template
from noteFiles import app
@app.route('/')
@app.route('/home')

def home():
    return render_template('index.html',title="index")

@app.route('/')
@app.route('/about')

def about():
    return render_template('about.html',title="about")

@app.route('/')
@app.route('/account')

def account():
    return render_template('account.html',title="account")

