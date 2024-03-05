import logging
from flask import Blueprint, render_template, flash, redirect, url_for
from flask_login import logout_user, login_user, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from .forms import LoginForm, RegistrationForm
from app.models import User
from app import db  # Import the database instance
from sqlalchemy.exc import SQLAlchemyError

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

auth = Blueprint('auth', __name__)

@auth.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))
    form = LoginForm()
    if form.validate_on_submit():
        try:
            user = User.query.filter_by(username=form.username.data).first()
            if user and check_password_hash(user.password, form.password.data):
                login_user(user)
                flash('You have been logged in!', 'success')
                return redirect(url_for('main.home'))
            else:
                flash('Login Unsuccessful. Please check username and password', 'danger')
        except SQLAlchemyError as e:
            logger.error(f'Database error during login for user {form.username.data}: {e}', exc_info=True)
            flash('An error occurred while accessing the database. Please try again.', 'danger')
        except Exception as e:
            logger.error(f'Unexpected error during login: {e}', exc_info=True)
            flash('An unexpected error occurred. Please try again later.', 'danger')
    return render_template('login.html', title='Login', form=form)

@auth.route('/logout')
def logout():
    try:
        logout_user()
        flash('You have been logged out.', 'success')
        return redirect(url_for('main.home'))
    except Exception as e:
        logger.error(f'Error during logout: {e}', exc_info=True)
        flash('An error occurred during logout. Please try again later.', 'danger')

@auth.route('/register', methods=['GET', 'POST'])
def register():
    """
    Register a new user.

    This function handles the registration process for a new user. It checks if the user is already logged in,
    validates the registration form, creates a new user in the database, logs in the user, and redirects to the home page.

    Returns:
        If the registration is successful, it redirects to the home page.
        If there is an error during registration, it displays an error message and renders the registration form.

    Raises:
        SQLAlchemyError: If there is an error with the database during registration.
        Exception: If there is an unexpected error during registration.
    """
    if current_user.is_authenticated: # Redirect to home if user is already logged in
        return redirect(url_for('main.home'))
    form = RegistrationForm()
    if form.validate_on_submit():
        try:
            hashed_password = generate_password_hash(form.password.data)
            user = User(username=form.username.data, password=hashed_password)
            db.session.add(user)
            db.session.commit()
            login_user(user)
            flash('Your account has been created! You are now logged in.', 'success')
            return redirect(url_for('main.home'))
        except SQLAlchemyError as e:
            db.session.rollback()
            logger.error(f'Database error during registration for user {form.username.data}: {e}', exc_info=True)
            flash('An error occurred while creating your account. Please try again.', 'danger')
        except Exception as e:
            logger.error(f'Unexpected error during registration: {e}', exc_info=True)
            flash('An unexpected error occurred. Please try again later.', 'danger')
    return render_template('register.html', title='Register', form=form)

# Flask application error handlers
@auth.app_errorhandler(404)
def not_found_error(error):
    return render_template('404.html'), 404

@auth.app_errorhandler(500)
def internal_error(error):
    db.session.rollback()
    return render_template('500.html'), 500
