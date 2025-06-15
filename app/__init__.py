# app/__init__.py
import os

from flask import Flask
from flask_login import LoginManager
from flask_mail import Mail
from flask_wtf.csrf import CSRFProtect
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate # Import Flask-Migrate
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from config import DevelopmentConfig, ProductionConfig, TestingConfig

# from .database import init_db # Remove get_db_connection - REMOVED TO BREAK CIRCULAR IMPORT

# Create extension instances
login_manager = LoginManager()
mail = Mail()
csrf = CSRFProtect()
db = SQLAlchemy()
migrate = Migrate() # Initialize Migrate
limiter = Limiter(
    key_func=get_remote_address,
    default_limits=["200 per day", "50 per hour"]
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
    migrate.init_app(app, db) # Initialize Migrate with app and db
    limiter.init_app(app)

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

    from .models import init_roles
    @app.cli.command("init-roles")
    def init_roles_command():
        """Initialize roles with predefined data."""
        init_roles()
        print("Roles initialized.")

    # Context processor to inject user role information into templates
    from flask_login import current_user
    @app.context_processor
    def inject_user_role_info():
        user_role = None
        if current_user.is_authenticated and hasattr(current_user, 'role') and current_user.role:
            user_role = current_user.role
        return dict(user_role=user_role)

    # init_db() # Initialize the database - No longer needed with SQLAlchemy

    return app
