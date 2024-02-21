from app import app, db
import sqlalchemy as sa
from app.models import User, Post
from flask import render_template, flash, redirect, url_for, request
from .forms import Form, RegistrationForm
from flask_login import current_user, login_user, logout_user
from urllib.parse import urlsplit

@app.route("/")
def index():
    form=Form()
    posts=Post.query.all()
    return render_template("index.html", posts=posts)

@app.route("/login", methods=['POST','GET'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form=Form()
    if form.validate_on_submit():
        user = db.session.scalar(sa.select(User).where(User.username == form.username.data))
        if not user or not user.check_password(form.password.data):
            flash("Invalid username or password")
            return redirect(url_for('login'))
        login_user(user, remember= form.remember_me.data)
        next_page = request.args.get('next')
        if not next_page or (urlsplit(next_page)).netloc != '':
            next_page = url_for('index')
        return redirect(next_page)
    return render_template("login.html",title='Sign In', form=form)

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))

@app.route('/register', methods=['POST','GET'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form=RegistrationForm()
    if form.validate_on_submit():
        user=User(username=form.username.data, email= form.email.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Congratulations, You are now Registered!')
        return redirect(url_for('login'))
    return render_template('register.html', form=form)