# app/__init__.py
import os

from flask import Flask
from flask_login import LoginManager
from flask_mail import Mail
from flask_wtf.csrf import CSRFProtect
from flask_sqlalchemy import SQLAlchemy
from flask_limiter import Limiter # Import Flask-Limiter
from flask_limiter.util import get_remote_address # For IP address based limiting
from config import DevelopmentConfig, ProductionConfig, TestingConfig

# from .database import init_db # Remove get_db_connection - REMOVED TO BREAK CIRCULAR IMPORT

# Create extension instances
login_manager = LoginManager()
mail = Mail()
csrf = CSRFProtect()
db = SQLAlchemy()
limiter = Limiter( # Initialize Limiter
    key_func=get_remote_address,
    default_limits=["200 per day", "50 per hour"] # Default limits for all routes
)


def create_app():
    app = Flask(__name__)

    # Determine configuration class based on FLASK_ENV environment variable
    config_class = {
        "development": DevelopmentConfig,
        "testing": TestingConfig,
        "production": ProductionConfig,
    }.get(os.environ.get("FLASK_ENV"), DevelopmentConfig)

    app.config.from_object(config_class)
    app.config['SQLALCHEMY_DATABASE_URI'] = app.config['DATABASE_URI'] # Add SQLAlchemy database URI
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False # Disable modification tracking

    # Set secure session cookie for production
    if not app.config.get('DEBUG', False) and not app.config.get('TESTING', False): # Ensure not debug and not testing
        app.config['SESSION_COOKIE_SECURE'] = True

    # Initialize extensions with the app object
    login_manager.init_app(app)
    mail.init_app(app)
    csrf.init_app(app)
    db.init_app(app)
    limiter.init_app(app) # Initialize Limiter with the app

    # Setup for Flask-Login
    login_manager.login_view = (
        "auth.login"  # Specify the view function that handles logins
    )
    login_manager.login_message_category = "info"

    # User loader function for Flask-Login
    from .models import User # Import User model

    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id)) # Use SQLAlchemy to load user

    # Register blueprints
    from .auth.routes import auth as auth_blueprint

    app.register_blueprint(auth_blueprint, url_prefix="/auth")

    from .main.routes import main as main_blueprint

    app.register_blueprint(main_blueprint)
    # init_db() # Initialize the database - No longer needed with SQLAlchemy

    return app
