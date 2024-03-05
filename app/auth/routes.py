import logging
from flask import Blueprint, render_template, flash, redirect, url_for, request
from flask_login import LoginManager, logout_user, login_user, current_user, login_required
from .forms import LoginForm, RegistrationForm
from app.models import User
from app import db  # Import the database instance

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

auth = Blueprint('auth', __name__)

@LoginManager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# Routes
@auth.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user and user.check_password(form.password.data):
            login_user(user)
            flash('You have been logged in!', 'success')
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('main.home'))
        else:
            flash('Login Unsuccessful. Please check username and password', 'danger')
    return render_template('login.html', title='Login', form=form)

@auth.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You have been logged out.', 'success')
    return redirect(url_for('main.home'))

@auth.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(username=form.username.data, email=form.email.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        login_user(user)
        flash('Your account has been created! You are now logged in.', 'success')
        return redirect(url_for('main.home'))
    return render_template('register.html', title='Register', form=form)

# Flask application error handlers
@auth.app_errorhandler(404)
def not_found_error(error):
    return render_template('404.html'), 404

@auth.app_errorhandler(500)
def internal_error(error):
    db.session.rollback()
    return render_template('500.html'), 500


@auth.route('/dashboard')
@login_required
def dashboard():
    return render_template('dashboard.html')