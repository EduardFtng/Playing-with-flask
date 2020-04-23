from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from app.config import Config
from flask_login import LoginManager

# Initialising the flask instance
app = Flask(__name__)

# Connecting with the PostgreSQL database-container from config.py
# app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:123@localhost:5432/flaskblog'
app.config.from_object(Config)

# Initialising the database instance 
db = SQLAlchemy(app)

bcrypt = Bcrypt(app)

login_manager = LoginManager(app)
login_manager.login_view = 'login'
# this line is for bootstrap class(css):
#login_manager.login_message_category = 'info'

from app import views