from  flask_wtf import FlaskForm
from  flask_wtf.file import FileField,FileAllowed
from wtforms import StringField,PasswordField,SubmitField,BooleanField,TextAreaField
from wtforms.validators import DataRequired,Length, Email,EqualTo, ValidationError
from noteFiles.models import User
from flask_login import current_user

class RegistrationForm(FlaskForm):
    username = StringField('Username',
     validators=[DataRequired(),Length(min=2, max=20)])
    email = StringField('Email', validators=[DataRequired(),Email()]) 
    password = PasswordField('password', validators=[DataRequired()])
    confirmPassword = PasswordField('Confirm Password',validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Sign Up')

    def validate_username(self,username):
      user = User.query.filter_by(username=username.data).first()
      if user:
        raise ValidationError('Username is taken...')

    def validate_email(self,email):
      user = User.query.filter_by(email=email.data).first()
      if user:
        raise ValidationError('Email already registered...')
 




class LogInForm(FlaskForm):

    email = StringField('Email', 
      validators=[DataRequired(),Email()]) 
    password = PasswordField('Password',validators=[DataRequired()])
    
    remember = BooleanField('Remember Me')
    login = SubmitField('Sign Up')
    
class UpdateAccountForm(FlaskForm):
    username = StringField('Username',
     validators=[DataRequired(),Length(min=2, max=20)])
    email = StringField('Email', validators=[DataRequired(),Email()]) 
    picture=FileField('Update profile picture', validators=[FileAllowed(['jpg','png'])])
    submit = SubmitField('Update ')


    def validate_username(self,username):
      if username.data != current_user.username:
        user = User.query.filter_by(username=username.data).first()
        if user:
          raise ValidationError('Username is taken...')

    def validate_email(self,email):
      if email.data != current_user.email:
        email = User.query.filter_by(email=email.data).first()
        if email:
          raise ValidationError('Email already registered...')
class PostForm(FlaskForm):
   title=StringField('Title',validators=[DataRequired()])
   content=TextAreaField('Content',validators=[DataRequired()])
   submit =SubmitField('Post')