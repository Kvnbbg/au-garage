# auth/routes.py
from flask import Blueprint, render_template, flash, redirect, url_for
from .forms import LoginForm
from flask_login import logout_user
from werkzeug.security import check_password_hash
from flask_login import login_user
from app.models import User
from app import db  # Import the database instance

auth = Blueprint('auth', __name__)


@auth.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user and check_password_hash(user.password, form.password.data):
            login_user(user)
            flash('You have been logged in!', 'success')
            return redirect(url_for('main.home'))
        else:
            flash('Login Unsuccessful. Please check username and password', 'danger')
    return render_template('login.html', title='Login', form=form)


@auth.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('main.home'))


@auth.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(username=form.username.data, password=form.password.data)
        db.session.add(user)
        db.session.commit()
        login_user(user)
        flash('Your account has been created! You are now logged in.', 'success')
        return redirect(url_for('main.home'))
    return render_template('register.html', title='Register', form=form)

