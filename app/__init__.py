# app/__init__.py
import os

from flask import Flask
from flask_login import LoginManager
from flask_mail import Mail
from flask_wtf.csrf import CSRFProtect
from config import DevelopmentConfig, ProductionConfig, TestingConfig

from .database import get_db_connection, init_db

__all__ = ["get_db_connection"]

# Create extension instances
login_manager = LoginManager()
mail = Mail()
csrf = CSRFProtect()  # CSRF protection


def create_app():
    app = Flask(__name__)

    # Determine configuration class based on FLASK_ENV environment variable
    config_class = {
        "development": DevelopmentConfig,
        "testing": TestingConfig,
        "production": ProductionConfig,
    }.get(os.environ.get("FLASK_ENV"), DevelopmentConfig)

    app.config.from_object(config_class)

    # Initialize extensions with the app object
    login_manager.init_app(app)
    mail.init_app(app)
    csrf.init_app(app)  # Initialize CSRF protection

    # Setup for Flask-Login
    login_manager.login_view = (
        "auth.login"  # Specify the view function that handles logins
    )
    login_manager.login_message_category = "info"

    # User loader function for Flask-Login
    from config import Config

    # Adjusting DATABASE_URI extraction to match your setup if needed
    DATABASE_URI = Config.DATABASE_URI.split("///")[-1]
    import sqlite3

    @login_manager.user_loader
    def load_user(user_id):
        conn = sqlite3.connect(DATABASE_URI)  # Use your actual database name
        cur = conn.cursor()
        cur.execute("SELECT * FROM users WHERE id=?", (user_id,))
        user = cur.fetchone()
        conn.close()
        return user

    # Register blueprints
    from .auth.routes import auth as auth_blueprint

    app.register_blueprint(auth_blueprint, url_prefix="/auth")

    from .main.routes import main as main_blueprint

    app.register_blueprint(main_blueprint)
    init_db()  # Initialize the database

    return app
