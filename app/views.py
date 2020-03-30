from app import app, db
from flask import render_template, request, redirect, url_for
from app.models import Blogpost
from datetime import datetime


@app.route('/')
def index():
    return render_template('public/index.html')

@app.route('/about')
def about():
    return render_template('public/about.html')

@app.route('/add')
def add():
    return render_template('public/add.html')

@app.route('/addpost', methods=['POST'])
def addpost():
    titel = request.form['titel']
    author = request.form['author']
    content = request.form['content']

    #Adding the information to the database:
    post = Blogpost(titel=titel, author=author, content=content, date_posted=datetime.now())
    db.session.add(post)
    db.session.commit()

    return redirect(url_for('index'))