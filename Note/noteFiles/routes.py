from  flask import render_template, flash,redirect
from  noteFiles import app
from  noteFiles.forms import RegistrationForm ,LogInForm


@app.route('/')
@app.route('/home')

def home():
    return render_template('index.html',title="index")

@app.route('/about')
def about():
    return render_template('about.html',title="about")

@app.route('/account')
def account():
    return render_template('account.html',title="account")


@app.route('/register',methods=['GET','POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        flash(f'Account created successfully for {form.username.data}!', 'success')
        return redirect(url_for('home'))
    return render_template('register.html',title="register",form=form)
    

@app.route('/login')
def login():
    form = LogInForm()
    return render_template('login.html',title="login",form=form)
