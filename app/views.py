from flask import render_template, request, redirect, url_for, flash
from app import app, db, bcrypt
from app.models import Blogpost, User
from app.forms import LoginForm, RegistrationForm
from datetime import datetime
from flask_login import current_user, login_user, logout_user, login_required


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


@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(username=form.username.data, email=form.email.data, password=hashed_password)
        
        # Adding an user to the database
        db.session.add(user)
        db.session.commit()
        
        flash('Congratulations, you are now a registered user!', 'bg-green-100 border-green-400')
        return redirect(url_for('login'))
    return render_template('public/signup.html', form=form)


@app.route('/login', methods=['GET', 'POST'])
def login():

    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = LoginForm()

    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            # If the inserd username and password match with the stored information inside the database, the user will be logged in
            login_user(user, remember=form.remember_me.data)
            # Redirecting from Login page to the page after the 'next' parameter else just redirect to index
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('index'))
        else:
            flash('Login Unsuccessful. Please check username and password', 'bg-red-100 border-red-400 text-red-700')
    return render_template('public/login.html', form=form)
   
@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))


