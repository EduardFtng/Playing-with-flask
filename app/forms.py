from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import DataRequired, Length, ValidationError, Email, EqualTo
from app.models import User

# WTForms Module to create 'html' forms:
class LoginForm(FlaskForm):
    # first argument of *Field() - it is the label name of the field 
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Remember Me')
    submit = SubmitField('Login')

    # Checking if the username already exists in the database
    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user is None:
            raise ValidationError('Username does not exist.')


    #def validate_password(self, password):
    #    user = User.query.filter_by(password=password.data)
    #    if password is not password.data:
    #        raise ValidationError('Wrong Password')
class RegistrationForm(FlaskForm):
    # validators List: DataRequired() - the field can't be empty, Length() - sets the min and max for username
    username = StringField('Username', validators=[DataRequired(), Length(min=3, max=20)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    password2 = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Register')
    
    # Checking if the username already exists in the database
    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user is not None:
            raise ValidationError('Please use a different username.')

    # Checking if the email already exists in the database
    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user is not None:
            raise ValidationError('Please use a different email address.')