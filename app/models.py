from app import db

class Blogpost(db.Model):
    __tablename__ = 'example'
    id = db.Column(db.Integer, primary_key=True)
    titel = db.Column(db.String(50))
    author = db.Column(db.String(20))
    date_posted = db.Column(db.DateTime)
    content = db.Column(db.Text)


# To create the database table Blogpost
# Run Python interactiv, then: 
# from app import db
# from app.models import Blogpost
# db.create_all()