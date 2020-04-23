from app import db, login_manager
from datetime import datetime
from flask_login import UserMixin

# Handling the current logged in User using the 'user_id'
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

class User(db.Model, UserMixin):
    __tablename__ = 'member'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(60), nullable=False)
    # Our post attribute has ralationship to the Blogpost class/model, also invisible column in the db session because it's just additional query running in the background
    # 'backref': it allows to get the user who created the post
    # 'lazy': for loading purpose
    posts = db.relationship('Blogpost', backref='author', lazy=True)

    # Magic Method to define how User Class will be printed out
    def __repr__(self):
      return f"User('{self.username}', '{self.email}')"

class Blogpost(db.Model):
    __tablename__ = 'blogpost'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    date_posted = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    content = db.Column(db.Text, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('member.id'), nullable=False)

    def __repr__(self):
      return f"Blogpost('{self.title}', '{self.date_posted}')"

# To create the database table Blogpost
# Run Python interactiv, then: 
# from app import db
# from app.models import Blogpost
# db.create_all()

# for psycopg2:
# postgresql-server-devel needed? + gcc