from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from app.config import Config
from flask_login import LoginManager

# Initialising the flask instance
app = Flask(__name__)

# Connecting with the PostgreSQL database-container from config.py
# app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:123@localhost:5432/flaskblog'
app.config.from_object(Config)

# Initialising the database instance 
db = SQLAlchemy(app)

login = LoginManager(app)
login.login_view = 'login'

from app import views, models