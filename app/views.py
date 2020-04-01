from app import app, db
from flask import render_template, request, redirect, url_for
from app.models import Blogpost
from datetime import datetime

@app.route('/')
def index():
    posts = Blogpost.query.order_by(Blogpost.date_posted.desc()).all()

    return render_template('public/index.html', posts=posts)

@app.route('/post/<int:post_id>')
def post(post_id):
    post = Blogpost.query.filter_by(id=post_id).one()
    
    return render_template('public/post.html', post=post)

@app.route('/about')
def about():
    return render_template('public/about.html')

@app.route('/add')
def add():
    return render_template('public/add.html')

@app.route('/addpost', methods=['POST'])
def addpost():
    title = request.form['title']
    author = request.form['author']
    content = request.form['content']

    #Adding the information to the database:
    post = Blogpost(title=title, author=author, content=content, date_posted=datetime.now())
    
    db.session.add(post)
    db.session.commit()

    return redirect(url_for('index'))