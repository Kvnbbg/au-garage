# app/__init__.py
from flask import Flask
import os
from flask_login import LoginManager
from flask_mail import Mail
from flask_wtf.csrf import CSRFProtect
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from flask_talisman import Talisman
from config import load_config
from app.cli import register_cli
from app.errors import register_error_handlers
from app.logging import configure_logging, init_request_context


def _normalize_sqlite_uri(app, database_uri):
    if not database_uri.startswith("sqlite:"):
        return database_uri
    if database_uri.startswith("sqlite:///:memory:"):
        return database_uri
    if database_uri.startswith("sqlite:///instance/"):
        relative_path = database_uri.replace("sqlite:///instance/", "", 1)
        absolute_path = os.path.join(app.instance_path, relative_path)
        return f"sqlite:///{os.path.abspath(absolute_path)}"
    if database_uri.startswith("sqlite:///"):
        return database_uri
    return database_uri


def _resolve_sqlite_path(database_uri):
    if not database_uri.startswith("sqlite:"):
        return None
    if database_uri.startswith("sqlite:///:memory:"):
        return None
    if database_uri.startswith("sqlite:///"):
        return database_uri.replace("sqlite:///", "", 1)
    return None


def _auto_initialize_sqlite(app):
    database_uri = app.config.get("SQLALCHEMY_DATABASE_URI", "")
    sqlite_path = _resolve_sqlite_path(database_uri)
    if not sqlite_path:
        return
    sqlite_dir = os.path.dirname(sqlite_path)
    if sqlite_dir:
        os.makedirs(sqlite_dir, exist_ok=True)
    with app.app_context():
        from .models import init_roles

        db.create_all()
        init_roles()


# Create extension instances
login_manager = LoginManager()
mail = Mail()
csrf = CSRFProtect()
db = SQLAlchemy()
migrate = Migrate()
limiter = Limiter(
    key_func=get_remote_address,
    default_limits=["200 per day", "50 per hour"]
)
talisman = Talisman()


def create_app(config_overrides=None):
    app = Flask(__name__)

    app_config, config_warnings = load_config()
    app.config.from_mapping(app_config.to_flask_dict())
    if config_overrides:
        app.config.update(config_overrides)
    app.config["SQLALCHEMY_DATABASE_URI"] = _normalize_sqlite_uri(
        app,
        app.config.get("SQLALCHEMY_DATABASE_URI", ""),
    )

    # Initialize extensions with the app object
    login_manager.init_app(app)
    mail.init_app(app)
    csrf.init_app(app)
    db.init_app(app)
    migrate.init_app(app, db)
    limiter.init_app(app)
    talisman.init_app(app)

    configure_logging(app)
    init_request_context(app)
    register_error_handlers(app)
    register_cli(app)
    _auto_initialize_sqlite(app)

    for warning in config_warnings:
        app.logger.warning(warning)

    login_manager.login_view = "auth.login"
    login_manager.login_message_category = "info"

    # User loader function for Flask-Login
    from .models import User

    @login_manager.user_loader
    def load_user(user_id):
        return db.session.get(User, int(user_id))

    # Register blueprints
    from .auth.routes import auth as auth_blueprint

    app.register_blueprint(auth_blueprint, url_prefix="/auth")

    from .main.routes import main as main_blueprint

    app.register_blueprint(main_blueprint)

    # Context processor to inject user role information into templates
    from flask_login import current_user
    @app.context_processor
    def inject_user_role_info():
        user_role = None
        if current_user.is_authenticated and hasattr(current_user, 'role') and current_user.role:
            user_role = current_user.role
        return dict(user_role=user_role)

    return app
