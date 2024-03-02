# app/__init__.py
"""
    The `create_app` function initializes a Flask application with various extensions and configurations
    based on the environment.
    
    :param user_id: The `user_id` parameter in the `load_user` function is the unique identifier for a
    user in the system. It is typically used to load a specific user from the database based on their ID
    when they are authenticated and accessing the application
    :return: The `create_app()` function returns a Flask application instance that is configured based
    on the environment specified in the `FLASK_ENV` environment variable. The function initializes
    various extensions such as SQLAlchemy for database operations, Flask-Migrate for database
    migrations, Flask-Login for user authentication, and Flask-Mail for email functionality. It also
    sets up the configuration for the mail server and registers blueprints for different parts of
"""
import os
import secrets

from flask import Flask
from flask_login import LoginManager
from flask_mail import Mail
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy

from .config import Config, DevelopmentConfig, ProductionConfig, TestingConfig

# Create extension instances without initializing them with an app object
db = SQLAlchemy()
migrate = Migrate()
login_manager = LoginManager()
mail = Mail()

# Setup LoginManager
login_manager.login_view = "auth.login"  # Specify the view function that handles logins
login_manager.login_message_category = "info"


def load_user(user_id):
    from app.models import User  # Import here to avoid circular imports

    return User.query.get(int(user_id))


def create_app():
    app = Flask(__name__)

    if os.environ.get("FLASK_ENV") == "development":
        config_class = DevelopmentConfig
    elif os.environ.get("FLASK_ENV") == "testing":
        config_class = TestingConfig

    else:
        config_class = ProductionConfig

    app.config.from_object(config_class)

    # Initialize extensions with the app object
    db.init_app(app)
    migrate.init_app(app, db)
    login_manager.init_app(app)
    mail.init_app(app)

    login_manager.user_loader(load_user)

    # Configure mail settings within the application factory
    app.config["MAIL_SERVER"] = "smtp.gmail.com"
    app.config["MAIL_PORT"] = 587
    app.config["MAIL_USE_TLS"] = True
    app.config["MAIL_USERNAME"] = "code@kvnbbg-creations.io"
    # Securely generate a random password for the mail account
    app.config["MAIL_PASSWORD"] = secrets.token_urlsafe(16)

    # Import and register blueprints
    from app.main.routes import main as main_blueprint

    app.register_blueprint(main_blueprint)

    from app.auth.routes import auth as auth_blueprint  # Corrected import path

    app.register_blueprint(auth_blueprint, url_prefix="/auth")

    # TODO: Initialize other extensions as needed

    return app
