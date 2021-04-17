from  flask import render_template, flash,redirect,url_for, request,abort
from  noteFiles import app,db,bcrypt
from  noteFiles.forms import RegistrationForm ,LogInForm ,UpdateAccountForm,PostForm
from noteFiles.models import User,Notes
from flask_login import login_user, current_user, logout_user,login_required
from PIL import Image
import os
import secrets

@app.route('/')
@app.route('/home')


def home():
    page = request.args.get('page',1,type=int)
    posts =Notes.query.order_by(Notes.datePosted.desc()).paginate(page=page, per_page=2)
   
    return render_template('index.html',title="index", posts=posts)

@app.route('/about')
def about():
    return render_template('about.html',title="about")

 
def savePicture(formPicture):
    randomHex=secrets.token_hex(8)
    fName,fExt= os.path.splitext(formPicture.filename)
    pictureFn=randomHex +fExt
    picturePath=os.path.join(app.root_path,'static/images',pictureFn)
    outputSize= (125,125)
    i =Image.open(formPicture)
    i.thumbnail(outputSize)
    i.save(picturePath)
    return pictureFn

@app.route('/account', methods=['GET','POST'])
@login_required

def account():
    form=UpdateAccountForm()
    print(form.validate_on_submit())

    if form.validate_on_submit():
        if form.picture.data:
            pictureFile=savePicture(form.picture.data)
            current_user.image_file= pictureFile
            
        current_user.username= form.username.data
        current_user.email=form.email.data

        db.session.commit()
        flash(f'Your account has been updated!','success')
        return redirect(url_for('account'))
    elif request.method== 'GET':
        form.username.data= current_user.username
        form.email.data= current_user.email
    image_file=url_for('static', filename='images/'+ current_user.image_file)
    return render_template('account.html',title="Account", image_file=image_file, form=form)


@app.route('/register',methods=['GET','POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
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
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = LogInForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password,form.password.data):
            login_user(user,remember=form.remember.data)
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('home'))
            return redirect(url_for('home'))
        else:    
            flash(f'login unsuccessfull, try again','danger')

    return render_template('login.html',title="login",form=form)

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('home'))

@app.route('/post/new',methods=['GET','POST'])
@login_required
def newPost():
    form=PostForm()
    if form.validate_on_submit():
        post=Notes(title=form.title.data, content=form.content.data,author=current_user)
        db.session.add(post)
        db.session.commit()
        flash(f'Your post is created','Success')
        return redirect(url_for('home'))
    return render_template('createPost.html',title="New Post",form=form)


@app.route('/post/<int:post_id>')
def post(post_id):
    post=Notes.query.get_or_404(post_id)
    return render_template('post.html',title=post.title, post=post)

@app.route('/post/<int:post_id>/update',methods=['GET','POST'])
@login_required
def updatePost(post_id):
    post=Notes.query.get_or_404(post_id)
    if post.author != current_user:
        abort(403)
    else:
        form=PostForm()
        if form.validate_on_submit():
            post.title=form.title.data
            post.content=form.content.data
            db.session.commit()
            flash(f'Your post has been updated.....','success')
            return redirect(url_for('post',post_id=post.id))
        elif request.method=='GET':
            form.title.data =post.title
            form.content.data=post.content
        return render_template('createPost.html',title="Update Post", form=form)

   
@app.route('/post/<int:post_id>/delete',methods=['POST'])
@login_required
def deletePost(post_id):
    post=Notes.query.get_or_404(post_id)
    if post.author != current_user:
        abort(403)

    db.session.delete(post)
    db.session.commit()
    flash(f'Post deleted successfully. ')
    return redirect(url_for('home'))
