import os
from flask_sqlalchemy import SQLAlchemy

class Config(object):
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'you-will-never-guess'

    SQLALCHEMY_DATABASE_URI = 'postgresql://postgres:123@localhost:5432/flaskblog'

    SQLALCHEMY_TRACK_MODIFICATIONS = False