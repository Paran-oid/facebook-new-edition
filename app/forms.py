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

    def __init__(self, original_username, *args, **kwargs):
            super().__init__(*args, **kwargs)
            self.original_username=original_username

    def validate_username(self, username):
         if username.data!=self.original_username:
            user=db.session.scalar(sa.select(User).where(User.username==self.username.data))
            if user:
                raise ValidationError('Please use a different username')
        
class EmptyForm(FlaskForm):
    submit= SubmitField('Submit')

class PostForm(FlaskForm):

    post=TextAreaField('Say Something', validators=[DataRequired(), Length(min=1, max=140)])
    submit=SubmitField("Post")

class ForgotPassword(FlaskForm):
    email=EmailField('Email', validators=[DataRequired(), Email()])
    submit=SubmitField('Send Email')

class ResetPasswordForm(FlaskForm):
    password=PasswordField('Password', validators=[DataRequired()])
    password2=PasswordField('Repeat Password', validators=[DataRequired(),EqualTo(password)])
    submit=SubmitField('Reset Password')