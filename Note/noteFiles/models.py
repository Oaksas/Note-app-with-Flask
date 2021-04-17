from noteFiles import app,db,login_manager
from datetime import datetime
from flask_login import UserMixin

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))
class User(db.Model, UserMixin):
    id =db.Column(db.Integer,primary_key= True)
    username=db.Column(db.String(20), unique=True, nullable=False)
    email=db.Column(db.String(120), unique=True, nullable=False)
    image_file = db.Column(db.String(200), nullable=False, default='profile.png')
    password = db.Column(db.String(60), nullable=False)
    post = db.relationship('Notes',backref='author', lazy= True )
    
    def __repr__(self):
        return f"User('{self.username}','{self.email}','{self.image_file}')"

class Notes(db.Model):
    id =db.Column(db.Integer,primary_key=True)
    title=db.Column(db.String(20), nullable=False)
    content=db.Column(db.Text, nullable=False)
    datePosted=db.Column(db.DateTime,nullable=False, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
        
    def __repr__(self):
        return f"Notes('{self.title}','{self.content}','{self.datePosted}')"




    




