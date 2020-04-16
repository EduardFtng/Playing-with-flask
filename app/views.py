from app import app, db
from flask import render_template, request, redirect, url_for, flash
from app.models import Blogpost, User
from app.forms import LoginForm, RegistrationForm
from datetime import datetime
from flask_login import current_user, login_user, logout_user, login_required
from werkzeug.urls import url_parse


@app.route('/')
def index():
    # Added Blogposts Title are shown on the index page descending(latest-first)
    posts = Blogpost.query.order_by(Blogpost.date_posted.desc()).all()

    return render_template('public/index.html', posts=posts)

@app.route('/post/<int:post_id>')
def post(post_id):
    # The full Blogpost with given post_id is selected and displayed on the site
    post = Blogpost.query.filter_by(id=post_id).one()
    
    return render_template('public/post.html', post=post)

@app.route('/about')
def about():
    return render_template('public/about.html')

@app.route('/add')
@login_required
def add():
    return render_template('public/add.html')

@app.route('/addpost', methods=['POST'])
def addpost():
    title = request.form['title']
    author = current_user.get_id() 
    #author = request.form['author']
    content = request.form['content']

    #Adding the information to the database:
    post = Blogpost(title=title, content=content, date_posted=datetime.now())
    
    db.session.add(post)
    db.session.commit()

    return redirect(url_for('index'))

@app.route('/login', methods=['GET', 'POST'])
def login():

    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = LoginForm()

    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            flash('Invalid username or password')
            return redirect(url_for('login'))

        login_user(user, remember=form.remember_me.data)
        return redirect(url_for('index'))

        next_page = request.args.get('next')
        if not next_page or url_parse(next_page).netloc != '':
            next_page = url_for('index')
        return redirect(next_page)

    return render_template('public/login.html', form=form)

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))


@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(username=form.username.data, email=form.email.data)
        user.set_password(form.password.data)
        
        db.session.add(user)
        db.session.commit()
        
        flash('Congratulations, you are now a registered user!')
        return redirect(url_for('login'))
    return render_template('public/signup.html', form=form)