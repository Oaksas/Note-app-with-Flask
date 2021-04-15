from  flask import render_template, flash,redirect,url_for
from  noteFiles import app,db,bcrypt
from  noteFiles.forms import RegistrationForm ,LogInForm
from noteFiles.models import User,Notes


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
        hashedPassword=bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(username=form.username.data,email=form.email.data,password=hashedPassword)
        db.session.add(user)
        db.session.commit()
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
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password,form.password.data):

            flash(f'login unsuccessfull, try again','danger')

    return render_template('login.html',title="login",form=form)
