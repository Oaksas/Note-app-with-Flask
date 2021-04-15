from  flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import  Bcrypt
from flask_login import LoginManager
app = Flask(__name__)
app.config ['SECRET_KEY'] = 'kkj32n4rkj32nrk24nda23413412er'
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:1234@localhost/noteApp'

db =SQLAlchemy(app)
bcrypt=Bcrypt(app)
login_manager=LoginManager(app)
from noteFiles.models import User,Notes
from  noteFiles.forms import RegistrationForm 

from noteFiles import routes