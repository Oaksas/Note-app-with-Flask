from  flask import render_template, flash,redirect,url_for
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
        print('validated')
        flash(f'Account created successfully for {form.username.data}!', 'success')
        return redirect(url_for('home'))
    else:
        print(form.errors)
    return render_template('register.html',title="register",form=form)
    

@app.route('/login',methods=['GET','POST'])
def login():
    form = LogInForm()
    if form.validate_on_submit():
        if form.email.data == 'aman.getnet2@gmail.com' and form.password.data =='password':
            flash(f'{form.email.data} logged in successfully','success')
            return redirect(url_for('home'))
        else:
            flash(f'login unsuccessfull, try again','danger')

    return render_template('login.html',title="login",form=form)
