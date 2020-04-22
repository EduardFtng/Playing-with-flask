from app import db, login
from datetime import datetime
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

class User(UserMixin, db.Model):
    __tablename__ = 'member'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)
    # Our post attribute has ralationship to the Blogpost class/model, also invisible column in the db session because it's just additional query running in the background
    # 'backref': it allows to get the user who created the post
    # 'lazy': for loading purpose
    posts = db.relationship('Blogpost', backref='author', lazy=True)

    def set_password(self, password):
      self.password_hash = generate_password_hash(password)

    def check_password(self, password):
      return check_password_hash(self.password_hash, password)

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

@login.user_loader
def load_user(id):
  return User.query.get(int(id))

# To create the database table Blogpost
# Run Python interactiv, then: 
# from app import db
# from app.models import Blogpost
# db.create_all()

# for psycopg2:
# postgresql-server-devel needed? + gcc