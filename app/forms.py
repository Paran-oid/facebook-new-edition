from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, EmailField, SubmitField, BooleanField, TextAreaField
from wtforms.validators import DataRequired, ValidationError, Email, EqualTo, Length
from app import db 
from app.models import User
import sqlalchemy as sa

class Form(FlaskForm):
    username=StringField("Enter username", validators=[DataRequired()])
    password=PasswordField("Enter password", validators=[DataRequired()])
    remember_me=BooleanField('Remember me')
    submit=SubmitField("submit")

class RegistrationForm(FlaskForm):
    username=StringField('Username', validators=[DataRequired()])
    email=StringField('Email', validators=[DataRequired(), Email()])
    password=PasswordField('Password', validators=[DataRequired()])
    password2=PasswordField('Repeat password', validators=[DataRequired(), EqualTo('password')])
    submit=SubmitField('Register')

    def validate_username(self, username):
        user=db.session.scalar(sa.select(User).where(User.username == username.data))
        if user:
            raise ValidationError('Please use a different username')
    
    def validate_email(self, email):
        user=db.session.scalar(sa.select(User).where(User.email == email.data))
        if user:
            raise ValidationError('Please use a different email')
        
class EditProfileForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    about_me = TextAreaField('About me', validators=[Length(min=0, max=140)])
    submit = SubmitField('Submit')