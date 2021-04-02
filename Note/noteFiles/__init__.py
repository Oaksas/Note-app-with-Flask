from  flask import Flask
from  noteFiles.forms import RegistrationForm 

app = Flask(__name__)
app.config ['SECRET_KEY'] = 'kkj32n4rkj32nrk24nda23413412er'
from noteFiles import routes